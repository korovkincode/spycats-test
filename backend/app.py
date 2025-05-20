from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.spyCat import router as SpyCatRouter
from routes.mission import router as MissionRouter
from routes.target import router as TargetRouter
from config.database import Database


app = FastAPI()
Database.setup()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173"
]
app.add_middleware(
    CORSMiddleware, allow_origins=origins,
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)


@app.get("/", tags=["Root"])
async def root() -> dict:
    return {"message": "API for Spy Cat Agency [Test Assement] using FastAPI + PostgreSQL"}


app.include_router(SpyCatRouter, tags=["Spy-Cat"], prefix="/spy-cat")
app.include_router(MissionRouter, tags=["Mission"], prefix="/mission")
app.include_router(TargetRouter, tags=["Target"], prefix="/target")