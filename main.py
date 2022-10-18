from fastapi import FastAPI

from core.crud_router import CrudRouter, MemCrudRouter, AlchemyCrudRouter
from app.product.endpoints import ProductEndpoints
from app.user.endpoints import UserEndpoints


app = FastAPI()

# add_routes(app)

router = MemCrudRouter(app)
router.add_class(UserEndpoints)
router.add_class(ProductEndpoints)
# router.get_methods()


@app.get("/")
def read_root():
    return {"Hello": "World"}
