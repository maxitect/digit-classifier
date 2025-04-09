from fastapi import APIRouter

router = APIRouter()


@router.post("/")
async def predict():
    # Dummy prediction endpoint
    return {"prediction": "dummy_value"}
