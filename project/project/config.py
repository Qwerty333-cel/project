from decouple import config

DATABASE_URL = config("DATABASE_URL", default="postgresql://postgres:laygon@localhost:5432/mydatabase")
db_url = 'postgresql://postgres:laygon@localhost:5432/mydatabase'