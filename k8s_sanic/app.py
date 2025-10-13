from datetime import datetime

from sanic import Sanic
from sanic.response import json

app = Sanic(__name__)


@app.get("/")
async def index(request):
    # 获取当前时间的年月日时分秒
    formatted_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return json({"message": f"22Hello from Sanic on K8s!：{formatted_time}"})


@app.get("/health")
async def health_check(request):
    return json({"status": "ok"})


if __name__ == "__main__":
    print("启动服务")
    app.run(host="0.0.0.0", port=8000, workers=4, debug=False)
