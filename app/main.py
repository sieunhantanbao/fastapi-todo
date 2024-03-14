from fastapi import FastAPI
from routers import company
app = FastAPI()

app.include_router(company.router)

@app.get("/")
async def health_check():
    return "Service up and running"