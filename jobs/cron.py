import datetime
from db import DB
from models.category import Category
from models.feature import Feature
from models.product import Product
from middlewares.serializer import serialize

db_obj = DB() ### creating a object of DB function in db.py file
db_session = db_obj.get_db() ### getting a session of database

def cron_job(productjson):
    product_id = db_session.query(Product).filter(Product.product_name == productjson['title']).first() ###checking whether the product already exists in the database

    if product_id is None:  ### if the product doesn't exists then add fields in all the tables

        db_session.add_all([Product(product_id=productjson['id'], product_name=productjson['title'], 
                                    product_price=productjson['price'], review_count=productjson['review_count'], 
                                    seller=productjson['seller'], availability=productjson['availability'])])

        for category in productjson['categories']:
            db_session.add_all([Category(product_id=productjson['id'], category=category)])

        for feature in productjson['features']:
            db_session.add_all([Feature(product_id=productjson['id'], feature=feature)])

    if product_id is not None: ### if the product does exists then update fields in all Product table and delete/insert in rest tables

        db_session.query(Product).filter(Product.product_name == productjson['title']).update({Product.product_price:productjson['price'],
        Product.review_count:productjson['review_count'], Product.seller:productjson['seller'], 
        Product.availability:productjson['availability'],
        Product.insert_date: datetime.datetime.now().date()}, synchronize_session = False)  ###Updating Product table

        db_session.query(Category).filter(Category.product_id == product_id.product_id).delete()  ### Deleting from Category Table

        for category in productjson['categories']:
            db_session.add_all([Category(product_id=productjson['id'], category=category)])

        db_session.query(Feature).filter(Feature.product_id == product_id.product_id).delete()  ### Deleting from Feature table

        for feature in productjson['features']:
            db_session.add_all([Feature(product_id=productjson['id'], feature=feature)])

    db_session.commit()

def get_product_data():
    product_colums = Product.__table__.columns.keys()  ## Getting column names
    product = db_session.query(Product).all() ## Getting all rows of the table
    return product_colums, serialize(product)


def get_categories_data():
    category_colums = Category.__table__.columns.keys() ## Getting column names
    category = db_session.query(Category).all() ## Getting all rows of the table
    return category_colums, serialize(category)

def get_features_data():
    feature_colums = Feature.__table__.columns.keys() ## Getting column names
    feature = db_session.query(Feature).all() ## Getting all rows of the table
    return feature_colums, serialize(feature)
