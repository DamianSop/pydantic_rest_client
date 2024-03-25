from typing import Type

from pydantic import BaseModel


class RestClient:
    headers = {'Content-Type': 'application/json'}

    def __init__(self, base_url: str, headers: dict | None = None, raise_for_status: bool = False):
        self.base_url = base_url
        self.raise_for_status = raise_for_status
        if headers:
            self.headers = headers

    @staticmethod
    def get_response_model(base_model: Type[BaseModel] | None = None):
        def decorator(func):
            async def wrapper(*args, **kwargs):
                json_data, status = await func(*args, **kwargs)
                is_received = status in (200, 201)

                if base_model is None:
                    return None, status
                elif issubclass(base_model, BaseModel) and is_received:
                    return base_model(**json_data), status
                elif isinstance(json_data, list) and is_received:
                    return [base_model(**i) for i in json_data]
                else:
                    return json_data, status

            return wrapper

        return decorator
