from fastapi import APIRouter

router = APIRouter()

@router.get("/{token}")
async def get_confirmation_page(token: str):
    return {"message": f"Confirmation page for token: {token}"}

@router.post("/{token}")
async def submit_confirmation(token: str):
    return {"message": "Confirmation submitted - En desarrollo"}