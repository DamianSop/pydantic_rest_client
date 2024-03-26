import pytest
from .example import ApiExample

api_example = ApiExample()


@pytest.mark.asyncio
async def test_get_example():
    example_data, status_code = await api_example.get_user(2)
    assert status_code == 200
    assert example_data.data.id == 2


@pytest.mark.asyncio
async def test_get_not_found_example():
    example_data, status_code = await api_example.get_not_found_user(23)
    assert status_code == 404


@pytest.mark.asyncio
async def test_delete_example():
    example_data, status_code = await api_example.delete_user()
    assert status_code == 204


@pytest.mark.asyncio
async def test_post_example():
    example_data, status_code = await api_example.post_user(name='Damian', job='developer')
    assert status_code == 201
    assert example_data.name == 'Damian'


@pytest.mark.asyncio
async def test_put_example():
    example_data, status_code = await api_example.put_user()
    assert status_code == 200
    assert example_data.name == 'Damian'


@pytest.mark.asyncio
async def test_patch_example():
    example_data, status_code = await api_example.patch_user()
    assert status_code == 200
    assert example_data.name == 'Damian'
