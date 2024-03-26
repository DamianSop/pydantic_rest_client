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


# Define Pydantic models for data validation
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


# Create an API client using AioHttpRestClient
class ApiExample:
    client = AioHttpRestClient('https://reqres.in/api')

    # Define a method to get user data
    @client.get_response_model(DataModel)
    def get_user(self, user_id: int):
        return self.client.get(f'/users/{user_id}')

    # Define a method to post user data
    @client.get_response_model(PostUserModel)
    def post_user(self, name: str, job: str):
        user_dict = {
            'name': name,
            'job': job
        }
        return self.client.post(f'/users', user_dict)


async def main():
    api_example = ApiExample()

    # Get user data for user with ID 2
    user, status_code = await api_example.get_user(2)
    print(status_code)  # Output: 200
    print(user)  # Output: data=UserModel(id=2, first_name='Janet')

    # Post user data
    user, status_code = await api_example.post_user(name='Damian', job='developer')
    print(status_code)  # Output: 201
    print(user)  # Output: name='Damian' job='developer' id=718 createdAt='2024-03-25T13:23:28.625Z'


if __name__ == '__main__':
    asyncio.run(main())
```

## Contributing
We welcome contributions! Feel free to fork the project, make your changes, and submit a pull request.

## License
This project is licensed under the MIT License - see the LICENSE.md file for details.
