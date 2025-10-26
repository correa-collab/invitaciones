from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel, EmailStr
import uuid
from datetime import datetime
from database.connection import get_db
from database.models import Invitation, Event, Guest, User
from routers.auth import get_current_active_user

router = APIRouter()

# Pydantic models for request/response
class InvitationCreate(BaseModel):
    event_id: int
    guest_email: EmailStr
    guest_first_name: str
    guest_last_name: str
    guest_phone: str = None
    guest_company: str = None

class InvitationResponse(BaseModel):
    id: int
    event_id: int
    guest_id: int
    invitation_token: str
    email_sent: bool
    sent_at: datetime = None
    guest_email: str
    guest_name: str
    event_title: str
    
    class Config:
        from_attributes = True

@router.get("/", response_model=List[InvitationResponse])
async def get_invitations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Obtener todas las invitaciones"""
    try:
        invitations = (
            db.query(Invitation)
            .join(Guest)
            .join(Event)
            .filter(Event.organizer_id == current_user.id)
            .all()
        )
        
        result = []
        for invitation in invitations:
            result.append(InvitationResponse(
                id=invitation.id,
                event_id=invitation.event_id,
                guest_id=invitation.guest_id,
                invitation_token=invitation.invitation_token,
                email_sent=invitation.email_sent,
                sent_at=invitation.sent_at,
                guest_email=invitation.guest.email,
                guest_name=f"{invitation.guest.first_name} {invitation.guest.last_name}",
                event_title=invitation.event.title
            ))
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener invitaciones: {str(e)}")

@router.post("/", response_model=InvitationResponse)
async def create_invitation(
    invitation_data: InvitationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Crear una nueva invitación"""
    try:
        # Verificar si el evento existe
        event = db.query(Event).filter(Event.id == invitation_data.event_id).first()
        if not event or event.organizer_id != current_user.id:
            raise HTTPException(status_code=404, detail="Evento no encontrado")
        
        # Buscar o crear el invitado
        guest = db.query(Guest).filter(Guest.email == invitation_data.guest_email).first()
        if not guest:
            guest = Guest(
                email=invitation_data.guest_email,
                first_name=invitation_data.guest_first_name,
                last_name=invitation_data.guest_last_name,
                phone=invitation_data.guest_phone,
                company=invitation_data.guest_company
            )
            db.add(guest)
            db.flush()  # Para obtener el ID del guest
        
        # Verificar si ya existe una invitación para este guest y evento
        existing_invitation = db.query(Invitation).filter(
            Invitation.event_id == invitation_data.event_id,
            Invitation.guest_id == guest.id
        ).first()
        
        if existing_invitation:
            raise HTTPException(
                status_code=400, 
                detail="Ya existe una invitación para este invitado en este evento"
            )
        
        # Crear la invitación
        invitation = Invitation(
            event_id=invitation_data.event_id,
            guest_id=guest.id,
            invitation_token=str(uuid.uuid4()),
            email_sent=False
        )
        
        db.add(invitation)
        db.commit()
        db.refresh(invitation)
        
        return InvitationResponse(
            id=invitation.id,
            event_id=invitation.event_id,
            guest_id=invitation.guest_id,
            invitation_token=invitation.invitation_token,
            email_sent=invitation.email_sent,
            sent_at=invitation.sent_at,
            guest_email=guest.email,
            guest_name=f"{guest.first_name} {guest.last_name}",
            event_title=event.title
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear invitación: {str(e)}")

@router.post("/send/{invitation_id}")
async def send_invitation(
    invitation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Enviar una invitación específica por email"""
    try:
        invitation = (
            db.query(Invitation)
            .join(Event)
            .filter(Invitation.id == invitation_id, Event.organizer_id == current_user.id)
            .first()
        )
        if not invitation:
            raise HTTPException(status_code=404, detail="Invitación no encontrada")
        
        # Aquí se implementaría la lógica de envío de email
        # Por ahora solo marcamos como enviada
        invitation.email_sent = True
        invitation.sent_at = datetime.utcnow()
        
        db.commit()
        db.refresh(invitation)
        
        return {"message": "Invitación enviada correctamente", "invitation_id": invitation_id}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al enviar invitación: {str(e)}")

@router.get("/{invitation_token}")
async def get_invitation_by_token(invitation_token: str, db: Session = Depends(get_db)):
    """Obtener invitación por token para página de confirmación"""
    try:
        invitation = db.query(Invitation).filter(
            Invitation.invitation_token == invitation_token
        ).join(Guest).join(Event).first()
        
        if not invitation:
            raise HTTPException(status_code=404, detail="Invitación no encontrada")
        
        return {
            "invitation_id": invitation.id,
            "event": {
                "id": invitation.event.id,
                "title": invitation.event.title,
                "description": invitation.event.description,
                "event_date": invitation.event.event_date,
                "location": invitation.event.location
            },
            "guest": {
                "id": invitation.guest.id,
                "first_name": invitation.guest.first_name,
                "last_name": invitation.guest.last_name,
                "email": invitation.guest.email
            },
            "token": invitation_token
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener invitación: {str(e)}")
