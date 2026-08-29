import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DB_PATH = os.path.join(ROOT, "database", "learning.db")
SCHEMA_PATH = os.path.join(ROOT, "database", "schema.sql")
CONTENT_DIR = os.path.join(ROOT, "content")
CHALLENGES_DEF = os.path.join(ROOT, "app", "data", "challenges_def.py")
