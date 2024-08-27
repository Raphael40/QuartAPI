from quart_db import Connection

async def migrate(connection: Connection) -> None:
    await connection.execute(
        """CREATE TABLE cards (
                id INTEGER PRIMARY KEY,
                question TEXT NOT NULL,
                answer TEXT NOT NULL
                )""",
    )

async def valid_migration(connection: Connection) -> bool:
    return True