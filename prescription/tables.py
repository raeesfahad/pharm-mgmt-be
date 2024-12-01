from typing import List
from database.models import PrescriptionBase, FileBase
from sqlmodel import Field, Relationship


class Prescription(PrescriptionBase, table=True):
    id: int = Field(primary_key=True)
    files: List["File"] = Relationship(back_populates="prescription")

class File(FileBase, table=True):
    id: int = Field(primary_key=True)
    prescription : Prescription | None = Relationship(back_populates="files")