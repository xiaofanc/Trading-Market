# Flask - Trading market
```
# Create a virtual environment named "venv"
python -m venv venv
source venv/bin/activate

# set flask app
export FLASK_APP=market.py
# set debug mode
export FLASK_DEBUG=1
# run the app
flask run

# install sqlalchemy
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
add python files to the market package

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

add register html
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