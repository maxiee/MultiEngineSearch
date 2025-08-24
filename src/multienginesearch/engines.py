"""
搜索引擎接口和实现
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Tuple
from duckduckgo_search import DDGS
import json
import os
import requests
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
import pytz


class SearchResult:
    """搜索结果数据类"""

    def __init__(self, title: str, url: str, description: str, engine: str):
        self.title = title
        self.url = url
        self.description = description
        self.engine = engine

    def to_dict(self) -> Dict[str, str]:
        """转换为字典格式"""
        return {
            "title": self.title,
            "url": self.url,
            "description": self.description,
            "engine": self.engine,
        }


class SearchResponse:
    """搜索响应数据类，包含搜索结果和元数据"""

    def __init__(
        self,
        results: List[SearchResult],
        rate_limit_info: Optional[Dict[str, Any]] = None,
    ):
        self.results = results
        self.rate_limit_info = rate_limit_info

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        data = {
            "results": [result.to_dict() for result in self.results],
            "count": len(self.results),
        }
        if self.rate_limit_info:
            data["rate_limit"] = self.rate_limit_info
        return data


class SearchEngine(ABC):
    """搜索引擎抽象基类"""

    @abstractmethod
    def search(
        self, query: str, limit: int = 10, time_filter: Optional[str] = None
    ) -> SearchResponse:
        """执行搜索并返回结果

        Args:
            query: 搜索查询字符串
            limit: 返回结果数量限制
            time_filter: 时间筛选参数 (d=一天, w=一周, m=一月, y=一年)

        Returns:
            SearchResponse: 包含搜索结果和元数据的响应对象
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """搜索引擎名称"""
        pass


class DuckDuckGoEngine(SearchEngine):
    """DuckDuckGo 搜索引擎实现"""

    def __init__(self, region: str = "wt-wt", safesearch: str = "moderate"):
        self.region = region
        self.safesearch = safesearch

    @property
    def name(self) -> str:
        return "duckduckgo"

    def search(
        self, query: str, limit: int = 10, time_filter: Optional[str] = None
    ) -> SearchResponse:
        """使用 DuckDuckGo 执行搜索

        Args:
            query: 搜索查询字符串
            limit: 返回结果数量限制
            time_filter: 时间筛选参数 (d=一天, w=一周, m=一月, y=一年)
        """
        try:
            ddgs = DDGS()
            results = ddgs.text(
                keywords=query,
                region=self.region,
                safesearch=self.safesearch,
                timelimit=time_filter,  # 传递时间筛选参数
                max_results=limit,
            )

            search_results = []
            for result in results:
                search_result = SearchResult(
                    title=result.get("title", ""),
                    url=result.get("href", ""),
                    description=result.get("body", ""),
                    engine=self.name,
                )
                search_results.append(search_result)

            return SearchResponse(search_results)

        except Exception as e:
            # 发生错误时返回空列表，避免程序崩溃
            print(f"DuckDuckGo 搜索出错: {e}")
            return SearchResponse([])


class GoogleEngine(SearchEngine):
    """Google Custom Search API 搜索引擎实现"""

    def __init__(self):
        # 从环境变量获取 API 密钥和搜索引擎 ID
        self.api_key = os.getenv("MES_GOOGLE_API_KEY")
        self.search_engine_id = os.getenv("MES_GOOGLE_SEARCH_ENGINE_ID")

        # 初始化限流配置
        self.daily_limit = 100

        # 初始化持久化配额跟踪
        self._init_quota_tracking()

        if not self.api_key or not self.search_engine_id:
            raise ValueError(
                "Google Search API 需要设置环境变量: "
                "MES_GOOGLE_API_KEY 和 MES_GOOGLE_SEARCH_ENGINE_ID"
            )

    def _init_quota_tracking(self):
        """初始化持久化配额跟踪"""
        # 使用用户主目录下的配置文件
        home_dir = Path.home()
        self.quota_file = home_dir / ".mes_google_quota.json"

        # 如果文件不存在或者是新的一天，初始化配额
        self._load_or_reset_quota()

    def _get_pacific_time(self) -> datetime:
        """获取太平洋时间（Google API 配额重置时区）"""
        pacific_tz = pytz.timezone("US/Pacific")
        return datetime.now(pacific_tz)

    def _get_next_reset_time(self) -> datetime:
        """获取下次配额重置时间（太平洋时间的明天午夜）"""
        pacific_tz = pytz.timezone("US/Pacific")
        now_pacific = self._get_pacific_time()
        # 明天午夜（太平洋时间）
        next_reset = (now_pacific + timedelta(days=1)).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        return next_reset

    def _load_or_reset_quota(self):
        """加载或重置配额信息"""
        # 使用太平洋时间作为基准
        pacific_now = self._get_pacific_time()
        today_pacific = pacific_now.date().isoformat()

        default_quota = {
            "date": today_pacific,
            "requests_used": 0,
            "daily_limit": self.daily_limit,
            "reset_time": self._get_next_reset_time().isoformat(),
            "timezone": "US/Pacific",
        }

        try:
            if self.quota_file.exists():
                with open(self.quota_file, "r", encoding="utf-8") as f:
                    quota_data = json.load(f)

                # 检查是否是新的一天（基于太平洋时间）
                if quota_data.get("date") != today_pacific:
                    # 新的一天，重置配额
                    quota_data = default_quota
                    self._save_quota(quota_data)
                else:
                    # 更新重置时间（以防时区变化）
                    quota_data["reset_time"] = self._get_next_reset_time().isoformat()
                    quota_data["timezone"] = "US/Pacific"
                    self._save_quota(quota_data)
            else:
                # 文件不存在，创建新文件
                quota_data = default_quota
                self._save_quota(quota_data)

            self.quota_data = quota_data

        except (json.JSONDecodeError, KeyError, IOError):
            # 文件损坏或格式错误，重置
            self.quota_data = default_quota
            self._save_quota(default_quota)

    def _save_quota(self, quota_data):
        """保存配额信息到文件"""
        try:
            with open(self.quota_file, "w", encoding="utf-8") as f:
                json.dump(quota_data, f, indent=2, ensure_ascii=False)
        except IOError:
            # 如果保存失败，继续使用内存中的数据
            pass

    def _update_quota_usage(self):
        """更新配额使用情况"""
        self.quota_data["requests_used"] += 1
        self._save_quota(self.quota_data)

    def _get_quota_info(self) -> Dict[str, Any]:
        """获取当前配额信息"""
        requests_used = self.quota_data["requests_used"]
        daily_limit = self.quota_data["daily_limit"]
        requests_remaining = max(0, daily_limit - requests_used)

        # 确保重置时间是最新的
        reset_time = self._get_next_reset_time().isoformat()

        return {
            "daily_limit": daily_limit,
            "requests_used": requests_used,
            "requests_remaining": requests_remaining,
            "limit_exceeded": requests_used >= daily_limit,
            "reset_time": reset_time,
            "timezone": "US/Pacific",
            "source": "persistent_tracking",
        }

    @property
    def name(self) -> str:
        return "google"

    def _build_payload(
        self,
        query: str,
        start: int = 1,
        num: int = 10,
        date_restrict: Optional[str] = None,
    ) -> Dict[str, Any]:
        """构建 Google Search API 请求参数"""
        payload = {
            "key": self.api_key,
            "q": query,
            "cx": self.search_engine_id,
            "start": start,
            "num": num,
        }

        # 时间筛选映射
        if date_restrict:
            time_mapping = {
                "d": "d1",  # 最近一天
                "w": "w1",  # 最近一周
                "m": "m1",  # 最近一月
                "y": "y1",  # 最近一年
            }
            payload["dateRestrict"] = time_mapping.get(date_restrict, date_restrict)

        return payload

    def _make_request(
        self, payload: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """发送 GET 请求到 Google Search API

        Returns:
            Tuple[Dict, Dict]: (响应数据, 限流信息)
        """
        # 检查是否已达到配额限制
        if self.quota_data["requests_used"] >= self.quota_data["daily_limit"]:
            rate_limit_info = self._get_quota_info()
            raise Exception(
                f"Google API 配额已达到每日限制 {self.quota_data['daily_limit']} 次。"
                f"将在 {rate_limit_info['reset_time']} 重置。"
            )

        response = requests.get(
            "https://www.googleapis.com/customsearch/v1", params=payload
        )

        if response.status_code != 200:
            raise Exception(
                f"Google Search API 请求失败，状态码: {response.status_code}"
            )

        # 更新配额使用情况
        self._update_quota_usage()

        # 获取当前配额信息
        rate_limit_info = self._get_quota_info()

        return response.json(), rate_limit_info

    def search(
        self, query: str, limit: int = 10, time_filter: Optional[str] = None
    ) -> SearchResponse:
        """使用 Google Custom Search API 执行搜索

        Args:
            query: 搜索查询字符串
            limit: 返回结果数量限制 (1-100)
            time_filter: 时间筛选参数 (d=一天, w=一周, m=一月, y=一年)
        """
        try:
            search_results = []
            rate_limit_info = None

            # Google API 每次最多返回 10 条结果，需要分页请求
            pages_needed = (limit - 1) // 10 + 1

            for page in range(pages_needed):
                start_index = page * 10 + 1

                # 最后一页可能不需要完整的 10 条结果
                if page == pages_needed - 1:
                    remaining = limit - len(search_results)
                    num_results = min(10, remaining)
                else:
                    num_results = 10

                if num_results <= 0:
                    break

                payload = self._build_payload(
                    query=query,
                    start=start_index,
                    num=num_results,
                    date_restrict=time_filter,
                )

                response_data, current_rate_limit = self._make_request(payload)
                rate_limit_info = current_rate_limit  # 保存最新的限流信息

                # 处理搜索结果
                items = response_data.get("items", [])
                if not items:
                    break

                for item in items:
                    if len(search_results) >= limit:
                        break

                    search_result = SearchResult(
                        title=item.get("title", ""),
                        url=item.get("link", ""),
                        description=item.get("snippet", ""),
                        engine=self.name,
                    )
                    search_results.append(search_result)

                # 如果这次请求返回的结果少于预期，说明没有更多结果了
                if len(items) < num_results:
                    break

            return SearchResponse(search_results, rate_limit_info)

        except Exception as e:
            # 发生错误时返回空列表，避免程序崩溃
            print(f"Google 搜索出错: {e}")
            return SearchResponse([])


class SearchEngineFactory:
    """搜索引擎工厂类"""

    _engines = {
        "duckduckgo": DuckDuckGoEngine,
        "google": GoogleEngine,
    }

    @classmethod
    def create_engine(cls, engine_name: str) -> Optional[SearchEngine]:
        """创建指定的搜索引擎实例"""
        if engine_name.lower() in cls._engines:
            try:
                return cls._engines[engine_name.lower()]()
            except Exception as e:
                print(f"创建搜索引擎 {engine_name} 失败: {e}")
                return None
        return None

    @classmethod
    def get_available_engines(cls) -> List[str]:
        """获取所有可用的搜索引擎名称"""
        return list(cls._engines.keys())

    @classmethod
    def register_engine(cls, name: str, engine_class: type):
        """注册新的搜索引擎"""
        cls._engines[name.lower()] = engine_class


# 搜索结果格式化函数
def format_results(response: SearchResponse, output_format: str = "simple") -> str:
    """格式化搜索结果"""
    if not response.results:
        return "❌ 没有找到搜索结果"

    if output_format == "json":
        return json.dumps(response.to_dict(), ensure_ascii=False, indent=2)
    else:  # simple format
        output = []
        output.append(f"🔍 找到 {len(response.results)} 个搜索结果:\n")

        for i, result in enumerate(response.results, 1):
            output.append(f"{i:2d}. {result.title}")
            output.append(f"    🔗 {result.url}")
            output.append(f"    📄 {result.description}")
            output.append(f"    🔍 来源: {result.engine}")
            output.append("")

        # 添加限流信息到 simple 格式
        if response.rate_limit_info:
            output.append("📊 API 使用情况:")
            rate_info = response.rate_limit_info
            output.append(f"    • 每日限额: {rate_info['daily_limit']} 次")
            output.append(f"    • 已使用: {rate_info['requests_used']} 次")
            output.append(f"    • 剩余: {rate_info['requests_remaining']} 次")

            if "reset_time" in rate_info:
                from datetime import datetime
                import pytz

                try:
                    # 解析时间并保持时区信息
                    reset_time = datetime.fromisoformat(rate_info["reset_time"])
                    # 如果没有时区信息，假设是太平洋时间
                    if reset_time.tzinfo is None:
                        pacific_tz = pytz.timezone("US/Pacific")
                        reset_time = pacific_tz.localize(reset_time)

                    # 显示时间和时区
                    timezone_name = rate_info.get("timezone", "Unknown")
                    output.append(
                        f"    • 配额重置: {reset_time.strftime('%Y-%m-%d %H:%M')} ({timezone_name})"
                    )
                except (ValueError, TypeError):
                    output.append(f"    • 配额重置: {rate_info['reset_time']}")

            if rate_info["limit_exceeded"]:
                output.append("    ⚠️ 警告: 已达到每日限额!")
            elif rate_info["requests_remaining"] < 10:
                output.append("    ⚠️ 提醒: 剩余配额不足10次")

            # 显示数据来源
            source_text = {
                "api_headers": "API响应头",
                "persistent_tracking": "本地跟踪",
                "local_counter": "会话计数器",
            }.get(rate_info.get("source", "unknown"), "未知")
            output.append(f"    • 数据来源: {source_text}")
            output.append("")

        return "\n".join(output)
