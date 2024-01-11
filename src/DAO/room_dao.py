import uuid

from sqlalchemy import Column, String, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from src.DAO.base import Base


class RoomDAO(Base):
    __tablename__ = 'rooms'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    storey_id = Column(UUID(as_uuid=True), ForeignKey('storeys.id'))
    deleted_at = Column(Date)

    def __init__(self, name, storey_id, deleted_at):
        self.name = name
        self.storey_id = storey_id
        self.deleted_at = deleted_at
