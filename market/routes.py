from market import app
from flask import render_template, redirect, url_for, flash, request
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from market import db
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    # submit the form only when the method is POST
    if request.method == 'POST':
        purchased_item = request.form.get('purchased_item')
        item = Item.query.filter_by(name=purchased_item).first()
        if item:
            # assign ownership of purchase
            if current_user.can_purchase(item):
                item.buy(current_user)
                flash(f"Congratulations! You purchased {item.name} for ${item.price} !!", category="success")
            else:
                flash(f"Unfortunately, you do not have enough money to purchase {item.name}", category="danger")
        return redirect(url_for('market_page'))
    
    # prevent resubmission of form after refresh
    if request.method == "GET":
        # remove item with owner
        items = Item.query.filter_by(owner=None)
        return render_template('market.html', items=items, purchase_form=purchase_form)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('market_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))

@app.route('/myitems', methods=['GET', 'POST'])
@login_required
def items_page():
    selling_form = SellItemForm()
    if request.method == "POST":
        sold_item = request.form.get('sold_item')
        item = Item.query.filter_by(name=sold_item).first()
        if item:
            # remove ownership of the item
            if current_user.can_sell(item):
                item.sell(current_user)
                flash(f"Congratulations! You sold {item.name} for ${item.price} !!", category="success")
            else:
                flash(f"Something wrong with selling {item.name}", category="danger")
        return redirect(url_for('market_page'))
    if request.method == "GET":
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template('myitems.html', owned_items=owned_items, selling_form=selling_form)







