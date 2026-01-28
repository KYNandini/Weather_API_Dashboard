"""
Database initialization script for production app
Ensures database tables are created before app runs
"""
import os
import sys

# Create instance folder first
instance_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
os.makedirs(instance_path, exist_ok=True)

from dotenv import load_dotenv
load_dotenv()

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app_production import app, db

def init_db():
    """Initialize the database"""
    print("Initializing database...")
    
    try:
        with app.app_context():
            # Create all tables
            db.create_all()
            print("✓ Database tables created successfully")
            print(f"✓ Database file: {instance_path}/weather_dashboard.db")
    except Exception as e:
        print(f"Error: {e}")
        raise

if __name__ == '__main__':
    try:
        init_db()
        print("\nDatabase initialization complete!")
    except Exception as e:
        print(f"Error initializing database: {e}")
        sys.exit(1)
