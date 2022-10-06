from fastapi import FastAPI

from core.utils import add_routes


app = FastAPI()

add_routes(app)


@app.get("/")
def read_root():
    return {"Hello": "World"}
