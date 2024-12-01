from database.models import Supplier, SupplierPublicWithDrugs, SupplierPublic
from database.connecter import engine
from sqlmodel import Session, select
from auth.local_provider import manager
from sqlalchemy.orm import selectinload
from fastapi import APIRouter, Depends, HTTPException, Query
from database.connecter import create_session
from typing import List

supplier_router = APIRouter(
    tags=["supplier"],
    #dependencies=[Depends(manager)]
)


@supplier_router.get("/all", response_model=List[SupplierPublicWithDrugs])
def get_suppliers(
    limit: int = Query(10, ge=1, description="Number of items to return"),
    offset: int = Query(0, description="Number of items to skip"),
    session: Session = Depends(create_session),
):
    total = session.query(Supplier).count()
    suppliers = session.exec(select(Supplier).offset(offset).limit(limit)).all()
    return suppliers[:limit] 


@supplier_router.get("/get/{sup_id}", response_model=SupplierPublicWithDrugs)
def read_supplier(sup_id: int):
    with Session(engine) as session:
        statement = select(Supplier).where(Supplier.id == sup_id).options(selectinload(Supplier.drugs))
        supplier = session.exec(statement).first()

        if not supplier:
            raise HTTPException(status_code=404, detail="supplier not found")
        return SupplierPublicWithDrugs.from_orm(supplier)


@supplier_router.post("/add")
def add_drug(supplier : Supplier):
    with Session(engine) as session:
        session.add(supplier)
        session.commit()
        session.refresh(supplier)
        return supplier


@supplier_router.delete("/delete/{sup_id}")
def delete_drug(sup_id: int):
    with Session(engine) as session:
        supplier = session.get(Supplier, sup_id)
        if not supplier:
            raise HTTPException(status_code=404, detail="Supplier not found")
        session.delete(supplier)
        session.commit()
        return {"ok": True}


@supplier_router.patch("/edit/{sup_id}")
def update_drug(sup_id: int, supplier: Supplier):
    with Session(engine) as session:
        db_supplier = session.get(Supplier, sup_id)
        if not db_supplier:
            raise HTTPException(status_code=404, detail="Supplier not found")
        supplier_data = supplier.dict(exclude_unset=True)
        for key, value in supplier_data.items():
            setattr(db_supplier, key, value)
        session.add(db_supplier)
        session.commit()
        session.refresh(db_supplier)
        return db_supplier
