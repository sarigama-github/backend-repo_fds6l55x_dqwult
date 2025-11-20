from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import datetime

from database import create_document, get_documents, db
from schemas import Booking

app = FastAPI(
    title="HKPhotography & Films API",
    description="Backend for booking submissions and content",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/test")
def test():
    # Verify database connectivity if available
    try:
        if db is not None:
            db.command("ping")
            db_ok = True
        else:
            db_ok = False
    except Exception:
        db_ok = False
    return {"status": "ok", "database": db_ok}


# -------------------- Booking Endpoints --------------------
class BookingResponse(BaseModel):
    id: str
    submitted_at: datetime


@app.post("/book", response_model=BookingResponse)
async def submit_booking(payload: Booking):
    try:
        booking_id = create_document("booking", payload)
        return {"id": booking_id, "submitted_at": datetime.utcnow()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/book", response_model=List[dict])
async def list_bookings(limit: int = 50):
    try:
        docs = get_documents("booking", {}, limit)
        # Convert ObjectId to string
        for d in docs:
            d["_id"] = str(d.get("_id"))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
