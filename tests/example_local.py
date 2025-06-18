#!/usr/bin/env python3
"""
Example usage of pydantic-rest-client with local test API
This example works with the test_api.py FastAPI server
"""

import asyncio
from pydantic import BaseModel
from rest_client import AioHttpRestClient, validate_response


# Pydantic models for our test API
class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    avatar: str


class UserResponse(BaseModel):
    data: User


class CreateUserRequest(BaseModel):
    name: str
    job: str


class CreateUserResponse(BaseModel):
    name: str
    job: str
    id: str
    created_at: str


class ApiExampleLocal:
    """Example class for working with local test API"""
    
    def __init__(self):
        # Initialize client with local test API
        self.client = AioHttpRestClient(
            base_url='http://localhost:8000',
            headers={'X-API-Version': '1.0'}
        )
    
    @validate_response(UserResponse)
    async def get_user(self, user_id: int):
        """Get user by ID"""
        return await self.client.get(f'/users/{user_id}')
    
    @validate_response()
    async def get_not_found_user(self, user_id: int):
        """Get non-existent user (should return 404)"""
        return await self.client.get(f'/users/{user_id}')
    
    @validate_response()
    async def delete_user(self, user_id: str = "test-user"):
        """Delete user (should return 204)"""
        return await self.client.delete(f'/users/{user_id}')
    
    @validate_response(CreateUserResponse)
    async def post_user(self, name: str, job: str):
        """Create a new user"""
        data = {'name': name, 'job': job}
        return await self.client.post('/users', data=data)
    
    @validate_response(CreateUserResponse)
    async def put_user(self, user_id: str = "test-user", name: str = "Damian", job: str = "developer"):
        """Update user"""
        data = {'name': name, 'job': job}
        return await self.client.put(f'/users/{user_id}', data=data)
    
    @validate_response(CreateUserResponse)
    async def patch_user(self, user_id: str = "test-user", name: str = "Damian", job: str = "developer"):
        """Partially update user"""
        data = {'name': name, 'job': job}
        return await self.client.patch(f'/users/{user_id}', data=data)
    
    @validate_response(UserResponse)
    async def get_user_with_headers(self, user_id: int, headers: dict):
        """Get user with custom headers"""
        return await self.client.get(f'/users/{user_id}', headers=headers)
    
    @validate_response(CreateUserResponse)
    async def post_user_with_headers(self, name: str, job: str, headers: dict):
        """Create user with custom headers"""
        data = {'name': name, 'job': job}
        return await self.client.post('/users', data=data, headers=headers)
    
    @validate_response()
    async def test_headers(self, headers: dict):
        """Test custom headers"""
        return await self.client.get('/headers', headers=headers)
    
    @validate_response()
    async def test_echo(self, data: dict, headers: dict | None = None):
        """Test echo endpoint"""
        return await self.client.post('/echo', data=data, headers=headers)
    
    @validate_response()
    async def test_error_endpoints(self):
        """Test various error endpoints"""
        results = {}
        
        # Test 404
        try:
            results['404'] = await self.client.get('/not-found')
        except Exception as e:
            results['404'] = str(e)
        
        # Test 401
        try:
            results['401'] = await self.client.get('/unauthorized')
        except Exception as e:
            results['401'] = str(e)
        
        # Test 403
        try:
            results['403'] = await self.client.get('/forbidden')
        except Exception as e:
            results['403'] = str(e)
        
        # Test 500
        try:
            results['500'] = await self.client.get('/server-error')
        except Exception as e:
            results['500'] = str(e)
        
        return results


async def demo_local_api():
    """Demo of working with local test API"""
    api = ApiExampleLocal()
    
    print("=== Local Test API Demo ===")
    
    try:
        # Test GET request
        print("\n1. GET user by ID:")
        result, status = await api.get_user(1)
        print(f"Status: {status}")
        if result:
            print(f"User: {result.data.first_name} {result.data.last_name}")
        
        # Test POST request
        print("\n2. Create new user:")
        result, status = await api.post_user("John Doe", "Software Engineer")
        print(f"Status: {status}")
        if result:
            print(f"Created user: {result.name} - {result.job}")
            user_id = result.id
        
        # Test PUT request
        print("\n3. Update user:")
        result, status = await api.put_user(user_id, "John Updated", "Senior Developer")
        print(f"Status: {status}")
        if result:
            print(f"Updated user: {result.name} - {result.job}")
        
        # Test PATCH request
        print("\n4. Partially update user:")
        result, status = await api.patch_user(user_id, job="Tech Lead")
        print(f"Status: {status}")
        if result:
            print(f"Patched user: {result.name} - {result.job}")
        
        # Test custom headers
        print("\n5. Test custom headers:")
        result, status = await api.test_headers({
            'X-Custom-Header': 'test-value',
            'Authorization': 'Bearer my-token'
        })
        print(f"Status: {status}")
        if result:
            print("Headers received successfully")
        
        # Test echo endpoint
        print("\n6. Test echo endpoint:")
        result, status = await api.test_echo(
            {'message': 'Hello, API!'},
            {'X-Request-ID': 'test-123'}
        )
        print(f"Status: {status}")
        if result:
            print(f"Echo response: {result.get('body', 'No body')}")
        
        # Test error endpoints
        print("\n7. Test error endpoints:")
        errors = await api.test_error_endpoints()
        for status_code, error in errors.items():
            print(f"  {status_code}: {error}")
        
        # Test DELETE request
        print("\n8. Delete user:")
        result, status = await api.delete_user(user_id)
        print(f"Status: {status}")
        print("User deleted successfully")
        
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        # Clean up
        await api.client.close()


if __name__ == "__main__":
    print("🚀 Starting Local API Demo")
    print("⚠️  Make sure test_api.py is running on http://localhost:8000")
    print("   Run: python test_api.py")
    print()
    
    asyncio.run(demo_local_api()) 