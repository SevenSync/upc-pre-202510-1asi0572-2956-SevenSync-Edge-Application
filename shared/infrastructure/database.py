"""
Database initialization for the Smart Band Edge Service.

Sets up the SQLite database and creates required tables for devices and health records.
"""
from peewee import SqliteDatabase

# Initialize SQLite database
db = SqliteDatabase('macetech.db')


def init_db() -> None:
    """
    Initialize the database and create tables for Device and HealthRecord models.
    """
    db.connect()
    """
    from iam.infrastructure.models import Device
    from health.infrastructure.models import HealthRecord
    """
    db.create_tables([], safe=True)
    """
    AGREGAR MODELOS AQUÍ, DENTRO DDE create_tables
    """
    db.close()
