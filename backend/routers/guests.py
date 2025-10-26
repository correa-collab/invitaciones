from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

from database.connection import get_db
from database.models import Guest, User
from routers.auth import get_current_active_user

router = APIRouter()

# Pydantic models
class GuestBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    phone: Optional[str] = None
    company: Optional[str] = None
    notes: Optional[str] = None

class GuestCreate(GuestBase):
    pass

class GuestUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    notes: Optional[str] = None

class GuestResponse(GuestBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

@router.get("/", response_model=List[GuestResponse])
async def get_guests(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Obtener todos los invitados"""
    guests = db.query(Guest).offset(skip).limit(limit).all()
    return guests

@router.post("/", response_model=GuestResponse)
async def create_guest(
    guest: GuestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Crear un nuevo invitado"""
    # Verificar si el email ya existe
    existing_guest = db.query(Guest).filter(Guest.email == guest.email).first()
    if existing_guest:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un invitado con este email"
        )
    
    db_guest = Guest(**guest.dict())
    db.add(db_guest)
    db.commit()
    db.refresh(db_guest)
    return db_guest

@router.get("/{guest_id}", response_model=GuestResponse)
async def get_guest(
    guest_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Obtener un invitado específico"""
    guest = db.query(Guest).filter(Guest.id == guest_id).first()
    if not guest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invitado no encontrado"
        )
    return guest

@router.put("/{guest_id}", response_model=GuestResponse)
async def update_guest(
    guest_id: int,
    guest_update: GuestUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Actualizar un invitado"""
    db_guest = db.query(Guest).filter(Guest.id == guest_id).first()
    if not db_guest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invitado no encontrado"
        )
    
    # Verificar email duplicado si se está actualizando
    if guest_update.email and guest_update.email != db_guest.email:
        existing_guest = db.query(Guest).filter(Guest.email == guest_update.email).first()
        if existing_guest:
            raise HTTPException(
                status_code=400,
                detail="Ya existe un invitado con este email"
            )
    
    update_data = guest_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_guest, field, value)
    
    db.commit()
    db.refresh(db_guest)
    return db_guest

@router.delete("/{guest_id}")
async def delete_guest(
    guest_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Eliminar un invitado"""
    db_guest = db.query(Guest).filter(Guest.id == guest_id).first()
    if not db_guest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invitado no encontrado"
        )
    
    db.delete(db_guest)
    db.commit()
    return {"message": "Invitado eliminado correctamente"}