#!/usr/bin/env python
# encoding:utf-8
from loguru import logger
import requests, json

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

async def batch_requester(source, extract, url, method="POST", output="JSON", headers=None, body=None):
    logger.info(f"[BatchRequester] APP 执行参数: source={source}, extract={extract}, body={body}")
    try:
        # 解析 source 为列表，兼容首尾多余引号和常见格式
        items = None
        if isinstance(source, str):
            src = source.strip()
            # 去除首尾引号
            if src.startswith('"') and src.endswith('"'):
                src = src[1:-1]
            # 替换转义
            src = src.replace('\\"', '"')
            # 尝试 json 解析
            try:
                items = json.loads(src)
            except Exception as e:
                logger.error(f"[BatchRequester] source json.loads 失败: {e}, src={src}")
                items = None
        elif isinstance(source, list):
            items = source
        else:
            logger.error("[BatchRequester] source 类型错误")
            return {"status": 1, "result": "source 类型错误"}

        if not isinstance(items, list):
            logger.error(f"[BatchRequester] source 解析后不是 list 类型: {type(items)}")
            return {"status": 1, "result": "source 解析后不是 list 类型"}

        # 解析 extract 映射规则
        extract_map = _parse_kv_lines(extract)
        # 解析外部 body 参数
        static_body = _parse_kv_lines(body) if body else {}

        results = []
        for item in items:
            if not isinstance(item, dict):
                logger.error(f"[BatchRequester] item 不是 dict 类型: {item}")
                results.append({"status": 1, "result": f"item 不是 dict 类型: {item}"})
                continue
            # 构建 body，合并静态参数和动态参数
            body_dict = static_body.copy()
            for k, item_key in extract_map.items():
                body_dict[k] = item.get(item_key)
            # 调用 requester
            result = await requester(url=url, method=method, output=output, headers=headers, body='\n'.join([f'{k}:{v}' for k,v in body_dict.items() if v is not None]))
            results.append(result)
        return {"status": 0, "result": results}
    except Exception as e:
        logger.error(f"[BatchRequester] APP 执行错误: {str(e)}")
        return {"status": 2, "result": str(e)}

def _parse_kv_lines(text):
    data = {}
    for line in text.splitlines():
        if ':' in line:
            k, v = line.split(':', 1)
            data[k.strip()] = v.strip()
    return data

def _try_parse_json(text):
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