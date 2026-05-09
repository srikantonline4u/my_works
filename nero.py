from fastapi import FastAPI
from model import Products
app = FastAPI()

products = [
    {"id": 1, "name": "Widget"},
]
@app.get("/product")
def get_product():
    return products
    