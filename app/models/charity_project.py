from sqlalchemy import Column, String, Text

from app.core.config import settings
from app.models.abstract import AbstractModel


class CharityProject(AbstractModel):
    name = Column(String(settings.MAX_LENGTH_NAME),
                  unique=True, nullable=False)
    description = Column(Text, unique=True, nullable=False)
