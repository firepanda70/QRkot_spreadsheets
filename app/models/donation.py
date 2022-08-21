from sqlalchemy import Column, Integer, Text, ForeignKey

from .charity_base import CharityBase


class Donation(CharityBase):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
