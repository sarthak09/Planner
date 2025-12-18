#!/usr/bin/env python3
"""
Quick test script to verify your GROQ API setup
Run this before starting the backend server
"""

from dotenv import load_dotenv
import os
import sys

def test_env_file():
    """Test if .env file exists and is readable"""
    print("=" * 60)
    print("🔍 Testing Environment Setup")
    print("=" * 60)
    
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("   Create a .env file with your GROQ_API_KEY")
        print("   Example: cp .env.example .env")
        return False
    
    print("✅ .env file found")
    return True

def test_api_key():
    """Test if GROQ_API_KEY is set"""
    load_dotenv()
    key = os.getenv("GROQ_API_KEY")
    
    if not key:
        print("❌ GROQ_API_KEY not found in .env file!")
        print("   Add the following line to your .env file:")
        print("   GROQ_API_KEY=your_actual_key_here")
        return False
    
    if key == "your_groq_api_key_here":
        print("❌ GROQ_API_KEY is still set to default value!")
        print("   Replace it with your actual API key from:")
        print("   https://console.groq.com/keys")
        return False
    
    print(f"✅ GROQ_API_KEY found: {key[:10]}...{key[-4:]}")
    return True

def test_imports():
    """Test if required packages are installed"""
    print("\n" + "=" * 60)
    print("📦 Testing Package Imports")
    print("=" * 60)
    
    required_packages = [
        ('flask', 'Flask'),
        ('flask_cors', 'CORS'),
        ('langchain', 'LangChain'),
        ('langchain_groq', 'ChatGroq'),
        ('langchain_core.prompts', 'ChatPromptTemplate'),
        ('dotenv', 'python-dotenv'),
    ]
    
    all_ok = True
    for package, name in required_packages:
        try:
            __import__(package)
            print(f"✅ {name}")
        except ImportError:
            print(f"❌ {name} - Run: pip install {package.replace('_', '-')}")
            all_ok = False
    
    return all_ok

def test_groq_connection():
    """Test connection to GROQ API"""
    print("\n" + "=" * 60)
    print("🌐 Testing GROQ API Connection")
    print("=" * 60)
    
    try:
        from langchain.chat_models import init_chat_model
        load_dotenv()
        
        print("🔄 Attempting to initialize GROQ model...")
        llm = init_chat_model(model="groq:llama-3.1-8b-instant")
        
        print("🔄 Testing API call...")
        response = llm.invoke("Say 'Hello'")
        
        print(f"✅ GROQ API connection successful!")
        print(f"   Response: {response.content[:50]}...")
        return True
        
    except Exception as e:
        print(f"❌ GROQ API connection failed!")
        print(f"   Error: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("\n🧪 AI Travel Planner - Setup Verification\n")
    
    tests = [
        ("Environment File", test_env_file),
        ("API Key", test_api_key),
        ("Package Imports", test_imports),
        ("GROQ Connection", test_groq_connection),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ {name} test crashed: {str(e)}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    all_passed = all(result for _, result in results)
    
    print("=" * 60)
    if all_passed:
        print("🎉 All tests passed! You can start the backend server.")
        print("   Run: python3 backend.py")
        return 0
    else:
        print("⚠️  Some tests failed. Please fix the issues above.")
        print("   See TROUBLESHOOTING.md for help")
        return 1

if __name__ == "__main__":
    sys.exit(main())