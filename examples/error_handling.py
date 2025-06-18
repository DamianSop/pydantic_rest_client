"""
Error handling examples in pydantic_rest_client

This file demonstrates various ways to handle errors
when working with REST APIs through pydantic_rest_client.
"""

import asyncio
from rest_client import AioHttpRestClient, NetworkError, ResponseError, ValidationError
from pydantic import BaseModel


class UserModel(BaseModel):
    id: int
    name: str
    email: str


class ApiClient:
    def __init__(self):
        self.client = AioHttpRestClient('https://reqres.in/api')

    async def get_user_safe(self, user_id: int):
        """
        Safe GET request with error handling
        """
        try:
            result, status = await self.client.get(f'/users/{user_id}')
            
            if status == 404:
                print(f"User with ID {user_id} not found")
                return None, status
            elif status >= 400:
                raise ResponseError(f"Server error: {status}", status, result)
            
            return result, status
            
        except NetworkError as e:
            print(f"Network error: {e}")
            return None, None
        except ResponseError as e:
            print(f"Response error: {e} (status: {e.status_code})")
            return None, e.status_code
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None, None

    async def create_user_safe(self, name: str, job: str):
        """
        Safe POST request with validation
        """
        try:
            user_data = {'name': name, 'job': job}
            result, status = await self.client.post('/users', user_data)
            
            if status == 201:
                # Try to validate response
                try:
                    user = UserModel(**result)
                    print(f"Created user: {user.name} ({user.email})")
                    return user, status
                except Exception as validation_error:
                    print(f"Response validation error: {validation_error}")
                    return result, status
            else:
                raise ResponseError(f"User creation error: {status}", status, result)
                
        except NetworkError as e:
            print(f"Network error during user creation: {e}")
            return None, None
        except ResponseError as e:
            print(f"Response error during user creation: {e}")
            return None, e.status_code
        except Exception as e:
            print(f"Unexpected error during user creation: {e}")
            return None, None

    async def update_user_safe(self, user_id: int, name: str, job: str):
        """
        Safe PUT request with retry logic
        """
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                user_data = {'name': name, 'job': job}
                result, status = await self.client.put(f'/users/{user_id}', user_data)
                
                if status == 200:
                    print(f"User {user_id} updated successfully")
                    return result, status
                elif status == 404:
                    print(f"User {user_id} not found")
                    return None, status
                elif status >= 500:
                    # Server error - try to retry
                    retry_count += 1
                    if retry_count < max_retries:
                        print(f"Server error {status}, retry {retry_count}/{max_retries}")
                        await asyncio.sleep(1)  # Wait 1 second before retry
                        continue
                    else:
                        raise ResponseError(f"Exceeded retry attempts, last status: {status}", status, result)
                else:
                    raise ResponseError(f"User update error: {status}", status, result)
                    
            except NetworkError as e:
                retry_count += 1
                if retry_count < max_retries:
                    print(f"Network error, retry {retry_count}/{max_retries}: {e}")
                    await asyncio.sleep(1)
                    continue
                else:
                    print(f"Exceeded retry attempts due to network errors: {e}")
                    return None, None
            except Exception as e:
                print(f"Unexpected error during user update: {e}")
                return None, None
        
        return None, None

    async def delete_user_safe(self, user_id: int):
        """
        Safe DELETE request
        """
        try:
            result, status = await self.client.delete(f'/users/{user_id}')
            
            if status == 204:
                print(f"User {user_id} deleted successfully")
                return True, status
            elif status == 404:
                print(f"User {user_id} not found for deletion")
                return False, status
            else:
                raise ResponseError(f"User deletion error: {status}", status, result)
                
        except NetworkError as e:
            print(f"Network error during user deletion: {e}")
            return False, None
        except ResponseError as e:
            print(f"Response error during user deletion: {e}")
            return False, e.status_code
        except Exception as e:
            print(f"Unexpected error during user deletion: {e}")
            return False, None


async def main():
    """Error handling demonstration"""
    api = ApiClient()
    
    print("=== Error Handling Demo ===\n")
    
    # Test GET request with non-existent user
    print("1. GET request for non-existent user:")
    result, status = await api.get_user_safe(999)
    print(f"Result: {result}, Status: {status}\n")
    
    # Test GET request with existing user
    print("2. GET request for existing user:")
    result, status = await api.get_user_safe(1)
    print(f"Result: {result}, Status: {status}\n")
    
    # Test user creation
    print("3. User creation:")
    result, status = await api.create_user_safe("John Doe", "Developer")
    print(f"Result: {result}, Status: {status}\n")
    
    # Test user update
    print("4. User update:")
    result, status = await api.update_user_safe(2, "Jane Smith", "Designer")
    print(f"Result: {result}, Status: {status}\n")
    
    # Test user deletion
    print("5. User deletion:")
    result, status = await api.delete_user_safe(2)
    print(f"Result: {result}, Status: {status}\n")
    
    # Close client
    await api.client.close()


if __name__ == "__main__":
    asyncio.run(main()) 