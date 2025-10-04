from typing import Any, Dict, List, Tuple

import numpy as np
import requests
from loguru import logger


def model_embedding_bgem3(input_words: List[str] | str) -> Dict[str, Any]:
    if isinstance(input_words, str):
        input_words = [input_words]

    input_words = [s.strip() for s in input_words if s.strip()]
    if not input_words:
        return {"dense_vecs": [], "sparse_vecs": [], "colbert_vecs": []}

    try:
        embedding_url = "http://127.0.0.1:8010/bge_m3"
        payload = {
            "sentences": input_words,
            "dense": True,
            "sparse": True,
            "colbert_vecs": True
        }
        timeout = max(10, len(input_words))
        resp = requests.post(embedding_url, json=payload, timeout=timeout)
        resp.raise_for_status()

        data = resp.json()["result"]
        return {
            "dense_vecs": np.array(data["dense_vecs"], dtype=np.float32),
            "dense_shape": data["dense_shape"],
            "sparse_vecs": [{int(k): float(v) for k, v in sp.items()}
                            for sp in data["sparse_vecs"]],
            "colbert_vecs": [np.array(m, dtype=np.float32)
                             for m in data["colbert_vecs"]]
        }
    except Exception as e:
        logger.exception(f"向量接口异常：{e}")
        return {}


def reranker_problem(query: str, recall_query: List[str]) -> Tuple[str, List[Tuple[str, float]]]:
    """
    重排接口
    :param query: 用户问题
    :param recall_query: 召回文档列表
    :return:
    """
    if not recall_query:
        return "", []

    logger.info(f"重排问题：{query} | 召回条数：{len(recall_query)}")
    pairs = [[query, doc] for doc in recall_query]
    try:
        ranker_url = "http://127.0.0.1:8010/bge_ranker_v2_m3"
        resp = requests.post(
            ranker_url,
            headers={"Content-Type": "application/json"},
            json={"problem_list": pairs, "batch_size": len(recall_query)},
            timeout=60
        )
        resp.raise_for_status()
        scores = resp.json().get("result", [[]])[0]
        if not scores:
            return "", []

        # 按分数降序排序
        ranked = sorted(zip(recall_query, scores), key=lambda x: x[1], reverse=True)
        best_text, best_score = ranked[0]
        logger.info(f"最高分：{best_score:.4f} | 文本：{best_text}")
        return best_text, ranked

    except Exception as e:
        logger.exception(f"重排接口异常:{e}")
        return "", []


if __name__ == '__main__':
    question = "我是中国人"

    input_word = ["你好", "我好", "在一起", "中国人很强大", "生为中国人很自豪"]
    result_embedding = model_embedding_bgem3(input_word)
    print(result_embedding)

    result_reranker = reranker_problem(question, input_word)
    print(result_reranker)
