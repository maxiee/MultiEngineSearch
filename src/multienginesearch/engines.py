"""
搜索引擎接口和实现
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from duckduckgo_search import DDGS
import json
import os
import requests


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


class SearchEngine(ABC):
    """搜索引擎抽象基类"""

    @abstractmethod
    def search(
        self, query: str, limit: int = 10, time_filter: Optional[str] = None
    ) -> List[SearchResult]:
        """执行搜索并返回结果

        Args:
            query: 搜索查询字符串
            limit: 返回结果数量限制
            time_filter: 时间筛选参数 (d=一天, w=一周, m=一月, y=一年)
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
    ) -> List[SearchResult]:
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

            return search_results

        except Exception as e:
            # 发生错误时返回空列表，避免程序崩溃
            print(f"DuckDuckGo 搜索出错: {e}")
            return []


class GoogleEngine(SearchEngine):
    """Google Custom Search API 搜索引擎实现"""

    def __init__(self):
        # 从环境变量获取 API 密钥和搜索引擎 ID
        self.api_key = os.getenv("MES_GOOGLE_API_KEY")
        self.search_engine_id = os.getenv("MES_GOOGLE_SEARCH_ENGINE_ID")

        if not self.api_key or not self.search_engine_id:
            raise ValueError(
                "Google Search API 需要设置环境变量: "
                "MES_GOOGLE_API_KEY 和 MES_GOOGLE_SEARCH_ENGINE_ID"
            )

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

    def _make_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """发送 GET 请求到 Google Search API"""
        response = requests.get(
            "https://www.googleapis.com/customsearch/v1", params=payload
        )
        if response.status_code != 200:
            raise Exception(
                f"Google Search API 请求失败，状态码: {response.status_code}"
            )
        return response.json()

    def search(
        self, query: str, limit: int = 10, time_filter: Optional[str] = None
    ) -> List[SearchResult]:
        """使用 Google Custom Search API 执行搜索

        Args:
            query: 搜索查询字符串
            limit: 返回结果数量限制 (1-100)
            time_filter: 时间筛选参数 (d=一天, w=一周, m=一月, y=一年)
        """
        try:
            search_results = []

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

                response_data = self._make_request(payload)

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

            return search_results

        except Exception as e:
            # 发生错误时返回空列表，避免程序崩溃
            print(f"Google 搜索出错: {e}")
            return []


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
def format_results(results: List[SearchResult], output_format: str = "simple") -> str:
    """格式化搜索结果"""
    if not results:
        return "❌ 没有找到搜索结果"

    if output_format == "json":
        return json.dumps(
            [result.to_dict() for result in results], ensure_ascii=False, indent=2
        )
    else:  # simple format
        output = []
        output.append(f"🔍 找到 {len(results)} 个搜索结果:\n")

        for i, result in enumerate(results, 1):
            output.append(f"{i:2d}. {result.title}")
            output.append(f"    🔗 {result.url}")
            output.append(f"    📄 {result.description}")
            output.append(f"    🔍 来源: {result.engine}")
            output.append("")

        return "\n".join(output)
