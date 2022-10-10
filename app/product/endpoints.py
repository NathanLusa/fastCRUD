from core.endpoints import BaseEndpoint


class ProductEndpoints(BaseEndpoint):

    @staticmethod
    def create() -> str:
        return ProductEndpoints.create.__module__

    @staticmethod
    def get_endpoint() -> str:
        return 'product'
