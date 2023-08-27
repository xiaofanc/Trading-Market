# Flask - Trading market
Create a virtual environment named "venv"
```
python -m venv venv
source venv/bin/activate
```

set flask app
`export FLASK_APP=market.py` \
set debug mode on, so we don't have to restart the app for every change
`export FLASK_DEBUG=1` \
run the app
`flask run`

install sqlalchemy
```
pip3 install flask-sqlalchemy
# create database
>>> python3
>>> from market import db
>>> db.create_all()
>>> from market import Item
>>> item1 = Item(name="Phone 10", barcode="893212299897", price="500", description="mobile phone")
>>> db.session.add(item1)
>>> db.session.commit()
>>> Item.query.all()
>>> for item in Item.query.all():
...     item.name
...     item.price
>>> for item in Item.query.filter_by(price=500):
...     item.name
```

templates directory: store all html files

bootstrap starter template: styling framework
https://getbootstrap.com/docs/4.5/getting-started/introduction/

Jinja syntax: allow access the parameters sent by the router

template inheritance: put common html code into one base template, then {% extends 'base.html' %} to use it

DB Browser for SQLite
https://sqlitebrowser.org/blog/version-3-12-2-released/

reconstructure:
- add python files to the market package
- add __init__ file for the app
```
# run the app after reconstructure
python3 run.py

# update models
>>> python3
>>> from market.models import db
>>> db.drop_all()
>>> db.create_all()
>>> from market.models import Item, User
>>> u1 = User(username='jsc', password_hash='123456', email_address='jsc@gmail.com')
>>> db.session.add(u1)
>>> db.session.commit()
>>> User.query.all()
>>> item1 = Item(name="Phone 10", barcode="893212299897", price="500", description="mobile phone")
>>> db.session.add(item1)
>>> db.session.commit()
>>> item2 = Item(name="Phone max", barcode="8932234567", price="700", description="mobile phone 2")
>>> db.session.add(item2)
>>> db.session.commit()
>>> Item.query.all()
[item=Phone 10, item=Phone max]
>>> i1 = Item.query.filter_by(name='Phone 10')
>>> i1
<flask_sqlalchemy.query.Query object at 0x1124535e0>
>>> i1.first()
item=Phone 10
>>> i1 = Item.query.filter_by(name='Phone 10').first()
>>> i1.owner = User.query.filter_by(username='jsc').first().id
>>> db.session.add(i1)
>>> db.session.commit()
>>> i1.owner
1
>>> i1.owned_user
<User 1>
```

add register page
```
pip3 install flask-wtf
```

generate hexadecimal random character as SECRET_KEY when user submits register form
```
>>> python3
>>> import os
>>> os.urandom(12).hex()
'f595e088df5d3e1cc981fa8d'
```

install email validation support
```
pip3 install email_validator
```

flash error messages when validation is wrong during register
```
{% with messages = get_flashed_messages(with_categories=true) %}
{% if messages %}
{% for category, message in messages %}
<div class="alert alert-{{ category }}">
    <button type="button" class="m1-2 mb-1 close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
    </button>
    {{ message }}
</div>
{% endfor %}
{% endif %}
{% endwith %}
```

capture the error if usename or email is not unique using ValidationError
```
def validate_username(self, username_to_check):
    user = User.query.filter_by(username=username_to_check.data).first()
    if user:
        raise ValidationError('Username already exists! Please try a different username')

```

store encrypted password instead
```
pip3 install flask_bcrypt
# create a bcrypt instance in the init file
# set the password property in the User model
```

add login page, create a login manager for the app
```
pip3 install flask_login
```

define a method to check if the password is matched with the hashed password in the model
```
def check_password(self, attempted_password):
    return bcrypt.check_password_hash(self.password_hash, attempted_password)
```

make sure every page knows about the login user
```
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Inherit from a class (UserMixin) that provides default implementations for the methods that Flask-Login expects user objects to have.
```

optimize the navbar if the user is logged in
```
{% if current_user.is_authenticated %}
    # show welcom message and budget
    # show log out button
{% else %}
    # show log in button
    # show register button
{% endif %}
```

add logout page && redirect to the home page

login required to see the market page && add login automatically after registeration
```
add decorator @login_required in the market route
add following in the init:
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"
```

divide the market into two parts
https://getbootstrap.com/docs/4.0/layout/grid/

add modal for buttons (popup window)
https://getbootstrap.com/docs/4.0/components/modal/

pusrchase item
- create a new form for purchasing items
- add form to modal
- if you want to print the purchase_form after submitting the purchase:
```
    print(purchase_form.__dict__)
    print(purchase_form['submit'])
```
- get the purchased item from request.form
    `purchased_item = request.form.get('purchased_item')`
- add ownership of the purchase
- remove item which is purchased from the market

add my items page to sell items
- display the owned items as cards
- create a new form for selling items
- add form to modal
- to trigger a modal, we include the modal in html
- get the selling item from request.form



