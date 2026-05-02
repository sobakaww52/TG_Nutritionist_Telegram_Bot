from datetime import datetime
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from typing import Optional

class Broadcast(SQLModel, table=True):
    id: UUID = Field(
        default_factory=uuid4, 
        primary_key=True,
        index=True,
        nullable=False
    )
    text: Optional[str] = Field(default=None, description="Текст рассылки")
    media_type: str = Field(default="text", description="text, photo, video")
    file_id: Optional[str] = Field(default=None, description="TG File ID")
    created_at: datetime = Field(default_factory=datetime.now)
    is_sent: bool = Field(default=False)