from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlmodel import SQLModel, select
from database.models import Drug, Supplier
from prescription.tables import Prescription
from database.connecter import create_connection
from drug.router import drug_router
from supplier.router import supplier_router
from user.router import auth_router
from database.connecter import create_session

from prescription.router import prescription_router

app =  FastAPI()
UPLOAD_DIR = "uploads"



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_connection()


@app.get("/api/v1")
def root():
    return { "version" : "0.1", "name" : "Pharma Managmet Backend"}

@app.get("/api/dashboard")
def dashboard_data(session = Depends(create_session)):
    total_sale = None
    statement_stock = select(Drug.name, Drug.stock)
    results = session.exec(statement_stock).all()
    prescription_data = session.exec(select(Prescription).where(Prescription.admin_uploaded == True)).all()
    user_pres = session.query(Prescription).filter(Prescription.admin_uploaded == False).count()
    total_drugs = session.query(Drug).count()
    total_prescriptions = session.query(Prescription).count()
    total_suppliers = session.query(Supplier).count()

    
  
    data = [{"name": drug.name, "stock": drug.stock} for drug in results]
    chart_data = [{"name": drug.name, "value": drug.stock} for drug in results]



    data = [{"name": drug.name, "stock": drug.stock} for drug in results]
    chart_data = [{"name": drug.name, "value": drug.stock} for drug in results]

    total_drugs = session.query(Drug).count()
    total_prescriptions = session.query(Prescription).count()
    total_suppliers = session.query(Supplier).count()

    results_data ={

          "stock" : data,
           "chart_data" : chart_data,
           "total_drugs" : total_drugs,
           "total_prescriptions" : total_prescriptions,
           "total_suppliers" : total_suppliers,
           "admin_prescriptions" : prescription_data,
           "total_sale" : 0,
           "user_pres" : user_pres
           
         }
    return results_data










app.include_router(drug_router, prefix="/api/drugs")
app.include_router(auth_router, prefix="/api/auth")
app.include_router(supplier_router, prefix="/api/supplier")
app.include_router(prescription_router, prefix="/api/prescription")
app.mount("/", StaticFiles(directory="fe", html=True), name="fe")
