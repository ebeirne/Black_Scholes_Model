from fastapi import FastAPI
from pydantic import BaseModel
from src.prediction import predict
from fastapi.middleware.cors import CORSMiddleware

class Query(BaseModel):
    symbol: str
    strike: float
    expiration: str  # "YYYY-MM-DD"
    option_type: int # 1=call, 0=put

app = FastAPI(
    title="BS-ML Option Pricer",
    description="Predict option prices using an ML model trained on S&P 500 data"
)

# if you need CORS for direct frontend calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # you can restrict to your frontend URL
    allow_methods=["POST"],
    allow_headers=["*"],
)

@app.post("/predict")
def get_price(q: Query):
    price = predict(q.symbol, q.strike, q.expiration, q.option_type)
    return {"predicted_price": price}
