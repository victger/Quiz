import os
from database.db import create_tables

db_file = '/app/db/quiz.db'

# Créer le dossier si nécessaire
os.makedirs(os.path.dirname(db_file), exist_ok=True)

if not os.path.exists(db_file):
    create_tables(db_file)