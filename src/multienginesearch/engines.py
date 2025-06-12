"""
搜索引擎接口和实现
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from duckduckgo_search import DDGS
import json


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
    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        """执行搜索并返回结果"""
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

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        """使用 DuckDuckGo 执行搜索"""
        try:
            ddgs = DDGS()
            results = ddgs.text(
                keywords=query,
                region=self.region,
                safesearch=self.safesearch,
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


class SearchEngineFactory:
    """搜索引擎工厂类"""

    _engines = {
        "duckduckgo": DuckDuckGoEngine,
    }

    @classmethod
    def create_engine(cls, engine_name: str) -> Optional[SearchEngine]:
        """创建指定的搜索引擎实例"""
        if engine_name.lower() in cls._engines:
            return cls._engines[engine_name.lower()]()
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
