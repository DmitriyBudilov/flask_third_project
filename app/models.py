from flask_security import RoleMixin
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

meals_orders_association = db.Table('meals_orders',
    db.Column('order_id', db.Integer(), db.ForeignKey('orders.id')),
    db.Column('meal_id', db.Integer(), db.ForeignKey('meals.id'))
    )


class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    role = db.Column(db.String(), unique=True)
    users = db.relationship('User')


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    mail = db.Column(db.String(), index=True, nullable=False, unique=True)
    password_hash = db.Column(db.String(), nullable=False)
    
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id'))
    roles = db.relationship('Role')
    orders = db.relationship('Order', back_populates='user')

    def __repr__(self):
        return f'{self.mail}'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Status(db.Model):
    __tablename__ = 'statuses'
    id = db.Column(db.Integer(), primary_key=True)
    status = db.Column(db.String(), nullable=False)
    title = db.Column(db.String(), nullable=False)

    order = db.relationship('Order', back_populates='status')

    def __repr__(self):
        return f'{self.title}'


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), nullable=False)
    
    meals = db.relationship('Meal', back_populates='category')

    def __repr__(self):
        return f'{self.title}'


class Meal(db.Model):
    __tablename__ = 'meals'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    picture = db.Column(db.String(), nullable=False)

    category_id = db.Column(db.Integer(), db.ForeignKey('categories.id'))
    category = db.relationship('Category', back_populates='meals')

    orders = db.relationship('Order', secondary=meals_orders_association, back_populates='meals')


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    name = db.Column(db.String(), nullable=False)
    order_sum = db.Column(db.Integer(), nullable=False)
    mail = db.Column(db.String(), nullable=False)
    phone = db.Column(db.String(), nullable=False)
    address = db.Column(db.String(), nullable=False)
    
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='orders')

    status_id = db.Column(db.Integer(), db.ForeignKey('statuses.id'))
    status = db.relationship('Status', back_populates='order')

    meals = db.relationship('Meal', secondary=meals_orders_association, back_populates='orders')
