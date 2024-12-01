from typing import Annotated, List
from fastapi import APIRouter, Body,Depends, Form, Query, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from database.connecter import create_session
from database.models import PrescriptionBase,PaginatedResponsePrescriptions
from prescription.tables import Prescription
from sqlmodel import select
from .tables import File as fl
import os

prescription_router = APIRouter(
    tags=["prescription"],
)

@prescription_router.get("/all", response_model=PaginatedResponsePrescriptions)
def get_all_prescriptions(
    limit: int = Query(10, ge=1, description="Number of items to return"),
    offset: int = Query(0, description="Number of items to skip"),
    session = Depends(create_session)
):
    total = session.query(Prescription).count()
    prescriptions = session.exec(select(Prescription).offset(offset).limit(limit)).all()
    return {
        "data": prescriptions,
        "total": total,
        "limit": limit,
        "offset": offset
    }

@prescription_router.get("/get/{pres_id}")
def get_prescription(pres_id, session = Depends(create_session)):
    prescription = session.exec(select(Prescription).where(Prescription.id == pres_id)).first()
    if not prescription:
        return {"error" : "record not found"}
    return prescription

@prescription_router.post("/add")
async def add_prescription(prescription : Prescription , session = Depends(create_session)):
    session.add(prescription)
    session.commit()
    session.refresh(prescription)
    return prescription

@prescription_router.delete("/delete/{pres_id}")
def delete_prescription(pres_id: int, session = Depends(create_session)):

    prescription = session.get(Prescription, pres_id)
    if not prescription:
        raise HTTPException(status_code=404, detail="Prescription not found")

    session.delete(prescription)
    session.commit()
    return {"ok": True}

@prescription_router.patch("/edit/{pres_id}")
def update_prescription(pres_id: str, prescription: Prescription, session=Depends(create_session)):
 
    db_prescription = session.get(Prescription, pres_id)
    if not db_prescription:
            raise HTTPException(status_code=404, detail="Prescription not found")
    prescription_data = prescription.model_dump(exclude_unset=True)
    for key, value in prescription_data.items():
        setattr(db_prescription, key, value)
        session.add(db_prescription)
        session.commit()
        session.refresh(db_prescription)
        return db_prescription

@prescription_router.post("/prescription_file/{pres_id}")
async def upload_file(pres_id : int, file_upload: UploadFile = File(...), session=Depends(create_session)):
    # Create directory to store files if it doesn't exist
    upload_dir = "fe/files"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    file_name = f"{file_upload.filename}"
    file_path = os.path.join(upload_dir, file_name)

    try:
        with open(file_path, "wb") as f:
            f.write(await file_upload.read())

    except Exception as e:
        return JSONResponse({"error": f"file write failed {e}"}, status_code=500)

    new_file = fl(file_path=file_name, prescription_id=pres_id)
    session.add(new_file);
    session.commit()
    session.refresh(new_file)
    return new_file
