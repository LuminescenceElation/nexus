from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Nexus API", version="1.0.0")

DB_HOST = "localhost"
DB_NAME = "nexus_db"
DB_USER = "app_user"
DB_PASSWORD = "app_password123"

class Item(BaseModel):
    name: str
    description: str = None

class ItemResponse(Item):
    id: int
    created_at: datetime

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")

@app.get("/", tags=["Health"])
def root():
    return {"message": "Nexus API is running", "version": "1.0.0", "status": "healthy"}

@app.get("/api/health", tags=["Health"])
def health():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        conn.close()
        return {"status": "healthy", "database": "connected", "timestamp": datetime.utcnow().isoformat()}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e), "timestamp": datetime.utcnow().isoformat()}, 500

@app.post("/api/items", response_model=ItemResponse, tags=["Items"])
def create_item(item: Item):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("INSERT INTO items (name, description) VALUES (%s, %s) RETURNING id, name, description, created_at", (item.name, item.description))
        result = cursor.fetchone()
        conn.commit()
        return result
    except Exception as e:
        conn.rollback()
        logger.error(f"Error creating item: {e}")
        raise HTTPException(status_code=500, detail="Error creating item")
    finally:
        cursor.close()
        conn.close()

@app.get("/api/items", response_model=List[ItemResponse], tags=["Items"])
def list_items():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("SELECT id, name, description, created_at FROM items ORDER BY created_at DESC")
        items = cursor.fetchall()
        return items
    except Exception as e:
        logger.error(f"Error listing items: {e}")
        raise HTTPException(status_code=500, detail="Error listing items")
    finally:
        cursor.close()
        conn.close()

@app.get("/api/items/{item_id}", response_model=ItemResponse, tags=["Items"])
def get_item(item_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("SELECT id, name, description, created_at FROM items WHERE id = %s", (item_id,))
        item = cursor.fetchone()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return item
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving item: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving item")
    finally:
        cursor.close()
        conn.close()

@app.delete("/api/items/{item_id}", tags=["Items"])
def delete_item(item_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM items WHERE id = %s RETURNING id", (item_id,))
        result = cursor.fetchone()
        conn.commit()
        if not result:
            raise HTTPException(status_code=404, detail="Item not found")
        return {"message": f"Item {item_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        logger.error(f"Error deleting item: {e}")
        raise HTTPException(status_code=500, detail="Error deleting item")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
