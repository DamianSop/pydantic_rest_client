# Pydantic REST Client

## Description
Pydantic REST Client is a Python library for simplifying interactions with REST APIs using Pydantic models for request and response data validation.

## Features
- Integration with REST APIs through asynchronous requests.
- Data validation with Pydantic models.
- Simplifies the request and response handling process.

## Installation
Install the library using pip:

```

pip install git+https://github.com/DamianSop/pydantic_rest_client.git

```

## Usage
Here is a simple example of how to use the Pydantic REST Client:
```python
import asyncio

from rest_client import AioHttpRestClient
from pydantic import BaseModel


class GetUserModel(BaseModel):
    id: int
    first_name: str | None


class DataModel(BaseModel):
    data: GetUserModel


class PostUserModel(BaseModel):
    name: str
    job: str
    id: int
    createdAt: str


class ApiExample:
    client = AioHttpRestClient('https://reqres.in/api')

    @client.get_response_model(DataModel)
    def get_user(self, user_id: int):
        return self.client.get(f'/users/{user_id}')

    @client.get_response_model(PostUserModel)
    def post_example(self, name: str, job: str):
        user_dict = {
            'name': name,
            'job': job
        }
        return self.client.post(f'/users', user_dict)


async def main():
    api_example = ApiExample()

    user, status_code = await api_example.get_user(2)
    print(status_code)  # 200
    print(user)  # data=UserModel(id=2, first_name='Janet')

    user, status_code = await api_example.post_example(name='Damian', job='developer')
    print(status_code)  # 201
    print(user)  # name='Damian' job='developer' id=718 createdAt='2024-03-25T13:23:28.625Z'

if __name__ == '__main__':
    asyncio.run(main())
```

## Contributing
We welcome contributions! Feel free to fork the project, make your changes, and submit a pull request.

## License
This project is licensed under the MIT License - see the LICENSE.md file for details.
