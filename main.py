from fastapi import FastAPI
from database.connection import init_db
from routers import employees, assets, assignments, tickets


app = FastAPI(title="IT Asset & Service Management System")


@app.on_event("startup")
def startup_event():
    init_db()


app.include_router(employees.router)
app.include_router(assets.router)
app.include_router(assignments.router)
app.include_router(tickets.router)


@app.get("/")
def health_check():
    return {"status": "ONLINE"}