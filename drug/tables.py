from .models import DrugBase
from sqlmodel import Field, Relationship
from typing import Optional

class Drug(DrugBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    supplier: Supplier | None = Relationship(back_populates="drugs")
