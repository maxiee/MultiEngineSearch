"""
MultiEngineSearch - 多引擎搜索工具

一个遵循Unix哲学原则的多搜索引擎统一命令行界面工具。
"""

from .engines import (
    SearchResult,
    SearchEngine,
    DuckDuckGoEngine,
    SearchEngineFactory,
    format_results,
)
from .cli import app, main

__version__ = "0.1.0"
__all__ = [
    "SearchResult",
    "SearchEngine",
    "DuckDuckGoEngine",
    "SearchEngineFactory",
    "format_results",
    "app",
    "main",
]
