import os

import httpx
import asyncio
from typing import List, Dict, Any, Optional
from mcp.server import FastMCP

# # 初始化 FastMCP 服务器
app = FastMCP('get_WeatherForecast')

@app.tool()
async def get_weather_forecast( location: str = "beijing", 
                               days: int = 5) -> List[Dict[str, str]]:
    """
    获取指定地点的未来几天天气预报
    
    Args:
        location (str): 地点名称（如'beijing'），默认为北京
        days (int, optional): 要获取的天数，默认为5天
        
    Returns:
        List[Dict[str, str]]: 天气预报数据的列表，每个元素是一个包含天气信息的字典
    """
    url = "https://api.seniverse.com/v3/weather/daily.json"
    params = {
        'key': "SkUkrLW-_y20nTC6h",
        'location': location,
        'language': 'zh-Hans',
        'unit': 'c',
        'start': 0,
        'days': days
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()  # 检查HTTP响应状态码
        
        data = response.json()
        results = data.get('results', [{}])[0]
        forecast_list = results.get('daily', [])
        
        # 转换数据格式，仅保留关键信息
        weather_forecast = []
        for forecast in forecast_list:
            date = forecast.get('date')
            weather = forecast.get('text_day')
            temp_high = forecast.get('high')
            temp_low = forecast.get('low')
            humidity = forecast.get('humidity')
            wind = f"{forecast['wind_direction']} {forecast['wind_scale']}级"
            rainfall = f"{forecast.get('rainfall')}mm"
 
            weather_forecast.append({
                'date': date,
                'weather': weather,
                'temp_high': temp_high,
                'temp_low': temp_low,
                'humidity': humidity,
                'wind': wind,
                'rainfall': rainfall
            })
            
        return weather_forecast


@app.tool()
async def web_search(query: str) -> str:
    """
    搜索互联网内容

    Args:
        query: 要搜索内容

    Returns:
        搜索结果的总结
    """

    async with httpx.AsyncClient() as client:
        response = await client.post(
            'https://open.bigmodel.cn/api/paas/v4/tools',
            headers={'Authorization': 'ac48f03d267c44f4b4b6438cf154ac3a.u9ZbXnLbK7ogl7wi'},
            json={
                'tool': 'web-search-pro',
                'messages': [
                    {'role': 'user', 'content': query}
                ],
                'stream': False
            }
        )

        res_data = []
        for choice in response.json()['choices']:
            for message in choice['message']['tool_calls']:
                search_results = message.get('search_result')
                if not search_results:
                    continue
                for result in search_results:
                    res_data.append(result['content'])

        return '\n\n\n'.join(res_data)
    

if __name__ == "__main__":
    print("get_WeatherForecast 服务启动")
    app.run(transport='stdio')