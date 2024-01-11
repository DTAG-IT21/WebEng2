import uuid

from sqlalchemy import Column, String, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from src.DAO.base import Base


class StoreyDAO(Base):
    __tablename__ = 'storeys'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    building_id = Column(UUID(as_uuid=True), ForeignKey('buildings.id'))
    deleted_at = Column(Date)

    def __init__(self, name, building_id, deleted_at):
        self.id = uuid.uuid4()
        self.name = name
        self.building_id = building_id
        self.deleted_at = deleted_at
        