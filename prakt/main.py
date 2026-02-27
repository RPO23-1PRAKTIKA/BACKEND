from fastapi import FastAPI
from database import engine, Base
from auth import router as auth_router
import uvicorn

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)

def main():
    uvicorn.run(app, host="127.0.0.1", port=8000)
if __name__ == "__main__":
    main()