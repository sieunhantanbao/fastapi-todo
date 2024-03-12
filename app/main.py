from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def health_check():
    return "Service up and running"