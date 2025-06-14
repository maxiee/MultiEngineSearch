"""
Multi-Engine Search CLI
使用 Typer 框架构建的命令行界面
"""

import typer
from typing import Optional
from typing_extensions import Annotated
from .engines import SearchEngineFactory, format_results

app = typer.Typer(
    name="mes",
    help="Multi-Engine Search - 多引擎搜索工具",
    add_completion=False,
    rich_markup_mode="markdown"
)


@app.command()
def search(
    query: Annotated[str, typer.Argument(help="搜索查询字符串")],
    engine: Annotated[
        Optional[str], 
        typer.Option(
            "--engine", "-e",
            help="指定搜索引擎 (google, duckduckgo, bing)"
        )
    ] = None,
    limit: Annotated[
        int, 
        typer.Option(
            "--limit", "-l",
            help="返回结果数量限制",
            min=1,
            max=100
        )
    ] = 10,
    output: Annotated[
        Optional[str],
        typer.Option(
            "--output", "-o",
            help="输出格式 (json, simple)"
        )
    ] = "simple",
    verbose: Annotated[
        bool,
        typer.Option(
            "--verbose", "-v",
            help="显示详细信息"
        )
    ] = False,
    time: Annotated[
        Optional[str],
        typer.Option(
            "--time", "-t",
            help="时间筛选范围 (d=最近一天, w=最近一周, m=最近一月, y=最近一年)"
        )
    ] = None,
):
    """
    执行多引擎搜索
    
    **示例用法:**
    
    - `mes search "python tutorial"`
    - `mes search "机器学习" --engine google --limit 5`
    - `mes search "AI新闻" --output json --verbose`
    - `mes search "最新技术" --time d --limit 10`
    """
    # 验证时间筛选参数
    if time and time not in ["d", "w", "m", "y"]:
        typer.echo("❌ 无效的时间筛选参数。支持的选项: d (一天), w (一周), m (一月), y (一年)")
        raise typer.Exit(1)
    
    if verbose:
        typer.echo(f"正在搜索: {query}")
        typer.echo(f"搜索引擎: {engine or '默认 (DuckDuckGo)'}")
        typer.echo(f"结果限制: {limit}")
        typer.echo(f"输出格式: {output}")
        if time:
            time_labels = {"d": "最近一天", "w": "最近一周", "m": "最近一月", "y": "最近一年"}
            typer.echo(f"时间筛选: {time_labels.get(time, time)}")
    
    # 默认使用 DuckDuckGo
    engine_name = engine or "duckduckgo"
    
    # 创建搜索引擎实例
    search_engine = SearchEngineFactory.create_engine(engine_name)
    
    if not search_engine:
        available_engines = SearchEngineFactory.get_available_engines()
        typer.echo(f"❌ 不支持的搜索引擎: {engine_name}")
        typer.echo(f"� 可用的搜索引擎: {', '.join(available_engines)}")
        raise typer.Exit(1)
    
    # 执行搜索
    if verbose:
        typer.echo(f"🔍 正在使用 {search_engine.name} 搜索...")
    
    results = search_engine.search(query, limit, time_filter=time)
    
    if not results:
        typer.echo("❌ 没有找到搜索结果")
        return
    
    # 格式化并输出结果
    formatted_results = format_results(results, output or "simple")
    typer.echo(formatted_results)


@app.command()
def config(
    list_engines: Annotated[
        bool,
        typer.Option(
            "--list", "-l",
            help="列出所有可用的搜索引擎"
        )
    ] = False,
    set_default: Annotated[
        Optional[str],
        typer.Option(
            "--set-default",
            help="设置默认搜索引擎"
        )
    ] = None,
):
    """
    配置搜索引擎和设置
    
    **示例用法:**
    
    - `mes config --list`
    - `mes config --set-default google`
    """
    if list_engines:
        typer.echo("📋 可用的搜索引擎:")
        engines = SearchEngineFactory.get_available_engines()
        for engine in engines:
            typer.echo(f"  • {engine}")
        
        typer.echo("\n💡 计划支持的搜索引擎:")
        planned_engines = ["bing", "baidu"]
        for engine in planned_engines:
            typer.echo(f"  • {engine} (开发中)")
    
    if set_default:
        available_engines = SearchEngineFactory.get_available_engines()
        if set_default in available_engines:
            typer.echo(f"✅ 已设置默认搜索引擎为: {set_default}")
            # TODO: 实现配置保存逻辑
        else:
            typer.echo(f"❌ 不支持的搜索引擎: {set_default}")
            typer.echo(f"💡 可用的搜索引擎: {', '.join(available_engines)}")


@app.command()
def version():
    """
    显示版本信息
    """
    typer.echo("🔍 Multi-Engine Search (mes) v0.1.0")
    typer.echo("   一个强大的多引擎搜索工具")


def main():
    """CLI 入口点"""
    app()


if __name__ == "__main__":
    main()
