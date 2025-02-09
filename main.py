from fastapi import FastAPI
from api.endpoints import user




app = FastAPI()
app.include_router(user.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
