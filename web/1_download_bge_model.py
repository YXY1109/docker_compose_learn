from modelscope import snapshot_download

# https://modelscope.cn/models/BAAI/bge-reranker-v2-m3
reranker_dir = snapshot_download('BAAI/bge-reranker-v2-m3', cache_dir='./models')
print(f"reranker_dir: {reranker_dir}")

# 模型下载
# https://modelscope.cn/models/BAAI/bge-m3
m3_dir = snapshot_download('BAAI/bge-m3', cache_dir='./models')
print(f"m3_dir: {m3_dir}")
