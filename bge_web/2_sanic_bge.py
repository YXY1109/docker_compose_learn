import argparse
import asyncio
import functools
import os

import numpy as np
import torch
from FlagEmbedding import BGEM3FlagModel, FlagAutoReranker
from loguru import logger
from sanic import Request, Sanic, json
from sanic.worker.manager import WorkerManager

parser = argparse.ArgumentParser()
parser.add_argument('--workers', type=int, default=1, help='workers')
parser.add_argument('--host', default="0.0.0.0", help='IP地址')
parser.add_argument('--port', type=int, default=8010, help='端口号')
parser.add_argument('--bge_m3_path', type=str, default="", help='向量模型路径')
parser.add_argument('--bge_reranker_path', type=str, default="", help='重排模型路径')
args = parser.parse_args()
logger.info(f"BGE_M3服务参数:{args}")

app = Sanic("bge_server")
WorkerManager.THRESHOLD = 6000  # 默认30s，600=60s

device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
logger.info(f"BGE服务，模型环境使用：{device}")

bge_m3_path = args.bge_m3_path
if not bge_m3_path:
    bge_m3_path = os.path.join(os.path.dirname(__file__), "models", "BAAI", "bge-m3")

logger.info(f"向量模型的权重路劲：{bge_m3_path}")
embeddings_model = BGEM3FlagModel(bge_m3_path, devices=[device])
logger.success("向量模型加载完成")

bge_reranker_path = args.bge_reranker_path
if not bge_reranker_path:
    bge_reranker_path = os.path.join(os.path.dirname(__file__), "models", "BAAI", "bge-reranker-v2-m3")
logger.info(f"重排模型的权重路劲：{bge_m3_path}")
reranker_model = FlagAutoReranker.from_finetuned(bge_reranker_path, use_fp16=True, trust_remote_code=True,
                                                 devices=[device])
logger.success("重排模型加载完成")


def safe_get(req: Request, attr: str, default=None):
    # 获取请求参数
    if default is None:
        default = {}
    try:
        if attr in req.form:
            return req.form.getlist(attr)[0]
        if attr in req.args:
            return req.args[attr]
        if attr in req.json:
            return req.json[attr]
    except Exception as e:
        logger.error(f"get {attr} from request failed:{e}")
    return default


@app.post("/bge_m3")
async def bge_m3(request: Request):
    logger.warning(f"bge_m3 worker_id：{os.getpid()}")

    sentences = safe_get(request, 'sentences')  # type:list
    logger.info(f"文本列表：{sentences}")
    return_dense = safe_get(request, 'dense', True)
    logger.info(f"稠密向量：{return_dense}")
    return_sparse = safe_get(request, 'sparse', False)
    logger.info(f"稀疏向量：{return_sparse}")
    return_colbert_vecs = safe_get(request, 'colbert_vecs', False)
    logger.info(f"多向量：{return_colbert_vecs}")

    if not sentences:
        return json({"error": "文本不能为空！"}, status=400)

    try:
        loop = asyncio.get_event_loop()
        embeddings_list = await asyncio.gather(
            loop.run_in_executor(None, functools.partial(embeddings_model.encode, sentences, return_dense=return_dense,
                                                         return_sparse=return_sparse,
                                                         return_colbert_vecs=return_colbert_vecs))
        )
        embeddings = embeddings_list[0]
    except Exception as e:
        return json({"status": "failed", "result": f"向量转换异常：{e}"})

    result = {}
    # 稠密
    if return_dense:
        dense_vecs = embeddings["dense_vecs"]
        dense_shape = dense_vecs.shape
        result["dense_vecs"] = dense_vecs.astype(np.float32).tolist()
        result["dense_shape"] = dense_shape

    # 稀疏
    if return_sparse:
        sparse_list = []
        for sp in embeddings["lexical_weights"]:
            sparse_list.append({int(k): float(v) for k, v in sp.items()})
        result["sparse_vecs"] = sparse_list

    # 多向量
    if return_colbert_vecs:
        result["colbert_vecs"] = [x.astype(np.float32).tolist() for x in embeddings["colbert_vecs"]]

    logger.success("处理完成！！！")
    return json({"status": "success", "result": result})


@app.post("/bge_ranker_v2_m3")
async def bge_reranker(request):
    logger.warning(f"bge_ranker worker_id：{os.getpid()}")
    problem_list = safe_get(request, "problem_list")  # type:list
    batch_size = safe_get(request, "batch_size", 4)
    try:
        loop = asyncio.get_event_loop()
        scores = await asyncio.gather(
            loop.run_in_executor(None, functools.partial(reranker_model.compute_score, problem_list,
                                                         batch_size=batch_size, normalize=True)))
        return json({"status": "success", "result": scores})
    except Exception as e:
        return json({"status": "failed", "result": f"重排异常：{e}"})


if __name__ == '__main__':
    app.run(host=args.host, port=args.port, workers=args.workers, debug=False, single_process=True)
