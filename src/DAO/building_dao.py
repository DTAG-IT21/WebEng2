import uuid

from sqlalchemy import Column, String, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from src.DAO.base import Base


class BuildingDAO(Base):
    __tablename__ = 'buildings'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    address = Column(String)
    deleted_at = Column(Date)

    def __init__(self, name, address, deleted_at):
        self.name = name
        self.address = address
        self.deleted_at = deleted_at