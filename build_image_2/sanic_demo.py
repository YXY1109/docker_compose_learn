from loguru import logger
from sanic import Sanic, json

app = Sanic("demo")


@app.get("/api")
async def hello(request):
    logger.info(f"api接口")
    return json({"msg": "Hello, Sanic!2"})


@app.post("/api/add")
async def add(request):
    logger.info(f"api-add接口")
    try:
        data = request.json
        a = float(data["a"])
        b = float(data["b"])
    except (KeyError, ValueError, TypeError):
        return json({"error": "Invalid JSON, need {a:number, b:number}"}, status=400)

    return json({"result": a + b})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8012, debug=True, auto_reload=True)
