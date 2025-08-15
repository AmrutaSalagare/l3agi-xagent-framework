#!/usr/bin/env python3
"""
Test script to verify XAgent integration with L3AGI framework
"""

import os
import sys
import asyncio

# Add XAgent to Python path
xagent_path = os.path.join(os.path.dirname(__file__), '..', '..', 'XAgent')
if xagent_path not in sys.path:
    sys.path.insert(0, xagent_path)

# Add current directory to path for local imports
current_path = os.path.dirname(__file__)
if current_path not in sys.path:
    sys.path.insert(0, current_path)

try:
    from agents.xagent_integration import L3AGIXAgentAdapter
    print("✅ Successfully imported L3AGIXAgentAdapter")
except ImportError as e:
    print(f"❌ Failed to import L3AGIXAgentAdapter: {e}")
    sys.exit(1)


async def test_xagent_basic():
    """Test basic XAgent functionality"""
    print("\n🧪 Testing basic XAgent functionality...")
    
    try:
        # Create XAgent adapter
        adapter = L3AGIXAgentAdapter(
            config={
                "model_name": "gpt-3.5-turbo",
                "temperature": 0.7
            },
            tools=[],
            system_message="You are a helpful assistant. Always respond with 'Hello from XAgent!'",
            memory=None
        )
        
        print("✅ XAgent adapter created successfully")
        
        # Test simple prompt
        test_prompt = "Say hello"
        print(f"📝 Testing prompt: '{test_prompt}'")
        
        response = await adapter.arun(test_prompt)
        print(f"🤖 XAgent response: {response}")
        
        if response and len(response) > 0:
            print("✅ XAgent integration test PASSED")
            return True
        else:
            print("❌ XAgent integration test FAILED - empty response")
            return False
            
    except Exception as e:
        print(f"❌ XAgent integration test FAILED: {e}")
        return False


def test_xagent_sync():
    """Test synchronous XAgent functionality"""
    print("\n🧪 Testing synchronous XAgent functionality...")
    
    try:
        # Create XAgent adapter
        adapter = L3AGIXAgentAdapter(
            config={
                "model_name": "gpt-3.5-turbo",
                "temperature": 0.7
            },
            tools=[],
            system_message="You are a helpful assistant. Always respond with 'Hello from XAgent sync!'",
            memory=None
        )
        
        print("✅ XAgent adapter created successfully")
        
        # Test simple prompt
        test_prompt = "Say hello synchronously"
        print(f"📝 Testing prompt: '{test_prompt}'")
        
        response = adapter.run(test_prompt)
        print(f"🤖 XAgent sync response: {response}")
        
        if response and len(response) > 0:
            print("✅ XAgent sync integration test PASSED")
            return True
        else:
            print("❌ XAgent sync integration test FAILED - empty response")
            return False
            
    except Exception as e:
        print(f"❌ XAgent sync integration test FAILED: {e}")
        return False


async def test_xagent_streaming():
    """Test XAgent streaming functionality"""
    print("\n🧪 Testing XAgent streaming functionality...")
    
    try:
        # Create XAgent adapter
        adapter = L3AGIXAgentAdapter(
            config={
                "model_name": "gpt-3.5-turbo",
                "temperature": 0.7
            },
            tools=[],
            system_message="You are a helpful assistant.",
            memory=None
        )
        
        print("✅ XAgent adapter created successfully")
        
        # Test streaming prompt
        test_prompt = "Count from 1 to 5"
        print(f"📝 Testing streaming prompt: '{test_prompt}'")
        
        streaming_response = []
        async for chunk in adapter.astream(test_prompt):
            if chunk:
                streaming_response.append(chunk)
                print(f"📡 Streamed chunk: {chunk}", end="", flush=True)
        
        full_response = "".join(streaming_response)
        print(f"\n🤖 Full streaming response: {full_response}")
        
        if full_response and len(full_response) > 0:
            print("✅ XAgent streaming test PASSED")
            return True
        else:
            print("❌ XAgent streaming test FAILED - empty response")
            return False
            
    except Exception as e:
        print(f"❌ XAgent streaming test FAILED: {e}")
        return False


def main():
    """Main test function"""
    print("🚀 Starting XAgent Integration Tests for L3AGI Framework")
    print("=" * 60)
    
    # Test results
    results = []
    
    # Test 1: Basic async functionality
    try:
        result = asyncio.run(test_xagent_basic())
        results.append(("Basic Async", result))
    except Exception as e:
        print(f"❌ Basic async test failed to run: {e}")
        results.append(("Basic Async", False))
    
    # Test 2: Synchronous functionality
    try:
        result = test_xagent_sync()
        results.append(("Synchronous", result))
    except Exception as e:
        print(f"❌ Sync test failed to run: {e}")
        results.append(("Synchronous", False))
    
    # Test 3: Streaming functionality
    try:
        result = asyncio.run(test_xagent_streaming())
        results.append(("Streaming", result))
    except Exception as e:
        print(f"❌ Streaming test failed to run: {e}")
        results.append(("Streaming", False))
    
    # Print results summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:<20}: {status}")
        if result:
            passed += 1
    
    print(f"\n📈 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! XAgent integration is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the integration.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
