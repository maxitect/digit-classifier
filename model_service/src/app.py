from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from config import settings
from utils.model_loader import load_model
from routers import predict
from models.prediction import ErrorResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("model_service")


def create_app():
    # Define lifespan event handler
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Startup: Load model
        logger.info("Loading model...")
        try:
            model = load_model(settings.model_path)
            app.state.model = model
            logger.info("Model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            app.state.model = None
            logger.warning(
                "API will start but prediction endpoints will be unavailable")

        yield
        # Shutdown: Clean up resources
        logger.info("Shutting down application...")
        # Add any cleanup code here (close connections, etc.)

    app = FastAPI(
        title="Digit Recognition API",
        description="API for recognizing handwritten digits "
        "using a neural network model",
        version="1.0.0",
        lifespan=lifespan
    )

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
    app.include_router(predict.router, prefix="/predict", tags=["prediction"])

    # Global error handling
    async def general_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ErrorResponse(
                detail="Internal Server Error",
                error_type="server_error"
            ).dict()
        )
    app.exception_handler(Exception)(general_exception_handler)

    async def http_exception_handler(request: Request, exc: HTTPException):
        logger.warning(
            f"HTTP exception: {exc.detail} (status code: {exc.status_code})")
        has_valid_headers = hasattr(exc, "headers") and exc.headers
        error_type = (
            exc.headers.get("X-Error-Type", "server_error")
            if has_valid_headers else "server_error"
        )
        return JSONResponse(
            status_code=exc.status_code,
            headers=exc.headers,
            content=ErrorResponse(
                detail=exc.detail,
                error_type=error_type
            ).model_dump()
        )
    app.exception_handler(HTTPException)(http_exception_handler)

    async def root():
        model_status = (
            "available" if app.state.model is not None else "unavailable"
        )
        return {
            "message": "Welcome to the Digit Recognition API",
            "model_status": model_status,
            "version": app.version
        }
    app.get("/", tags=["health"])(root)

    async def health_check():
        """
        Health check endpoint to verify API status and model availability
        """
        return {
            "status": "healthy",
            "model_loaded": app.state.model is not None
        }
    app.get("/health", tags=["health"])(health_check)

    return app


app = create_app()
