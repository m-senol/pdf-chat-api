from databases import Database
from .config import DATABASE_URL
from sqlalchemy import create_engine, MetaData


database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)
metadata = MetaData()
