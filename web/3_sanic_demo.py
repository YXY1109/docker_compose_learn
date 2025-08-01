from sanic import Sanic, json

app = Sanic("demo")


@app.get("/api")
async def hello(request):
    return json({"msg": "Hello, Sanic!"})


@app.post("/api/add")
async def add(request):
    try:
        data = request.json
        a = float(data["a"])
        b = float(data["b"])
    except (KeyError, ValueError, TypeError):
        return json({"error": "Invalid JSON, need {a:number, b:number}"}, status=400)

    return json({"result": a + b})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8011, debug=True, auto_reload=True)
