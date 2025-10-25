from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_invitations():
    return {"message": "Invitations endpoint - En desarrollo"}

@router.post("/send")
async def send_invitations():
    return {"message": "Send invitations - En desarrollo"}