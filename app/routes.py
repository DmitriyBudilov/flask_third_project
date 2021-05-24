import csv

from flask import request, render_template, redirect, url_for, session, flash
from flask_login import current_user, login_required, login_user, logout_user

from app.forms import *
from app.models import *
from app import app, db, login_manager

login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/process_login/', methods=['POST'])
def process_login():
    form = Login()
    print('test1')
    if form.validate_on_submit():
        print('test2')
        user = User.query.filter_by(mail=form.mail.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Пользователь авторизован!')
            return redirect(url_for('index'))
    flash('Неправильное имя или пароль!')
    return redirect(url_for('login'))


@app.route('/')
def index():
    # if session.get('cart') == None:
        # session['cart'] = []
    # session.pop('cart')
    # print(session.get('cart'))
    cart = session.get('cart', [])
    session['cart'] = cart
    categories = Category.query.all()
    meals = Meal.query.all()
    # print(session['cart'])
    return render_template('main.html', meals=meals, categories=categories)


@app.route('/add_to_cart/<int:meal_id>/<int:meal_price>', methods=['GET'])
def add_to_cart(meal_id, meal_price):
    cart = session.get('cart', [])
    cart.append({'id': meal_id, 'price': meal_price})
    session['cart'] = cart
    return redirect(url_for('index'))


@app.route('/cart/', methods=['GET', 'POST'])
def render_cart():
    form = OrderForm()
    cart = [ item['id'] for item in session['cart'] ]
    cart_session = Meal.query.filter(Meal.id.in_(cart)).all()
    return render_template('cart.html', cart_session=cart_session, form=form)

@app.route('/del_from_cart/<int:id>')
def del_from_cart(id):
    cart = session.get('cart')
    cart = [item for item in cart if not (item['id'] == id)]
    session['cart'] = cart
    return redirect(url_for('render_cart'))


@app.route('/account/')
def account():
    return render_template('account.html')


@app.route('/login/', methods=["GET", "POST"])
def login():
    form = Login()
    print(request.base_url)
    if request.method == "POST":
        if form.validate_on_submit: 
            user = User.query.filter_by(mail=form.mail.data).first()
            if user and user.check_password(form.password.data):
                return redirect(url_for('index'))

    return render_template('login.html', form=form)


@app.route('/registration/', methods=['GET', 'POST'])
def registration():
    form = Registration()

    if request.method == "POST":
        if form.validate_on_submit:
            if not User.query.filter_by(mail=form.mail.data).first():
                user = User(mail=form.mail.data, roles=Role.query.get(2))
                user.set_password(form.password.data)
                db.session.add(user)
                db.session.commit()
                flash('Вы зарегистрированы. Теперь можете войти!')
                return redirect(url_for('index'))
            else:
                flash('Такой пользователь уже зарегистрирован!')

    return render_template('register.html', form=form)

@app.route('/logout/')
def logout():
    logout_user()
    flash('Вы успешно разлогинились!')
    return redirect(url_for('index'))


@app.route('/ordered/<int:order_sum>', methods=['POST'])
def ordered(order_sum):
    form = OrderForm()
    if form.validate_on_submit():
        order_ids = [ item['id'] for item in session['cart'] ]
        order = Order(name=form.name.data, mail=form.mail.data, phone=form.phone.data, address=form.address.data, order_sum=order_sum, status=Status.query.filter_by(status='preparing').first())
        meals = Meal.query.filter(Meal.id.in_(order_ids)).all()
        order.user = current_user
        order.meals = meals
        # order.status = 
        print(order.status)
        db.session.add(order)
        db.session.commit()
        session.pop('cart')
        
        # print(name, address, mail, tel)
        return render_template('ordered.html')


@app.route('/db_generator/')
def db_generator():
    with open('delivery_categories.csv') as file:
        reader = csv.DictReader(file)
        categories = [item for item in reader]

    for item in categories:
        category = Category(title=item['title'])
        db.session.add(category)
    db.session.commit()

    with open('delivery_items.csv') as file:
        reader = csv.DictReader(file)
        meals = [item for item in reader]

    for item in meals:
        meal = Meal(title=item['title'],
                    price=item['price'], 
                    description=item['description'], 
                    picture=item['picture'], 
                    category=Category.query.filter_by(id=int(item['category_id'])).first())
        db.session.add(meal)

    statuses = [{'status': 'preparing', 'title': 'Готовится'}, 
                {'status': 'on_the_way', 'title': 'В пути'},
                {'status': 'redy', 'title': 'Выполнен'}
                ]

    roles = ['admin', 'user']

    for item in statuses:
        status = Status(status=item['status'], title=item['title'])
        db.session.add(status)

    for item in roles:
        role = Role(role=item)
        db.session.add(role)

    db.session.commit()

    return redirect(url_for('index'))