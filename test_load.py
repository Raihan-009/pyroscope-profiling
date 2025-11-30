"""
Load testing script to generate traffic for Pyroscope profiling.
This script creates various types of load to test the profiling capabilities.
"""
import asyncio
import aiohttp
import random
import time
from typing import List

BASE_URL = "http://localhost:8000"


async def create_user(session: aiohttp.ClientSession, user_id: int) -> dict:
    """Create a new user"""
    data = {
        "email": f"user{user_id}@example.com",
        "full_name": f"User {user_id}",
        "is_active": True
    }
    async with session.post(f"{BASE_URL}/users/", json=data) as response:
        return await response.json()


async def get_users(session: aiohttp.ClientSession, skip: int = 0, limit: int = 100) -> dict:
    """Get list of users"""
    async with session.get(f"{BASE_URL}/users/?skip={skip}&limit={limit}") as response:
        return await response.json()


async def get_user_by_id(session: aiohttp.ClientSession, user_id: int) -> dict:
    """Get a specific user"""
    async with session.get(f"{BASE_URL}/users/{user_id}") as response:
        return await response.json()


async def create_post(session: aiohttp.ClientSession, user_id: int, post_id: int) -> dict:
    """Create a post for a user"""
    data = {
        "title": f"Post {post_id} by User {user_id}",
        "content": f"This is the content of post {post_id}. " * 10,
        "is_published": True
    }
    async with session.post(f"{BASE_URL}/users/{user_id}/posts/", json=data) as response:
        return await response.json()


async def compute_fibonacci(session: aiohttp.ClientSession, n: int) -> dict:
    """Trigger CPU-intensive Fibonacci computation"""
    async with session.get(f"{BASE_URL}/compute/fibonacci/{n}") as response:
        return await response.json()


async def compute_sum(session: aiohttp.ClientSession, n: int) -> dict:
    """Trigger CPU-intensive sum computation"""
    async with session.get(f"{BASE_URL}/compute/sum/{n}") as response:
        return await response.json()


async def health_check(session: aiohttp.ClientSession) -> dict:
    """Health check"""
    async with session.get(f"{BASE_URL}/health") as response:
        return await response.json()


async def run_user_operations(session: aiohttp.ClientSession, num_operations: int):
    """Run various user operations"""
    tasks = []
    for i in range(num_operations):
        # Create users
        tasks.append(create_user(session, i))
        # Get users
        if i % 5 == 0:
            tasks.append(get_users(session, skip=0, limit=10))
    await asyncio.gather(*tasks, return_exceptions=True)


async def run_cpu_intensive_operations(session: aiohttp.ClientSession, num_operations: int):
    """Run CPU-intensive operations for profiling"""
    tasks = []
    for i in range(num_operations):
        # Fibonacci computation (CPU intensive)
        n = random.randint(30, 35)
        tasks.append(compute_fibonacci(session, n))
        
        # Sum computation (CPU intensive)
        if i % 2 == 0:
            n = random.randint(1000000, 5000000)
            tasks.append(compute_sum(session, n))
    
    await asyncio.gather(*tasks, return_exceptions=True)


async def run_mixed_load(session: aiohttp.ClientSession, duration: int):
    """Run mixed load for specified duration"""
    start_time = time.time()
    operation_count = 0
    
    while time.time() - start_time < duration:
        tasks = []
        
        # Health checks
        tasks.append(health_check(session))
        
        # User operations
        if operation_count % 3 == 0:
            tasks.append(get_users(session, skip=0, limit=20))
        
        # CPU intensive operations
        if operation_count % 5 == 0:
            tasks.append(compute_fibonacci(session, random.randint(25, 30)))
        
        await asyncio.gather(*tasks, return_exceptions=True)
        operation_count += 1
        
        # Small delay to avoid overwhelming
        await asyncio.sleep(0.1)
    
    print(f"Completed {operation_count} operation cycles in {duration} seconds")


async def main():
    """Main function to run load tests"""
    print("Starting load testing for Pyroscope profiling...")
    print("=" * 60)
    
    async with aiohttp.ClientSession() as session:
        # Test health endpoint first
        print("\n1. Testing health endpoint...")
        try:
            health = await health_check(session)
            print(f"   ✓ Health check: {health}")
        except Exception as e:
            print(f"   ✗ Health check failed: {e}")
            return
        
        # Create some initial users
        print("\n2. Creating initial users...")
        try:
            user_tasks = [create_user(session, i) for i in range(10)]
            users = await asyncio.gather(*user_tasks, return_exceptions=True)
            print(f"   ✓ Created {len([u for u in users if not isinstance(u, Exception)])} users")
        except Exception as e:
            print(f"   ⚠ User creation had errors: {e}")
        
        # Create posts for users
        print("\n3. Creating posts...")
        try:
            post_tasks = [create_post(session, user_id=i % 5 + 1, post_id=i) for i in range(20)]
            posts = await asyncio.gather(*post_tasks, return_exceptions=True)
            print(f"   ✓ Created {len([p for p in posts if not isinstance(p, Exception)])} posts")
        except Exception as e:
            print(f"   ⚠ Post creation had errors: {e}")
        
        # Run CPU-intensive operations
        print("\n4. Running CPU-intensive operations (this will take a while)...")
        start = time.time()
        await run_cpu_intensive_operations(session, num_operations=20)
        elapsed = time.time() - start
        print(f"   ✓ Completed CPU-intensive operations in {elapsed:.2f} seconds")
        
        # Run mixed continuous load
        print("\n5. Running mixed continuous load for 60 seconds...")
        print("   (This generates realistic traffic patterns for profiling)")
        await run_mixed_load(session, duration=60)
        
        print("\n" + "=" * 60)
        print("Load testing completed!")
        print("\nNext steps:")
        print("1. Open Pyroscope UI at http://localhost:4040")
        print("2. Select 'fastapi-app' from the application dropdown")
        print("3. Explore the profiling data and flame graphs")
        print("4. Try different queries and time ranges")


if __name__ == "__main__":
    print("Load Testing Script for FastAPI Pyroscope Profiling")
    print("Make sure the FastAPI app is running on http://localhost:8000")
    print("Press Ctrl+C to stop early\n")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nLoad testing interrupted by user")
    except Exception as e:
        print(f"\n\nError during load testing: {e}")

