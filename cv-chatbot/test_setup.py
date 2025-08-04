#!/usr/bin/env python3
"""
Quick test script to verify the CV chatbot setup
"""

import os
import sys
from pathlib import Path

def test_file_structure():
    """Test if all required files exist."""
    print("🔍 Testing file structure...")
    
    required_files = [
        "app.py",
        "requirements.txt",
        "backend/__init__.py",
        "backend/auth.py",
        "backend/chatbot.py",
        "backend/prompts.py",
        "config/settings.py",
        "data/cv_data.txt",
        ".env.example",
        ".gitignore"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ All required files present")
        return True

def test_imports():
    """Test if the main modules can be imported."""
    print("🔍 Testing imports...")
    
    try:
        # Add the current directory to Python path
        sys.path.insert(0, str(Path.cwd()))
        
        from backend.auth import AuthManager
        from backend.chatbot import CVChatbot
        from backend.prompts import get_system_prompt, get_welcome_message
        from config.settings import load_cv_data
        
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_auth_manager():
    """Test the AuthManager functionality."""
    print("🔍 Testing AuthManager...")
    
    try:
        # Set a test password
        os.environ["ACCESS_PASSWORD"] = "test_password_123"
        
        from backend.auth import AuthManager
        auth = AuthManager()
        
        # Test password verification
        if not auth.verify_password("test_password_123"):
            print("❌ Password verification failed")
            return False
        
        if auth.verify_password("wrong_password"):
            print("❌ Password verification should have failed")
            return False
        
        # Test token generation
        token = auth.generate_session_token("test_password_123")
        if not token:
            print("❌ Token generation failed")
            return False
        
        print("✅ AuthManager tests passed")
        return True
    except Exception as e:
        print(f"❌ AuthManager test error: {e}")
        return False

def test_cv_data_loading():
    """Test CV data loading."""
    print("🔍 Testing CV data loading...")
    
    try:
        from config.settings import load_cv_data
        cv_data = load_cv_data()
        
        if not cv_data or len(cv_data.strip()) == 0:
            print("❌ CV data is empty")
            return False
        
        print(f"✅ CV data loaded ({len(cv_data)} characters)")
        return True
    except Exception as e:
        print(f"❌ CV data loading error: {e}")
        return False

def test_prompts():
    """Test prompt generation."""
    print("🔍 Testing prompts...")
    
    try:
        from backend.prompts import get_system_prompt, get_welcome_message, get_suggested_questions
        
        system_prompt = get_system_prompt("Sample CV data", "John Doe")
        if not system_prompt or len(system_prompt) < 50:
            print("❌ System prompt generation failed")
            return False
        
        welcome = get_welcome_message()
        if not welcome:
            print("❌ Welcome message generation failed")
            return False
        
        suggestions = get_suggested_questions()
        if not suggestions or len(suggestions) == 0:
            print("❌ Suggested questions generation failed")
            return False
        
        print("✅ Prompt generation tests passed")
        return True
    except Exception as e:
        print(f"❌ Prompt test error: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Running CV Chatbot Setup Tests")
    print("=" * 50)
    
    tests = [
        test_file_structure,
        test_imports,
        test_auth_manager,
        test_cv_data_loading,
        test_prompts
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The chatbot setup is working correctly.")
        print("\n📝 Next steps:")
        print("1. Copy .env.example to .env and add your API key and password")
        print("2. Update data/cv_data.txt with your actual CV information")
        print("3. Run: streamlit run app.py")
        return True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    main()