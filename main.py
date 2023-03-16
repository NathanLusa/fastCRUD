from typing import Any, Dict

from fastapi import FastAPI

from app.database import BaseDeclarativeList, engine, get_db
from app.endpoints.account import AccountEndpoints
from app.endpoints.product import ProductEndpoints
from app.endpoints.user import UserEndpoints
from core.crud_router import AlchemyCrudRouter, CrudRouter, MemCrudRouter

app = FastAPI()

router = AlchemyCrudRouter(app, db=get_db)
router.add_endpoint(UserEndpoints())
router.add_endpoint(AccountEndpoints())
# router.add_endpoint(ProductEndpoints())

# router = MemCrudRouter(app)
# router.add_endpoint(UserEndpoints())
# router.add_endpoint(ProductEndpoints())

for base_declarative in BaseDeclarativeList:
    base_declarative.metadata.create_all(bind=engine)


@app.get('/')
def read_root() -> Dict[Any, Any]:
    return {'Hello': 'World'}
