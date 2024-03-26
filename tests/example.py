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


class PutUserModel(BaseModel):
    name: str
    job: str
    updatedAt: str


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

    @client.get_response_model(DataModel)
    def get_not_found_user(self, user_id: int):
        return self.client.get(f'/unknown/{user_id}')

    # Define a method to delete user data
    @client.get_response_model()
    def delete_user(self, user_id: int = 2):
        return self.client.delete(f'/users/{user_id}')

    # Define a method to put user data
    @client.get_response_model(PutUserModel)
    def put_user(self, user_id: int = 2, name: str = 'Damian', job: str = 'developer'):
        user_dict = {
            'name': name,
            'job': job
        }
        return self.client.put(f'/users/{user_id}', user_dict)

    # Define a method to patch user data
    @client.get_response_model(PutUserModel)
    def patch_user(self, user_id: int = 2, name: str = 'Damian', job: str = 'developer'):
        user_dict = {
            'name': name,
            'job': job
        }
        return self.client.patch(f'/users/{user_id}', user_dict)
