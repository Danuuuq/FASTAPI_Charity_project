from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.abstract import AbstractModel


class Donation(AbstractModel):
    user_id = Column(Integer, ForeignKey(
        'user.id', name='fk_donation_user_id_user'))
    comment = Column(Text, nullable=True)
