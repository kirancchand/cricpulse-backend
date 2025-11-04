from fastapi import FastAPI
from routes.auth import auth
from routes.admin import admin
from routes.application import application
app = FastAPI(title="StrikeIt")


#include route
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(application.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8020,reload=True)