from sqlalchemy import Column, String, Text, Integer, Table
from .db import metadata

pdf_texts = Table(
    'pdf_texts',
    metadata,
    Column('id', String, primary_key=True),
    Column('filename', String),
    Column('page_count', Integer),
    Column('content', Text),
    Column('upload_date', String),
)
