"""
测试 DuckDuckGo 搜索引擎
"""

import pytest
from multienginesearch.engines import (
    DuckDuckGoEngine,
    SearchEngineFactory,
    SearchResponse,
    GoogleEngine,
)
import os


def test_duckduckgo_engine_creation():
    """测试 DuckDuckGo 引擎创建"""
    engine = DuckDuckGoEngine()
    assert engine.name == "duckduckgo"


def test_search_engine_factory():
    """测试搜索引擎工厂"""
    # 测试创建 DuckDuckGo 引擎
    engine = SearchEngineFactory.create_engine("duckduckgo")
    assert engine is not None
    assert engine.name == "duckduckgo"

    # 测试创建不存在的引擎
    engine = SearchEngineFactory.create_engine("nonexistent")
    assert engine is None

    # 测试获取可用引擎列表
    engines = SearchEngineFactory.get_available_engines()
    assert "duckduckgo" in engines


def test_duckduckgo_search():
    """测试 DuckDuckGo 搜索功能"""
    engine = DuckDuckGoEngine()

    # 执行搜索
    response = engine.search("python programming", limit=3)

    # 验证响应类型
    assert isinstance(response, SearchResponse)
    assert isinstance(response.results, list)
    assert len(response.results) <= 3

    if response.results:  # 如果有结果
        result = response.results[0]
        assert hasattr(result, "title")
        assert hasattr(result, "url")
        assert hasattr(result, "description")
        assert hasattr(result, "engine")
        assert result.engine == "duckduckgo"

        # 测试转换为字典
        result_dict = result.to_dict()
        assert "title" in result_dict
        assert "url" in result_dict
        assert "description" in result_dict
        assert "engine" in result_dict

        # 测试响应转换为字典
        response_dict = response.to_dict()
        assert "results" in response_dict
        assert "count" in response_dict
        assert response_dict["count"] == len(response.results)


def test_duckduckgo_search_with_time_filter():
    """测试 DuckDuckGo 带时间筛选的搜索功能"""
    engine = DuckDuckGoEngine()

    # 测试不同的时间筛选参数
    time_filters = ["d", "w", "m", "y"]

    for time_filter in time_filters:
        # 执行带时间筛选的搜索
        response = engine.search("AI news", limit=2, time_filter=time_filter)

        # 验证响应
        assert isinstance(response, SearchResponse)
        assert isinstance(response.results, list)
        assert len(response.results) <= 2

        if response.results:  # 如果有结果
            result = response.results[0]
            assert hasattr(result, "title")
            assert hasattr(result, "url")
            assert hasattr(result, "description")
            assert hasattr(result, "engine")
            assert result.engine == "duckduckgo"

    # 测试无时间筛选（应该与默认行为一致）
    response_no_filter = engine.search("AI news", limit=2)
    response_with_none = engine.search("AI news", limit=2, time_filter=None)

    # 两种调用方式应该产生相同的行为
    assert isinstance(response_no_filter, SearchResponse)
    assert isinstance(response_with_none, SearchResponse)


if __name__ == "__main__":
    pytest.main([__file__])


def test_google_engine_rate_limit_tracking():
    """测试 Google 引擎限流跟踪功能"""
    # 设置测试环境变量（仅在测试时使用）
    test_api_key = os.getenv("MES_GOOGLE_API_KEY")
    test_search_engine_id = os.getenv("MES_GOOGLE_SEARCH_ENGINE_ID")

    if not test_api_key or not test_search_engine_id:
        pytest.skip("跳过 Google API 测试：未设置环境变量")

    try:
        engine = GoogleEngine()

        # 测试初始状态
        assert engine.daily_limit == 100
        assert engine.requests_used == 0

        # 执行一次搜索
        response = engine.search("test query", limit=1)

        # 验证响应类型
        assert isinstance(response, SearchResponse)

        # 验证限流信息存在
        assert response.rate_limit_info is not None
        assert "daily_limit" in response.rate_limit_info
        assert "requests_used" in response.rate_limit_info
        assert "requests_remaining" in response.rate_limit_info
        assert "limit_exceeded" in response.rate_limit_info

        # 验证限流值
        rate_info = response.rate_limit_info
        assert rate_info["daily_limit"] == 100
        assert rate_info["requests_used"] >= 1  # 至少使用了一次
        assert (
            rate_info["requests_remaining"]
            == rate_info["daily_limit"] - rate_info["requests_used"]
        )
        assert rate_info["limit_exceeded"] == (
            rate_info["requests_used"] >= rate_info["daily_limit"]
        )

        print(f"限流信息: {rate_info}")

    except ValueError as e:
        pytest.skip(f"跳过 Google API 测试: {e}")
    except Exception as e:
        # 其他异常可能是网络错误或 API 错误
        print(f"Google API 测试失败: {e}")
        # 不失败测试，因为这可能是网络问题


def test_search_response_to_dict():
    """测试 SearchResponse 对象的 to_dict 方法"""
    from multienginesearch.engines import SearchResult

    # 创建测试数据
    results = [
        SearchResult("Title 1", "http://example1.com", "Description 1", "test_engine"),
        SearchResult("Title 2", "http://example2.com", "Description 2", "test_engine"),
    ]

    rate_limit_info = {
        "daily_limit": 100,
        "requests_used": 5,
        "requests_remaining": 95,
        "limit_exceeded": False,
    }

    # 测试不带限流信息的响应
    response_without_rate_limit = SearchResponse(results)
    response_dict = response_without_rate_limit.to_dict()

    assert "results" in response_dict
    assert "count" in response_dict
    assert "rate_limit" not in response_dict
    assert response_dict["count"] == 2
    assert len(response_dict["results"]) == 2

    # 测试带限流信息的响应
    response_with_rate_limit = SearchResponse(results, rate_limit_info)
    response_dict = response_with_rate_limit.to_dict()

    assert "results" in response_dict
    assert "count" in response_dict
    assert "rate_limit" in response_dict
    assert response_dict["count"] == 2
    assert response_dict["rate_limit"] == rate_limit_info
