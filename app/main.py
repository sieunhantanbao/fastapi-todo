from fastapi import FastAPI
import uvicorn
from routers import company, user
app = FastAPI()

app.include_router(company.router)
app.include_router(user.router)

@app.get("/")
async def health_check():
    return "Service up and running"

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)