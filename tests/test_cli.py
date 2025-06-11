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
    assert "google" in result.stdout
    assert "bing" in result.stdout
    assert "duckduckgo" in result.stdout


def test_search_command():
    """测试搜索命令"""
    result = runner.invoke(app, ["search", "test query"])
    assert result.exit_code == 0
    assert "搜索 'test query' 的结果将在这里显示" in result.stdout


def test_search_with_verbose():
    """测试带详细信息的搜索命令"""
    result = runner.invoke(app, ["search", "test query", "--verbose"])
    assert result.exit_code == 0
    assert "正在搜索: test query" in result.stdout
    assert "搜索引擎: 全部" in result.stdout


def test_search_with_options():
    """测试带选项的搜索命令"""
    result = runner.invoke(app, [
        "search", "test query", 
        "--engine", "google", 
        "--limit", "5", 
        "--output", "json",
        "--verbose"
    ])
    assert result.exit_code == 0
    assert "正在搜索: test query" in result.stdout
    assert "搜索引擎: google" in result.stdout
    assert "结果限制: 5" in result.stdout
    assert "输出格式: json" in result.stdout


def test_help_command():
    """测试帮助命令"""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Multi-Engine Search - 多引擎搜索工具" in result.stdout
    assert "search" in result.stdout
    assert "config" in result.stdout
    assert "version" in result.stdout
