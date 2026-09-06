import os
import sqlite3


class SensorStorage:
    def __init__(self, db_path: str = "data/monitoring.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        """Create a connection to the SQLite database."""
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _init_db(self) -> None:
        """Create SQLite tables if they don't exist."""
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sensors (
                id INTEGER PRIMARY KEY,
                unit TEXT NOT NULL,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                min_valid_value REAL NOT NULL,
                max_valid_value REAL NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS measurements (
                id INTEGER PRIMARY KEY,
                timestamp TEXT NOT NULL,
                sensor_id INTEGER NOT NULL REFERENCES sensors(id),
                value REAL NOT NULL
            )
        """)

        conn.commit()
        conn.close()

    def add_sensor(self, sensor_metadata: dict) -> int:
        """Insert a new sensor and return its generated ID."""
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO sensors (
                unit,
                name,
                type,
                min_valid_value,
                max_valid_value
            )
            VALUES (
                :unit,
                :name,
                :type,
                :min_valid_value,
                :max_valid_value
            )
        """, sensor_metadata)

        sensor_id = cursor.lastrowid

        conn.commit()
        conn.close()

        return sensor_id

    def store_measurement(self, measurement: dict) -> int:
        """Insert a new measurement and return its generated ID."""
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO measurements (
                timestamp,
                sensor_id,
                value
            )
            VALUES (
                :timestamp,
                :sensor_id,
                :value
            )
        """, measurement)

        conn.commit()
        conn.close()

    def fetch_sensor(self, sensor_id: int) -> dict:
        """Retrieve sensor metadata"""
        conn = self._connect()
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()
        cursor.execute("""
            SELECT *
            FROM sensors
            WHERE id = ?       
        """, (sensor_id,)
        )

        row = cursor.fetchone()
        conn.close()
         
        if row is None:
            raise ValueError(f"Sensor {sensor_id} not found")

        return dict(row)

    def fetch_all_sensors(self) -> list[dict]:
        """Retrieve all sensors metadatas"""
        conn = self._connect()
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()
        cursor.execute("""
            SELECT *
            FROM sensors
        """
        )

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]