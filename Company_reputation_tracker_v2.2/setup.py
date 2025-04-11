#!/usr/bin/env python
"""
Setup script for the Company Reputation Tracker.
This script installs dependencies and initializes the database.
"""

import os
import subprocess
import sys
import time

def print_step(message):
    """Print a step message with formatting."""
    print("\n" + "=" * 80)
    print(f" {message}")
    print("=" * 80)

def main():
    """Run the setup process."""
    print_step("Setting up Company Reputation Tracker")
    
    # Check if pip is available
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], check=True, stdout=subprocess.PIPE)
    except subprocess.CalledProcessError:
        print("Error: pip is not available. Please install pip first.")
        return False
    
    # Install requirements
    print_step("Installing dependencies")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    except subprocess.CalledProcessError:
        print("Error installing dependencies. Please check the error message above.")
        
        # Offer to install minimal dependencies
        choice = input("\nWould you like to try installing minimal dependencies without Hugging Face? (y/n): ")
        if choice.lower() == 'y':
            # Create minimal requirements file
            with open("requirements_minimal.txt", "w") as f:
                f.write("""dash>=2.9.0
dash-bootstrap-components>=1.4.0
plotly>=5.13.0
sqlalchemy>=2.0.0
requests>=2.31.0
python-dotenv>=1.0.0
pandas>=2.0.0
""")
            
            try:
                print("\nInstalling minimal dependencies...")
                subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements_minimal.txt"], check=True)
                print("Minimal dependencies installed successfully.")
            except subprocess.CalledProcessError:
                print("Error installing minimal dependencies. Setup cannot continue.")
                return False
        else:
            return False
    
    # Download NLTK data
    print_step("Downloading NLTK data")
    try:
        import nltk
        nltk.download('punkt', quiet=True)
        nltk.download('averaged_perceptron_tagger', quiet=True)
        print("NLTK data downloaded successfully.")
    except Exception as e:
        print(f"Warning: Could not download NLTK data: {e}")
        print("This may affect TextBlob functionality if Hugging Face is not available.")
    
    # Initialize the database
    print_step("Initializing the database")
    try:
        print("Running db.py to create database...")
        subprocess.run([sys.executable, "db.py"], check=True)
    except subprocess.CalledProcessError:
        print("Error initializing the database. Please check the error message above.")
        return False
    
    # Create .env file if it doesn't exist
    if not os.path.exists(".env"):
        print_step("Creating .env file")
        with open(".env", "w") as f:
            f.write("NEWSAPI_KEY=your_newsapi_key_here\n")
        print(".env file created. Please edit it to add your NewsAPI key.")
    
    # Success message
    print_step("Setup completed successfully!")
    print("""
To run the application:
    
1. Edit .env file to add your NewsAPI key
2. Run the dashboard with: python dashboard.py
3. Access the dashboard at: http://localhost:8050

To add companies and fetch mentions:
    python runner.py --add --name "Company Name" --aliases "Alias1,Alias2"
    python runner.py --company 1
    
Enjoy your Company Reputation Tracker!
""")
    
    return True

if __name__ == "__main__":
    success = main()
    
    if not success:
        print("\nSetup encountered errors. Please resolve the issues and try again.")
        sys.exit(1)
    
    # Wait for user to read the instructions
    input("\nPress Enter to exit...")