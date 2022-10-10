

class BaseEndpoint():

    def __init__(self) -> None:
        pass

    @staticmethod
    def get_endpoint() -> str:
        raise NotImplementedError()
