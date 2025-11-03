from typing import List, Any

from fastapi import FastAPI
from paddleocr import PPStructureV3
from pydantic import BaseModel

app = FastAPI()

# Initialize PP-StructureV3 pipeline
# http://www.paddleocr.ai/main/version3.x/pipeline_usage/PP-StructureV3.html#2
pipeline = PPStructureV3(
    lang="en",
    use_doc_orientation_classify=True,
    use_doc_unwarping=True,
    use_textline_orientation=True,
    device="cpu"
)



@app.get("/")
async def root():
    return {"message": "PP-StructureV3 Document Analysis API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/analyze")
async def analyze_document(
        image_url: str = "https://paddle-model-ecology.bj.bcebos.com/paddlex/imgs/demo_image/pp_structure_v3_demo.png"):
    """
    Analyze document using PP-StructureV3 pipeline

    Args:
        image_url: URL of the image to analyze

    Returns:
        Structured analysis results
    """
    try:
        print(f"image_url:{image_url}")
        output = pipeline.predict(image_url)
        print(f"output:{output}")
        return {"code": 200, "msg": "success", "result": "good"}

    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)
