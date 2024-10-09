import pytest
from app.db import database

@pytest.mark.asyncio
async def test_database_connection():
    query = "SELECT 1"
    await database.connect()
    try:
        result = await database.fetch_one(query)
    except Exception as e:
        assert False, f"Failed to connect to database: {e}"
    else:
        assert result is not None, "Failed to connect to the database"
        assert result[0] == 1, "Unexpected result from the database query"
    finally:
        await database.disconnect()
