from fastapi import FastAPI

from core.utils import CrudRouter
from app.product.endpoints import ProductEndpoints
from app.user.endpoints import UserEndpoints


app = FastAPI()

# add_routes(app)

router = CrudRouter(app)
router.add_class(UserEndpoints)
# router.add_class(ProductEndpoints)
# router.get_methods()


@app.get("/")
def read_root():
    return {"Hello": "World"}
