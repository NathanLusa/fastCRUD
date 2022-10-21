from fastapi import FastAPI

from core.crud_router import CrudRouter, MemCrudRouter  # , AlchemyCrudRouter
from app.database import get_db
from app.product.endpoints import ProductEndpoints
from app.user.endpoints import UserEndpoints


app = FastAPI()

# router = AlchemyCrudRouter(app, db=get_db)
# router.add_class(UserEndpoints)
# router.add_class(ProductEndpoints)

router = MemCrudRouter(app)
router.add_class(UserEndpoints)
router.add_class(ProductEndpoints)


@app.get("/")
def read_root():
    return {"Hello": "World"}
