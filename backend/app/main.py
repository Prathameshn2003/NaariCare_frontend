from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import doctors

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes with /api prefix
app.include_router(doctors.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Backend running successfully"}
