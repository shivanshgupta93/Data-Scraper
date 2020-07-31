from sqlalchemy import Column, Integer, String, Date, Float
from models.base import Base
import datetime

#### Product class to create Product table
class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    product_id = Column(String)
    product_name = Column(String)
    product_price = Column(String)
    review_count = Column(Integer)
    seller = Column(String)
    availability = Column(String)
    insert_date = Column(Date(), default=datetime.datetime.now().date())

    def __repr__(self):
        return "<Title (product_id='%s', product_name='%s', product_price='%s', review_count='%d', seller='%s', availability='%s', inserted_date='%s' )" % (self.product_id, self.product_name, self.product_price, self.review_count, self.seller, self.availability, self.inserted_date)
