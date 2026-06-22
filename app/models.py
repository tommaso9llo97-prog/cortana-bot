import enum
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON, Enum, Index, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class UserStateEnum(str, enum.Enum):
    IDLE = "idle"
    FOCUS = "focus"
    BREAK = "break"
    PROCRASTINATION = "procrastination"

class ConversationRole(str, enum.Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class DeviceEventType(str, enum.Enum):
    APP_USAGE = "app_usage"
    LOCATION = "location"
    BATTERY = "battery"
    SCREEN = "screen"
    PROCRASTINATION = "procrastination"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String, unique=True, index=True, nullable=False)
    is_owner = Column(Boolean, default=False, nullable=False)
    current_state = Column(Enum(UserStateEnum), default=UserStateEnum.IDLE, nullable=False)
    summary_context = Column(Text, nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")
    device_events = relationship("DeviceEvent", back_populates="user", cascade="all, delete-orphan")

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role = Column(Enum(ConversationRole), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", back_populates="conversations")

class DeviceEvent(Base):
    __tablename__ = "device_events"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    event_type = Column(Enum(DeviceEventType), nullable=False)
    payload = Column(JSON, nullable=False)
    idempotency_key = Column(String(64), nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="device_events")

    __table_args__ = (
        UniqueConstraint('user_id', 'idempotency_key', name='uq_device_events_user_idempotency'),
        Index("idx_device_events_user_time", "user_id", "timestamp"),
    )