from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_guests():
    return {"message": "Guests endpoint - En desarrollo"}

@router.post("/")
async def create_guest():
    return {"message": "Create guest - En desarrollo"}