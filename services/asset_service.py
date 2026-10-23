import sqlite3
from database.connection import get_db_connection


class AssetService:

    @staticmethod
    def create_asset(asset):
        conn = get_db_connection()

        try:
            conn.execute(
                "INSERT INTO assets "
                "(asset_id, type, brand, model, serial_no, purchase_date) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (
                    asset.asset_id,
                    asset.type,
                    asset.brand,
                    asset.model,
                    asset.serial_no,
                    asset.purchase_date
                )
            )

            conn.commit()

            return {
                "message": "Asset created",
                "status": "AVAILABLE"
            }

        except sqlite3.IntegrityError:
            conn.rollback()
            return {
                "error": "Asset ID or serial number already exists"
            }

        finally:
            conn.close()

    @staticmethod
    def get_asset(asset_id):
        conn = get_db_connection()

        try:
            row = conn.execute(
                "SELECT asset_id, type, brand, model, serial_no, "
                "status, purchase_date "
                "FROM assets WHERE asset_id = ?",
                (asset_id,)
            ).fetchone()

            if row is None:
                return None

            return {
                "asset_id": row[0],
                "type": row[1],
                "brand": row[2],
                "model": row[3],
                "serial_no": row[4],
                "status": row[5],
                "purchase_date": row[6]
            }

        finally:
            conn.close()

    
    @staticmethod
    def get_all_assets():
        conn = get_db_connection()

        try:
            rows = conn.execute(
                "SELECT asset_id, type, brand, model, serial_no, "
                "status, purchase_date "
                "FROM assets "
                "ORDER BY asset_id"
            ).fetchall()

            assets = []

            for row in rows:
                assets.append({
                    "asset_id": row[0],
                    "type": row[1],
                    "brand": row[2],
                    "model": row[3],
                    "serial_no": row[4],
                    "status": row[5],
                    "purchase_date": row[6]
                })

            return assets

        finally:
            conn.close()


    @staticmethod
    def update_asset(asset_id: str, asset):
        conn = get_db_connection()

        try:
            existing = conn.execute(
                "SELECT asset_id FROM assets WHERE asset_id = ?",
                (asset_id,)
            ).fetchone()

            if existing is None:
                return {"error": "Asset not found"}

            conn.execute(
                "UPDATE assets "
                "SET type = ?, brand = ?, model = ?, serial_no = ?, purchase_date = ? "
                "WHERE asset_id = ?",
                (
                    asset.type,
                    asset.brand,
                    asset.model,
                    asset.serial_no,
                    asset.purchase_date,
                    asset_id
                )
            )

            conn.commit()

            return {
                "message": "Asset updated",
                "asset_id": asset_id
            }

        finally:
            conn.close()

    @staticmethod
    def delete_asset(asset_id: str):
        conn = get_db_connection()

        try:
            existing = conn.execute(
                "SELECT asset_id FROM assets WHERE asset_id = ?",
                (asset_id,)
            ).fetchone()

            if existing is None:
                return {"error": "Asset not found"}

            conn.execute(
                "DELETE FROM assets WHERE asset_id = ?",
                (asset_id,)
            )

            conn.commit()

            return {
                "message": "Asset deleted",
                "asset_id": asset_id
            }

        finally:
            conn.close()