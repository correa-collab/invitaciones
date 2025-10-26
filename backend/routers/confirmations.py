from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

from database.connection import get_db
from database.models import Confirmation, Invitation, Event, Guest

router = APIRouter()

# Pydantic models
class ConfirmationCreate(BaseModel):
    will_attend: bool
    additional_guests: Optional[int] = 0
    dietary_requirements: Optional[str] = None
    special_requests: Optional[str] = None

class ConfirmationResponse(BaseModel):
    id: int
    invitation_id: int
    will_attend: bool
    additional_guests: int
    dietary_requirements: Optional[str] = None
    special_requests: Optional[str] = None
    confirmed_at: datetime
    
    class Config:
        from_attributes = True

class InvitationDetailsResponse(BaseModel):
    invitation_id: int
    event_title: str
    event_description: Optional[str] = None
    event_date: datetime
    event_location: str
    guest_name: str
    guest_email: str
    already_confirmed: bool
    confirmation_details: Optional[ConfirmationResponse] = None

@router.get("/{token}", response_model=InvitationDetailsResponse)
async def get_confirmation_page(token: str, db: Session = Depends(get_db)):
    """Obtener detalles de la invitación para la página de confirmación"""
    try:
        # Buscar la invitación por token
        invitation = db.query(Invitation).filter(
            Invitation.invitation_token == token
        ).join(Event).join(Guest).first()
        
        if not invitation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invitación no encontrada o token inválido"
            )
        
        # Verificar si ya existe una confirmación
        existing_confirmation = db.query(Confirmation).filter(
            Confirmation.invitation_id == invitation.id
        ).first()
        
        return InvitationDetailsResponse(
            invitation_id=invitation.id,
            event_title=invitation.event.title,
            event_description=invitation.event.description,
            event_date=invitation.event.event_date,
            event_location=invitation.event.location,
            guest_name=f"{invitation.guest.first_name} {invitation.guest.last_name}",
            guest_email=invitation.guest.email,
            already_confirmed=existing_confirmation is not None,
            confirmation_details=ConfirmationResponse(
                id=existing_confirmation.id,
                invitation_id=existing_confirmation.invitation_id,
                will_attend=existing_confirmation.will_attend,
                additional_guests=existing_confirmation.additional_guests,
                dietary_requirements=existing_confirmation.dietary_requirements,
                special_requests=existing_confirmation.special_requests,
                confirmed_at=existing_confirmation.confirmed_at
            ) if existing_confirmation else None
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener detalles de la invitación: {str(e)}"
        )

@router.post("/{token}", response_model=ConfirmationResponse)
async def submit_confirmation(
    token: str, 
    confirmation: ConfirmationCreate,
    db: Session = Depends(get_db)
):
    """Enviar confirmación de asistencia"""
    try:
        # Buscar la invitación por token
        invitation = db.query(Invitation).filter(
            Invitation.invitation_token == token
        ).first()
        
        if not invitation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invitación no encontrada o token inválido"
            )
        
        # Verificar si ya existe una confirmación
        existing_confirmation = db.query(Confirmation).filter(
            Confirmation.invitation_id == invitation.id
        ).first()
        
        if existing_confirmation:
            # Actualizar confirmación existente
            update_data = confirmation.dict()
            for field, value in update_data.items():
                setattr(existing_confirmation, field, value)
            
            db.commit()
            db.refresh(existing_confirmation)
            return existing_confirmation
        else:
            # Crear nueva confirmación
            db_confirmation = Confirmation(
                invitation_id=invitation.id,
                **confirmation.dict()
            )
            
            db.add(db_confirmation)
            db.commit()
            db.refresh(db_confirmation)
            return db_confirmation
            
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar confirmación: {str(e)}"
        )

@router.get("/invitation/{invitation_id}", response_model=ConfirmationResponse)
async def get_confirmation_by_invitation(
    invitation_id: int,
    db: Session = Depends(get_db)
):
    """Obtener confirmación por ID de invitación"""
    confirmation = db.query(Confirmation).filter(
        Confirmation.invitation_id == invitation_id
    ).first()
    
    if not confirmation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Confirmación no encontrada"
        )
    
    return confirmation