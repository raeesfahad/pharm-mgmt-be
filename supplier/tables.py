
from database.models import SupplierBase
from sqlmodel import Field, Relationship
from typing import Optional, List

class Supplier(SupplierBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    drugs: List["Drug"] = Relationship(back_populates="supplier")
