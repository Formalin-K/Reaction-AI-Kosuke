from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from predict_utils import load_prediction_model, predict_product

app = FastAPI()

# CORS（ローカルHTMLからアクセスできるようにする）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 必要に応じて制限してもOK
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 入力の形式
class PredictRequest(BaseModel):
    input: str

# モデル読み込み（起動時に一度だけ）
model, vocab_data = load_prediction_model("./")

@app.post("/predict")
def predict(request: PredictRequest):
    result = predict_product(request.input, model, vocab_data)
    return {"output": result}
