"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal
from datetime import date

# ------------------------------------------------------------------
# Core app schemas
# ------------------------------------------------------------------

class Booking(BaseModel):
    """
    Booking requests from website
    Collection name: "booking"
    """
    full_name: str = Field(..., description="Full Name")
    contact_number: str = Field(..., description="Phone number")
    email: Optional[EmailStr] = Field(None, description="Email address")
    event_type: Literal[
        "Wedding",
        "Pre-Wedding",
        "Baby Shower",
        "Model Shoot",
        "Birthday",
        "Corporate",
        "Other",
    ] = Field(..., description="Type of event")
    event_date: Optional[date] = Field(None, description="Event date")
    location: Optional[str] = Field(None, description="Event location")
    budget_range: Optional[str] = Field(None, description="Budget range text")
    notes: Optional[str] = Field(None, description="Additional notes")
    requirements: Optional[str] = Field(None, description="Photo/Video requirements")


# Example schemas (kept for reference)
class User(BaseModel):
    name: str
    email: str
    address: str
    age: Optional[int] = None
    is_active: bool = True

class Product(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    category: str
    in_stock: bool = True
