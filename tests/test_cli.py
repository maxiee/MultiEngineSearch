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
    assert "Multi-Engine Search (mse) v0.1.0" in result.stdout


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
    # 现在搜索会返回实际结果，而不是占位符消息
    assert "找到" in result.stdout and "个搜索结果" in result.stdout


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
