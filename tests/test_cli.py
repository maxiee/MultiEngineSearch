"""
测试 CLI 功能的基本单元测试
"""

import pytest
from typer.testing import CliRunner
from multienginesearch.cli import app

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


def test_search_command():
    """测试搜索命令"""
    result = runner.invoke(app, ["search", "test query"])
    assert result.exit_code == 0
    # 现在搜索会返回实际结果，如果遇到速率限制会显示错误信息
    assert (
        "找到" in result.stdout and "个搜索结果" in result.stdout
    ) or "没有找到搜索结果" in result.stdout


def test_search_with_verbose():
    """测试带详细信息的搜索命令"""
    result = runner.invoke(app, ["search", "test query", "--verbose"])
    assert result.exit_code == 0
    assert "正在搜索: test query" in result.stdout
    assert "搜索引擎: 默认 (DuckDuckGo)" in result.stdout


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


def test_search_with_duckduckgo():
    """测试使用 DuckDuckGo 搜索"""
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


def test_help_command():
    """测试帮助命令"""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Multi-Engine Search - 多引擎搜索工具" in result.stdout
    assert "search" in result.stdout
    assert "config" in result.stdout
    assert "version" in result.stdout


def test_search_with_time_filter():
    """测试时间筛选搜索"""
    result = runner.invoke(
        app,
        [
            "search",
            "AI news",
            "--time",
            "d",
            "--limit",
            "2",
            "--verbose",
        ],
    )
    assert result.exit_code == 0
    assert "正在搜索: AI news" in result.stdout
    assert "时间筛选: 最近一天" in result.stdout


def test_search_with_invalid_time_filter():
    """测试无效时间筛选参数"""
    result = runner.invoke(
        app,
        [
            "search",
            "test query",
            "--time",
            "invalid",
        ],
    )
    assert result.exit_code == 1
    assert "无效的时间筛选参数" in result.stdout
    assert "支持的选项: d (一天), w (一周), m (一月), y (一年)" in result.stdout


def test_search_with_all_time_filters():
    """测试所有时间筛选选项"""
    time_filters = ["d", "w", "m", "y"]
    time_labels = ["最近一天", "最近一周", "最近一月", "最近一年"]

    for time_filter, expected_label in zip(time_filters, time_labels):
        result = runner.invoke(
            app,
            [
                "search",
                "test query",
                "--time",
                time_filter,
                "--verbose",
                "--limit",
                "1",
            ],
        )
        assert result.exit_code == 0
        assert f"时间筛选: {expected_label}" in result.stdout
