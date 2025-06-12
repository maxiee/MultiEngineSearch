"""
测试 CLI 功能的基本单元测试
"""

import pytest
from typer.testing import CliRunner
from unittest.mock import patch, MagicMock
from multienginesearch.cli import app
from multienginesearch.engines import SearchResult  # 导入 SearchResult

runner = CliRunner()


def test_version_command():
    """测试版本命令"""
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "Multi-Engine Search (mes) v0.1.0" in result.stdout


def test_config_list_command():
    """测试配置列表命令"""
    result = runner.invoke(app, ["config", "--list"])
    assert result.exit_code == 0
    assert "可用的搜索引擎:" in result.stdout
    assert "duckduckgo" in result.stdout
    assert "计划支持的搜索引擎:" in result.stdout


@patch("multienginesearch.cli.SearchEngineFactory.create_engine")
def test_search_command(mock_create_engine):
    """测试搜索命令"""
    # 配置模拟引擎和搜索方法
    mock_engine = MagicMock()
    mock_engine.name = "duckduckgo"
    mock_engine.search.return_value = [
        SearchResult(
            title="Test Title 1",
            url="http://example.com/1",
            description="Description 1",
            engine="duckduckgo",
        ),
        SearchResult(
            title="Test Title 2",
            url="http://example.com/2",
            description="Description 2",
            engine="duckduckgo",
        ),
    ]
    mock_create_engine.return_value = mock_engine

    result = runner.invoke(app, ["search", "test query"])
    assert result.exit_code == 0
    assert "Test Title 1" in result.stdout
    assert "http://example.com/1" in result.stdout
    assert "Description 1" in result.stdout
    # 验证模拟搜索是否被调用
    mock_engine.search.assert_called_once_with("test query", 10, time_filter=None)


@patch("multienginesearch.cli.SearchEngineFactory.create_engine")
def test_search_with_verbose(mock_create_engine):
    """测试带详细信息的搜索命令"""
    # 配置模拟引擎和搜索方法
    mock_engine = MagicMock()
    mock_engine.name = "duckduckgo"
    mock_engine.search.return_value = [
        SearchResult(
            title="Verbose Test",
            url="http://example.com/verbose",
            description="Verbose desc",
            engine="duckduckgo",
        )
    ]
    mock_create_engine.return_value = mock_engine

    result = runner.invoke(app, ["search", "test query", "--verbose"])
    assert result.exit_code == 0
    assert "正在搜索: test query" in result.stdout
    assert "搜索引擎: 默认 (DuckDuckGo)" in result.stdout
    assert "Verbose Test" in result.stdout
    mock_engine.search.assert_called_once_with("test query", 10, time_filter=None)


def test_search_with_options():
    """测试带选项的搜索命令 - 使用不支持的引擎"""
    result = runner.invoke(
        app,
        [
            "search",
            "test query",
            "--engine",
            "google",
            "--limit",
            "5",
            "--output",
            "json",
            "--verbose",
        ],
    )
    # Google 引擎不支持，应该返回错误
    assert result.exit_code == 1
    assert "不支持的搜索引擎: google" in result.stdout


@patch("multienginesearch.cli.SearchEngineFactory.create_engine")
def test_search_with_duckduckgo(mock_create_engine):
    """测试使用 DuckDuckGo 搜索"""
    # 配置模拟引擎和搜索方法
    mock_engine = MagicMock()
    mock_engine.name = "duckduckgo"
    mock_engine.search.return_value = [
        SearchResult(
            title="Python Test",
            url="http://python.org",
            description="Python official site",
            engine="duckduckgo",
        ),
        SearchResult(
            title="Tutorial Test",
            url="http://realpython.com",
            description="Real Python",
            engine="duckduckgo",
        ),
        SearchResult(
            title="Another Python",
            url="http://python.org/2",
            description="Python site 2",
            engine="duckduckgo",
        ),
    ]
    mock_create_engine.return_value = mock_engine

    result = runner.invoke(
        app,
        [
            "search",
            "python tutorial",
            "--engine",
            "duckduckgo",
            "--limit",
            "3",
            "--verbose",
        ],
    )
    assert result.exit_code == 0
    assert "正在搜索: python tutorial" in result.stdout
    assert "搜索引擎: duckduckgo" in result.stdout
    assert "结果限制: 3" in result.stdout
    assert "Python Test" in result.stdout
    assert "Tutorial Test" in result.stdout
    assert "Another Python" in result.stdout
    mock_engine.search.assert_called_once_with("python tutorial", 3, time_filter=None)


def test_help_command():
    """测试帮助命令"""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Multi-Engine Search - 多引擎搜索工具" in result.stdout
    assert "search" in result.stdout
    assert "config" in result.stdout
    assert "version" in result.stdout


@patch("multienginesearch.cli.SearchEngineFactory.create_engine")
def test_search_with_time_filter(mock_create_engine):
    """测试时间筛选搜索"""
    # 配置模拟引擎和搜索方法
    mock_engine = MagicMock()
    mock_engine.name = "duckduckgo"
    mock_engine.search.return_value = [
        SearchResult(
            title="Recent News",
            url="http://example.com/news_day",
            description="News from today",
            engine="duckduckgo",
        )
    ]
    mock_create_engine.return_value = mock_engine

    result = runner.invoke(
        app,
        [
            "search",
            "latest tech news",
            "--engine",
            "duckduckgo",
            "--limit",
            "1",
            "--time",
            "d",  # 最近一天
            "--verbose",
        ],
    )
    assert result.exit_code == 0
    assert "正在搜索: latest tech news" in result.stdout
    assert "搜索引擎: duckduckgo" in result.stdout
    assert "结果限制: 1" in result.stdout
    assert "时间筛选: 最近一天" in result.stdout
    assert "Recent News" in result.stdout
    mock_engine.search.assert_called_once_with("latest tech news", 1, time_filter="d")


@patch("multienginesearch.cli.SearchEngineFactory.create_engine")
def test_search_no_results(mock_create_engine):
    """测试搜索没有结果的情况"""
    # 配置模拟引擎和搜索方法，返回空列表
    mock_engine = MagicMock()
    mock_engine.name = "duckduckgo"
    mock_engine.search.return_value = []
    mock_create_engine.return_value = mock_engine

    result = runner.invoke(app, ["search", "a query that yields no results"])
    assert result.exit_code == 0
    assert "没有找到搜索结果" in result.stdout
    mock_engine.search.assert_called_once_with(
        "a query that yields no results", 10, time_filter=None
    )


@patch("multienginesearch.cli.SearchEngineFactory.create_engine")
def test_search_output_json(mock_create_engine):
    """测试 JSON 输出格式"""
    mock_engine = MagicMock()
    mock_engine.name = "duckduckgo"
    mock_search_results = [
        SearchResult(
            title="JSON Test 1",
            url="http://example.com/json1",
            description="Desc 1",
            engine="duckduckgo",
        ),
        SearchResult(
            title="JSON Test 2",
            url="http://example.com/json2",
            description="Desc 2",
            engine="duckduckgo",
        ),
    ]
    mock_engine.search.return_value = mock_search_results
    mock_create_engine.return_value = mock_engine

    result = runner.invoke(app, ["search", "json output test", "--output", "json"])
    assert result.exit_code == 0
    # 验证输出是否为有效的 JSON，并且包含预期的数据
    import json

    try:
        output_data = json.loads(result.stdout)
        assert isinstance(output_data, list)
        assert len(output_data) == 2
        assert output_data[0]["title"] == "JSON Test 1"
        assert output_data[1]["url"] == "http://example.com/json2"
    except json.JSONDecodeError:
        pytest.fail("Output is not valid JSON")
    mock_engine.search.assert_called_once_with("json output test", 10, time_filter=None)


# ... 其他测试用例 ...
# 注意：如果还有其他测试用例直接或间接调用了 DuckDuckGoEngine.search，
# 也需要用类似的方式进行 mock。
# 例如，如果 test_search_with_time_filter 之前没有 mock，现在也加上了。
