#!/usr/bin/env python3
"""
Simple test script for pydantic-rest-client
This script tests basic functionality without complex async test frameworks
"""

import asyncio
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from pydantic_rest_client import AioHttpRestClient
from pydantic_rest_client.exceptions import RestClientError


class SimpleTestRunner:
    """Simple test runner for basic functionality"""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def test(self, name, test_func):
        """Run a test and record results"""
        print(f"\n🧪 Testing: {name}")
        try:
            result = test_func()
            if result:
                print(f"✅ PASS: {name}")
                self.passed += 1
            else:
                print(f"❌ FAIL: {name}")
                self.failed += 1
        except Exception as e:
            print(f"💥 ERROR: {name} - {e}")
            self.errors.append((name, str(e)))
            self.failed += 1
    
    async def async_test(self, name, test_func):
        """Run an async test and record results"""
        print(f"\n🧪 Testing: {name}")
        try:
            result = await test_func()
            if result:
                print(f"✅ PASS: {name}")
                self.passed += 1
            else:
                print(f"❌ FAIL: {name}")
                self.failed += 1
        except Exception as e:
            print(f"💥 ERROR: {name} - {e}")
            self.errors.append((name, str(e)))
            self.failed += 1
    
    def run_sync_tests(self):
        """Run synchronous tests"""
        print("\n" + "="*60)
        print("🔧 Running Synchronous Tests")
        print("="*60)
        
        # Test 1: Client initialization
        self.test("Client initialization", self._test_client_init)
        
        # Test 2: Header merging
        self.test("Header merging", self._test_header_merging)
        
        # Test 3: URL validation
        self.test("URL validation", self._test_url_validation)
    
    async def run_async_tests(self):
        """Run asynchronous tests"""
        print("\n" + "="*60)
        print("⚡ Running Asynchronous Tests")
        print("="*60)
        
        # Test 1: Session management
        await self.async_test("Session management", self._test_session_management)
        
        # Test 2: HTTP methods (mocked)
        await self.async_test("HTTP methods", self._test_http_methods)
        
        # Test 3: Error handling
        await self.async_test("Error handling", self._test_error_handling)
    
    def _test_client_init(self):
        """Test client initialization"""
        try:
            # Test basic initialization
            client = AioHttpRestClient('https://api.example.com')
            assert client.base_url == 'https://api.example.com'
            assert 'Content-Type' in client.headers
            assert client.headers['Content-Type'] == 'application/json'
            
            # Test with custom headers
            custom_headers = {'Authorization': 'Bearer token'}
            client = AioHttpRestClient('https://api.example.com', headers=custom_headers)
            assert client.headers['Authorization'] == 'Bearer token'
            assert client.headers['Content-Type'] == 'application/json'
            
            return True
        except Exception as e:
            print(f"Client init error: {e}")
            return False
    
    def _test_header_merging(self):
        """Test header merging functionality"""
        try:
            client = AioHttpRestClient('https://api.example.com')
            
            # Test without additional headers
            merged = client._merge_headers()
            assert merged == client.headers
            
            # Test with additional headers
            custom_headers = {'X-Custom': 'value'}
            merged = client._merge_headers(custom_headers)
            assert merged['Content-Type'] == 'application/json'
            assert merged['X-Custom'] == 'value'
            
            # Test overriding existing headers
            override_headers = {'Content-Type': 'text/plain'}
            merged = client._merge_headers(override_headers)
            assert merged['Content-Type'] == 'text/plain'
            
            return True
        except Exception as e:
            print(f"Header merging error: {e}")
            return False
    
    def _test_url_validation(self):
        """Test URL validation"""
        try:
            # Test empty URL
            try:
                AioHttpRestClient('')
                return False  # Should have raised ValueError
            except ValueError:
                pass
            
            # Test wrong header type
            try:
                AioHttpRestClient('https://api.example.com', headers=123)  # type: ignore
                return False  # Should have raised TypeError
            except TypeError:
                pass
            
            return True
        except Exception as e:
            print(f"URL validation error: {e}")
            return False
    
    async def _test_session_management(self):
        """Test session management"""
        try:
            client = AioHttpRestClient('https://api.example.com')
            
            # Test session creation
            session = await client._get_session()
            assert session is not None
            assert not session.closed
            
            # Test session reuse
            session2 = await client._get_session()
            assert session is session2
            
            # Test session closing
            await client.close()
            assert session.closed
            assert client._session is None
            
            return True
        except Exception as e:
            print(f"Session management error: {e}")
            # Try to close the client if it exists
            try:
                if hasattr(client, '_session') and client._session:
                    await client.close()
            except:
                pass
            return False
    
    async def _test_http_methods(self):
        """Test HTTP methods with mocking"""
        try:
            from unittest.mock import AsyncMock, patch
            
            client = AioHttpRestClient('https://api.example.com')
            
            # Mock the _make_request method
            with patch.object(client, '_make_request') as mock_make_request:
                mock_make_request.return_value = ({'test': 'data'}, 200)
                
                # Test all HTTP methods
                methods = [
                    ('GET', client.get, '/test'),
                    ('POST', client.post, '/test', {'name': 'test'}),
                    ('PUT', client.put, '/test', {'name': 'test'}),
                    ('PATCH', client.patch, '/test', {'name': 'test'}),
                    ('DELETE', client.delete, '/test'),
                ]
                
                for method_name, method_func, url, *args in methods:
                    result, status = await method_func(url, *args)
                    assert status == 200
                    assert result == {'test': 'data'}
                
                # Verify all methods were called
                assert mock_make_request.call_count == len(methods)
            
            await client.close()
            return True
        except Exception as e:
            print(f"HTTP methods error: {e}")
            return False
    
    async def _test_error_handling(self):
        """Test error handling"""
        try:
            client = AioHttpRestClient('https://api.example.com')
            
            # Test network error handling
            from unittest.mock import AsyncMock, patch
            
            with patch.object(client, '_get_session') as mock_get_session:
                mock_session = AsyncMock()
                mock_session.request.side_effect = Exception("Network error")
                mock_get_session.return_value = mock_session
                
                try:
                    await client._make_request('GET', '/test')
                    return False  # Should have raised an exception
                except RuntimeError as e:
                    assert "Unexpected error during GET request" in str(e)
            
            await client.close()
            return True
        except Exception as e:
            print(f"Error handling test error: {e}")
            return False
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*60)
        print("📊 TEST SUMMARY")
        print("="*60)
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        print(f"💥 Errors: {len(self.errors)}")
        
        if self.errors:
            print("\nError Details:")
            for name, error in self.errors:
                print(f"  - {name}: {error}")
        
        total = self.passed + self.failed
        if total > 0:
            success_rate = (self.passed / total) * 100
            print(f"\nSuccess Rate: {success_rate:.1f}%")
        
        if self.failed == 0:
            print("\n🎉 All tests passed!")
            return True
        else:
            print(f"\n❌ {self.failed} test(s) failed!")
            return False


async def main():
    """Main test function"""
    print("🚀 Starting Simple Test Suite for pydantic-rest-client")
    
    runner = SimpleTestRunner()
    
    # Run synchronous tests
    runner.run_sync_tests()
    
    # Run asynchronous tests
    await runner.run_async_tests()
    
    # Print summary
    success = runner.print_summary()
    
    return 0 if success else 1


if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⏹️  Test run interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 Unexpected error: {e}")
        sys.exit(1) 