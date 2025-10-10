from datetime import datetime

from sanic import Sanic
from sanic.response import json

app = Sanic(__name__)


@app.get("/")
async def index(request):
    # 获取当前时间的年月日时分秒
    formatted_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return json({"message": f"4Hello from Sanic on K8s!：{formatted_time}"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
