import pytest
from pydantic import BaseModel

from rest_client import AioHttpRestClient


client = AioHttpRestClient('https://reqres.in/api')


class GetUserExample(BaseModel):
    id: int
    first_name: str | None


class GetDataExample(BaseModel):
    data: GetUserExample


class PostUserExample(BaseModel):
    name: str
    job: str
    id: int
    createdAt: str


class PutUserExample(BaseModel):
    name: str
    job: str
    updatedAt: str


@client.get_response_model(GetDataExample)
def get_example(user_id: int = 2):
    return client.get(f'/users/{user_id}')


@client.get_response_model(GetDataExample)
def get_not_found_example():
    return client.get(f'/unknown/23')


@client.get_response_model()
def delete_example(user_id: int = 2):
    return client.delete(f'/users/{user_id}')


@client.get_response_model(PostUserExample)
def post_example(name: str = 'Damian', job: str = 'developer'):
    user_dict = {
        'name': name,
        'job': job
    }
    return client.post(f'/users', user_dict)


@client.get_response_model(PutUserExample)
def put_example(user_id: int = 2, name: str = 'Damian', job: str = 'developer'):
    user_dict = {
        'name': name,
        'job': job
    }
    return client.put(f'/users/{user_id}', user_dict)


@client.get_response_model(PutUserExample)
def patch_example(user_id: int = 2, name: str = 'Damian', job: str = 'developer'):
    user_dict = {
        'name': name,
        'job': job
    }
    return client.patch(f'/users/{user_id}', user_dict)


@pytest.mark.asyncio
async def test_get_example():
    example_data, status_code = await get_example()
    assert status_code == 200
    assert example_data.data.id == 2


@pytest.mark.asyncio
async def test_get_not_found_example():
    example_data, status_code = await get_not_found_example()
    assert status_code == 404


@pytest.mark.asyncio
async def test_delete_example():
    example_data, status_code = await delete_example()
    assert status_code == 204


@pytest.mark.asyncio
async def test_post_example():
    example_data, status_code = await post_example()
    assert status_code == 201
    assert example_data.name == 'Damian'


@pytest.mark.asyncio
async def test_put_example():
    example_data, status_code = await put_example()
    assert status_code == 200
    assert example_data.name == 'Damian'


@pytest.mark.asyncio
async def test_patch_example():
    example_data, status_code = await patch_example()
    assert status_code == 200
    assert example_data.name == 'Damian'
