
import os
import sys

# Unset DATABASE_URL to simulate missing env var
if "DATABASE_URL" in os.environ:
    del os.environ["DATABASE_URL"]

try:
    from app import database
    print("Database imported successfully")
except Exception as e:
    print(f"Caught expected error during import: {e}")

try:
    import main
    print("Main imported successfully")
except Exception as e:
    print(f"Caught expected error during main import: {e}")
