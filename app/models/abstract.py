from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, Integer

from app.core.db import Base
from app.core.config import settings


class AbstractModel(Base):
    __abstract__ = True

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=settings.DEFAULT_AMOUNT,
                             nullable=False)
    fully_invested = Column(Boolean, default=False, nullable=False)
    create_date = Column(DateTime, default=lambda: datetime.now(timezone.utc),
                         nullable=False)
    close_date = Column(DateTime, nullable=True)
