from fastapi import FastAPI

app = FastAPI(title="CricPulse")


@app.get("/")
async def root():
    return {"message": "Hello World"}
