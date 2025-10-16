from datetime import datetime

from sanic import Sanic
from sanic.response import json
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Sanic(__name__)

# 配置Sanic
app.config.ACCESS_LOG = True
app.config.KEEP_ALIVE_TIMEOUT = 75  # 设置keep-alive超时
app.config.REQUEST_TIMEOUT = 60  # 设置请求超时
app.config.RESPONSE_TIMEOUT = 60  # 设置响应超时


@app.get("/")
async def index(request):
    # 获取当前时间的年月日时分秒
    formatted_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logger.info(f"Request received at {formatted_time}")
    return json({"message": f"32Hello from Sanic on K8s!：{formatted_time}"})


@app.get("/health")
async def health_check(request):
    return json({"status": "ok"}, status=200)


# 添加中间件用于请求日志
@app.middleware("request")
async def add_request_id(request):
    request.ctx.request_id = request.id
    logger.info(f"Request {request.id} started: {request.method} {request.path}")


@app.middleware("response")
async def log_response(request, response):
    logger.info(f"Request {request.ctx.request_id} completed with status {response.status}")


if __name__ == "__main__":
    print("启动服务")
    # 在K8s环境中，不使用workers模式，避免进程管理问题
    app.run(host="0.0.0.0", port=8000, workers=1, debug=False, access_log=True)
