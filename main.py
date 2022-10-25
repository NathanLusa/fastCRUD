from typing import Dict, Any

from fastapi import FastAPI

# , MemCrudRouter
from core.crud_router import CrudRouter, AlchemyCrudRouter
from app.database import get_db
from app.product.endpoints import ProductEndpoints
from app.user.endpoints import UserEndpoints


app = FastAPI()

router = AlchemyCrudRouter(app, db=get_db)
router.add_class(UserEndpoints)
# router.add_class(ProductEndpoints)

# router = MemCrudRouter(app)
# router.add_class(UserEndpoints)
# router.add_class(ProductEndpoints)


@app.get("/")
def read_root() -> Dict[Any, Any]:
    return {"Hello": "World"}
