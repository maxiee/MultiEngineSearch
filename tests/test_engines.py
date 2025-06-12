"""
测试 DuckDuckGo 搜索引擎
"""

import pytest
from multienginesearch.engines import DuckDuckGoEngine, SearchEngineFactory


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
    results = engine.search("python programming", limit=3)

    # 验证结果
    assert isinstance(results, list)
    assert len(results) <= 3

    if results:  # 如果有结果
        result = results[0]
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


def test_duckduckgo_search_with_time_filter():
    """测试 DuckDuckGo 带时间筛选的搜索功能"""
    engine = DuckDuckGoEngine()

    # 测试不同的时间筛选参数
    time_filters = ["d", "w", "m", "y"]

    for time_filter in time_filters:
        # 执行带时间筛选的搜索
        results = engine.search("AI news", limit=2, time_filter=time_filter)

        # 验证结果
        assert isinstance(results, list)
        assert len(results) <= 2

        if results:  # 如果有结果
            result = results[0]
            assert hasattr(result, "title")
            assert hasattr(result, "url")
            assert hasattr(result, "description")
            assert hasattr(result, "engine")
            assert result.engine == "duckduckgo"

    # 测试无时间筛选（应该与默认行为一致）
    results_no_filter = engine.search("AI news", limit=2)
    results_with_none = engine.search("AI news", limit=2, time_filter=None)

    # 两种调用方式应该产生相同的行为
    assert isinstance(results_no_filter, list)
    assert isinstance(results_with_none, list)


if __name__ == "__main__":
    pytest.main([__file__])
