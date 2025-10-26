#!/usr/bin/env python
# encoding:utf-8
from loguru import logger
import json


async def json2string(input_json):
  logger.info("[JSON转换String] APP 执行参数为: {input_json}", input_json=input_json)
  try:
    parsed_string = json.dumps(input_json, ensure_ascii=False, indent=2)
    return {"status": 0, "result": parsed_string}
  except Exception as e:
    logger.error("[JSON转换String] JSON序列化错误: {error}", error=str(e))
    return {"status": 2, "result": "Invalid JSON object"}

async def string2json(input_string):
    logger.info("[String转换JSON] APP 执行参数为: {input_string}", input_string=input_string)
    try:
        parsed_json = json.loads(input_string)
        return {"status": 0, "result": parsed_json}
    except Exception as e:
        logger.error("[String转换JSON] JSON解析错误: {error}", error=str(e))
        return {"status": 2, "result": "Invalid JSON string"}

if __name__ == '__main__':
    # 导入异步库
    import asyncio

    test_input_string = r"""{
  "config": {
    "appName": "SimpleTestApp",
    "version": 1.2,
    "isEnabled": true,
    "maxRetries": 3,
    "tempThreshold": null,
    "database": {
      "host": "localhost",
      "port": 5432,
      "sslEnabled": false
    },
    "features": [
      "logging",
      "caching",
      "authentication"
    ]
  },
  "status": "active",
  "lastUpdated": "2025-10-26T21:45:00Z",
  "report": "System Check Report - 2025-10-26\nHostname: server-01\nUptime: 15 days, 3:22\nCPU Load: 0.15, 0.10, 0.08\nMemory Usage: 45% (3.2GB/7GB)\nDisk Usage: / 68%, /var 45%\nServices: sshd[UP], nginx[UP], mysql[UP]\nSecurity: No critical updates pending"
}"""


    # 测试函数
    async def test():
        result2 = await string2json(test_input_string)
        result1 = await json2string(result2)

        print(result1)
        print(result2)


    # 加入异步队列
    async def main(): await asyncio.gather(test())


    # 启动执行
    asyncio.run(main())