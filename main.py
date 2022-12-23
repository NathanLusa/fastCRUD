from typing import Dict, Any

from fastapi import FastAPI

from core.crud_router import CrudRouter, AlchemyCrudRouter, MemCrudRouter
from app.database import get_db, Base, engine
from app.endpoints.product import ProductEndpoints
from app.endpoints.user import UserEndpoints


app = FastAPI()

router = AlchemyCrudRouter(app, db=get_db)
router.add_class(UserEndpoints)
# router.add_class(ProductEndpoints)

# router = MemCrudRouter(app)
# router.add_class(UserEndpoints)
# router.add_class(ProductEndpoints)

Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root() -> Dict[Any, Any]:
    return {"Hello": "World"}
