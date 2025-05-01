import httpx
import asyncio
from typing import List, Dict, Any, Optional
from mcp.server import FastMCP

# # 初始化 FastMCP 服务器
app = FastMCP('todo')

@app.tool()
async def get_todo(year :int) -> str:
    """获取本地指定目录下的文件列表。

    Args:
        year: 指定年份找到当年的计划目标或愿望
    """
    match year:
        case 2022: return "学习python"  # 2022年计划目标或愿望
        case 2023: return "学习java"  # 2023年计划目标或愿望
        case 2024: return "学习c++"  # 2024年计划目标或愿望
        case 2025: return "学习数学"
        case 2026: return "学习英语"
        case 2027: return "买小汽车"
        case 2028: return "买房子"
        case 2029: return "买飞机"

if __name__ == "__main__":
    print("todo 服务启动...")
    app.run(transport='stdio')