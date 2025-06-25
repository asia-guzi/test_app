from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import register_routes


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Location"],
)

register_routes(app)
