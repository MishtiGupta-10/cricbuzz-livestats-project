import os
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from database.database import Base, engine
from database.models import Venue, Team, Player, Match, Scorecard, SyncLog

def run_test():
    print("Creating tables in memory...")
    try:
        Base.metadata.create_all(bind=engine)
        print("Successfully created tables!")
        print("Models are properly configured.")
    except Exception as e:
        print(f"Error creating tables: {e}")

if __name__ == "__main__":
    run_test()
