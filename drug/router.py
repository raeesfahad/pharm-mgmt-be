from database.models import Drug, DrugCreate, DrugPublic, DrugPublicWithSupplier, PaginatedResponseDrug
from database.connecter import engine
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from auth.local_provider import manager
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query

drug_router = APIRouter(
    tags=["drugs"],
    #dependencies=[Depends(manager)],
)


@drug_router.get("/all", response_model=PaginatedResponseDrug)
def get_drugs(
    limit: int = Query(10, ge=1, description="Number of items to return"),
    offset: int = Query(0, description="Number of items to skip"),
):
    with Session(engine) as session:
        # Count total number of drugs
        total = session.query(Drug).count()

        # Fetch paginated drugs
        statement = (
            select(Drug)
            .options(selectinload(Drug.supplier))
            .offset(offset)
            .limit(limit)
        )
        drugs = session.exec(statement).all()

        # Create response
        response = PaginatedResponseDrug(
            data=[DrugPublicWithSupplier.from_orm(drug) for drug in drugs],
            total=total,
            limit=limit,
            offset=offset,
        )
        return response


@drug_router.get("/get/{drug_id}", response_model=DrugPublic)
def read_drug(drug_id: int):
    with Session(engine) as session:
        drug = session.get(Drug, drug_id)
        if not drug:
            raise HTTPException(status_code=404, detail="Drug not found")
        return drug


@drug_router.post("/add", response_model=DrugCreate)
def add_drug(drug: Drug):
    with Session(engine) as session:
        session.add(drug)
        session.commit()
        session.refresh(drug)
        return drug


@drug_router.delete("/delete/{drug_id}")
def delete_drug(drug_id: int):
    with Session(engine) as session:
        drug = session.get(Drug, drug_id)
        if not drug:
            raise HTTPException(status_code=404, detail="Drug not found")
        session.delete(drug)
        session.commit()
        return {"message" : "drug deleted suceessfully"}


@drug_router.patch("/edit/{drug_id}", response_model=DrugPublic)
def update_drug(drug_id: int, drug: Drug):
    with Session(engine) as session:
        db_drug = session.get(Drug, drug_id)
        if not db_drug:
            raise HTTPException(status_code=404, detail="Drug not found")
        drug_data = drug.dict(exclude_unset=True)
        for key, value in drug_data.items():
            setattr(db_drug, key, value)
        session.add(db_drug)
        session.commit()
        session.refresh(db_drug)
        return db_drug
