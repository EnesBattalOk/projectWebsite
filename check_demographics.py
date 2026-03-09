import os
from flask import Flask
from models import db, Visitor

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'projects.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    visitors = Visitor.query.all()
    print(f"Total visitors recorded: {len(visitors)}")
    countries = {}
    for v in visitors:
        countries[v.country] = countries.get(v.country, 0) + 1
    
    print("\nCountry Distribution:")
    for country, count in countries.items():
        print(f"{country}: {count}")
