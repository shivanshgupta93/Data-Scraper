from sqlalchemy import Column, Integer, String, Date, Float
from models.base import Base
import datetime

#### Category class to create Category table
class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    product_id = Column(String)
    category = Column(String)
    insert_date = Column(Date(), default=datetime.datetime.now().date())

    def __repr__(self):
        return "<Title (product_id='%s', category='%s', inserted_date='%s' )" % (self.product_id, self.category, self.inserted_date)