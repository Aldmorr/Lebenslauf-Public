#!/usr/bin/env python3
"""
Setup script for CV Knowledge Assistant Chatbot
"""

import os
import subprocess
import sys
from pathlib import Path

def create_virtual_environment():
    """Create a virtual environment for the project."""
    print("Creating virtual environment...")
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ Virtual environment created successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to create virtual environment")
        return False

def install_requirements():
    """Install required packages."""
    print("Installing requirements...")
    venv_python = "venv/Scripts/python.exe" if os.name == "nt" else "venv/bin/python"
    
    if not os.path.exists(venv_python):
        print("❌ Virtual environment not found. Please create it first.")
        return False
    
    try:
        subprocess.run([venv_python, "-m", "pip", "install", "--upgrade", "pip"], check=True)
        subprocess.run([venv_python, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install requirements")
        return False

def setup_environment_file():
    """Setup the .env file from template."""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_file.exists():
        print("⚠️  .env file already exists. Skipping...")
        return True
    
    if not env_example.exists():
        print("❌ .env.example file not found")
        return False
    
    try:
        with open(env_example, 'r') as f:
            content = f.read()
        
        with open(env_file, 'w') as f:
            f.write(content)
        
        print("✅ .env file created from template")
        print("⚠️  Please edit .env file and add your API key and password!")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def check_cv_data():
    """Check if CV data file exists and prompt user to update it."""
    cv_file = Path("data/cv_data.txt")
    
    if not cv_file.exists():
        print("❌ CV data file not found")
        return False
    
    print("✅ CV data file found")
    print("⚠️  Please update data/cv_data.txt with your actual CV information!")
    return True

def print_next_steps():
    """Print next steps for the user."""
    activate_cmd = "venv\\Scripts\\activate" if os.name == "nt" else "source venv/bin/activate"
    
    print("\n" + "="*60)
    print("🎉 Setup completed! Next steps:")
    print("="*60)
    print(f"1. Activate virtual environment: {activate_cmd}")
    print("2. Edit .env file with your API key and password")
    print("3. Update data/cv_data.txt with your CV information")
    print("4. Run the app: streamlit run app.py")
    print("5. Access at: http://localhost:8501")
    print("="*60)

def main():
    """Main setup function."""
    print("🚀 Setting up CV Knowledge Assistant Chatbot...")
    print("="*60)
    
    # Check if we're in the right directory
    if not Path("app.py").exists():
        print("❌ app.py not found. Are you in the correct directory?")
        return False
    
    success = True
    
    # Setup steps
    if not create_virtual_environment():
        success = False
    
    if success and not install_requirements():
        success = False
    
    if success and not setup_environment_file():
        success = False
    
    if success and not check_cv_data():
        success = False
    
    if success:
        print_next_steps()
    else:
        print("❌ Setup failed. Please check the errors above.")
    
    return success

if __name__ == "__main__":
    main()