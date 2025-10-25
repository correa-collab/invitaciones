from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.connection import Base

# Association table for many-to-many relationship between events and guests
event_guests = Table(
    'event_guests',
    Base.metadata,
    Column('event_id', Integer, ForeignKey('events.id'), primary_key=True),
    Column('guest_id', Integer, ForeignKey('guests.id'), primary_key=True)
)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    events = relationship("Event", back_populates="organizer")

class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    event_date = Column(DateTime, nullable=False)
    location = Column(String, nullable=False)
    max_guests = Column(Integer, default=100)
    is_active = Column(Boolean, default=True)
    organizer_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    organizer = relationship("User", back_populates="events")
    guests = relationship("Guest", secondary=event_guests, back_populates="events")
    invitations = relationship("Invitation", back_populates="event")

class Guest(Base):
    __tablename__ = "guests"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone = Column(String)
    company = Column(String)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    events = relationship("Event", secondary=event_guests, back_populates="guests")
    invitations = relationship("Invitation", back_populates="guest")

class Invitation(Base):
    __tablename__ = "invitations"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    guest_id = Column(Integer, ForeignKey("guests.id"))
    invitation_token = Column(String, unique=True, nullable=False)
    sent_at = Column(DateTime(timezone=True))
    email_sent = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    event = relationship("Event", back_populates="invitations")
    guest = relationship("Guest", back_populates="invitations")
    confirmation = relationship("Confirmation", back_populates="invitation", uselist=False)

class Confirmation(Base):
    __tablename__ = "confirmations"
    
    id = Column(Integer, primary_key=True, index=True)
    invitation_id = Column(Integer, ForeignKey("invitations.id"))
    will_attend = Column(Boolean, nullable=False)
    additional_guests = Column(Integer, default=0)
    dietary_requirements = Column(Text)
    special_requests = Column(Text)
    confirmed_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    invitation = relationship("Invitation", back_populates="confirmation")