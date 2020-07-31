from sqlalchemy import Column, Integer, String, Date, Float
from models.base import Base
import datetime

#### Feature class to create Feature table
class Feature(Base):
    __tablename__ = 'feature'

    id = Column(Integer, primary_key=True)
    product_id = Column(String)
    feature = Column(String)
    insert_date = Column(Date(), default=datetime.datetime.now().date())

    def __repr__(self):
        return "<Title (product_id='%s', feature='%s', inserted_date='%s' )" % (self.product_id, self.feature, self.inserted_date)
