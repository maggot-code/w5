#!/usr/bin/env python
# encoding:utf-8
from loguru import logger
import requests

async def requester(url, method="POST", output="JSON", headers=None, body=None):
    logger.info(f"[Requester] APP 执行参数: url={url}, method={method}, output={output}")
    req_headers = _parse_kv_lines(headers) if headers else {}
    # 默认 Content-Type: application/json
    if not any(k.lower() == "content-type" for k in req_headers):
        req_headers["Content-Type"] = "application/json"

    # 解析 body，每行一个 key:value，转 dict
    req_body = None
    if body:
        req_body = _parse_kv_lines(body)

    try:
        if method.upper() == "GET":
            resp = requests.get(url, headers=req_headers)
        elif method.upper() == "POST":
            resp = requests.post(url, headers=req_headers, json=req_body)
        else:
            return {"status": 1, "result": f"不支持的请求方式: {method}"}

        if output.upper() == "TEXT":
            return {"status": 0, "result": resp.text}
        elif output.upper() == "JSON":
            return {"status": 0, "result": _try_parse_json(resp.text)}
        else:
            return {"status": 0, "result": str(resp)}
    except Exception as e:
        logger.error(f"[Requester] APP 执行错误: {str(e)}")
        return {"status": 2, "result": str(e)}


def _parse_kv_lines(text):
    data = {}
    for line in text.splitlines():
        if ':' in line:
            k, v = line.split(':', 1)
            data[k.strip()] = v.strip()
    return data

def _try_parse_json(text):
    import json
    if isinstance(text, dict):
        return text
    try:
        return json.loads(text) if text else None
    except Exception:
        return text

if __name__ == '__main__':
    # 导入异步库
    import asyncio

        # 测试函数
    async def test():
        pass


    # 加入异步队列
    async def main(): await asyncio.gather(test())


    # 启动执行
    asyncio.run(main())