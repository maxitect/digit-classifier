from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from routers import predict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("model_service")

app = FastAPI(title="Model Service API")

# Configure CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(predict.router, prefix="/predict", tags=["predict"])

from config import settings
from utils.model_loader import load_model

@app.on_event("startup")
async def startup_event():
    logger.info("Loading model...")
    model = load_model(settings.model_path)
    app.state.model = model
    logger.info("Model loaded successfully.")


# Global error handling example
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}")
    return HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/")
async def root():
    return {"message": "Welcome to the Model Service API"}
