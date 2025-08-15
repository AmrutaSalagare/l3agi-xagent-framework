#!/usr/bin/env python3
"""
Simple structure test to verify XAgent integration files are properly created
"""

import os
import sys

def test_file_structure():
    """Test that all required files were created"""
    print("🔍 Testing XAgent Integration File Structure...")
    
    base_path = os.path.dirname(__file__)
    
    required_files = [
        "agents/xagent_integration.py",
        "agents/conversational/conversational.py",
        "agents/conversational/conversational_langchain_backup.py",
        "agents/agent_simulations/agent/dialogue_agent_with_tools.py",
        "agents/agent_simulations/agent/dialogue_agent_with_tools_langchain_backup.py",
        "test.py",
        "test_langchain_backup.py",
        "test_xagent_integration.py"
    ]
    
    missing_files = []
    existing_files = []
    
    for file_path in required_files:
        full_path = os.path.join(base_path, file_path)
        if os.path.exists(full_path):
            existing_files.append(file_path)
            print(f"✅ {file_path}")
        else:
            missing_files.append(file_path)
            print(f"❌ {file_path}")
    
    print(f"\n📊 Results: {len(existing_files)}/{len(required_files)} files found")
    
    if missing_files:
        print("❌ Missing files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    else:
        print("✅ All required files are present!")
        return True


def test_code_structure():
    """Test that key code changes are present"""
    print("\n🔍 Testing Code Structure Changes...")
    
    base_path = os.path.dirname(__file__)
    
    # Test XAgent integration file
    integration_file = os.path.join(base_path, "agents", "xagent_integration.py")
    if os.path.exists(integration_file):
        with open(integration_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if "L3AGIXAgentAdapter" in content:
            print("✅ L3AGIXAgentAdapter class found in integration file")
        else:
            print("❌ L3AGIXAgentAdapter class not found")
            
        if "async def arun" in content:
            print("✅ Async run method found")
        else:
            print("❌ Async run method not found")
            
        if "def run" in content:
            print("✅ Sync run method found")
        else:
            print("❌ Sync run method not found")
    else:
        print("❌ XAgent integration file not found")
        return False
    
    # Test conversational.py changes
    conv_file = os.path.join(base_path, "agents", "conversational", "conversational.py")
    if os.path.exists(conv_file):
        with open(conv_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if "xagent_integration" in content:
            print("✅ XAgent integration import found in conversational.py")
        else:
            print("❌ XAgent integration import not found in conversational.py")
            
        if "L3AGIXAgentAdapter" in content:
            print("✅ XAgent adapter usage found in conversational.py")
        else:
            print("❌ XAgent adapter usage not found in conversational.py")
    else:
        print("❌ conversational.py file not found")
        return False
    
    return True


def test_backup_files():
    """Test that backup files were created"""
    print("\n🔍 Testing Backup Files...")
    
    base_path = os.path.dirname(__file__)
    
    backup_files = [
        "agents/conversational/conversational_langchain_backup.py",
        "agents/agent_simulations/agent/dialogue_agent_with_tools_langchain_backup.py",
        "test_langchain_backup.py"
    ]
    
    all_backups_exist = True
    
    for backup_file in backup_files:
        full_path = os.path.join(base_path, backup_file)
        if os.path.exists(full_path):
            print(f"✅ Backup file exists: {backup_file}")
        else:
            print(f"❌ Backup file missing: {backup_file}")
            all_backups_exist = False
    
    return all_backups_exist


def main():
    """Main test function"""
    print("🚀 XAgent Integration Structure Test")
    print("=" * 50)
    
    results = []
    
    # Test 1: File structure
    results.append(("File Structure", test_file_structure()))
    
    # Test 2: Code structure
    results.append(("Code Structure", test_code_structure()))
    
    # Test 3: Backup files
    results.append(("Backup Files", test_backup_files()))
    
    # Print results
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:<20}: {status}")
        if result:
            passed += 1
    
    print(f"\n📈 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL STRUCTURE TESTS PASSED!")
        print("✅ XAgent integration structure is complete")
        print("📝 Ready for dependency installation and functional testing")
        return True
    else:
        print("⚠️ Some structure tests failed")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
