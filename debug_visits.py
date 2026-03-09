import os
from flask import Flask
from models import db, Visitor, SiteVisit
from datetime import datetime

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'projects.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    print(f"Current UTC time: {datetime.utcnow()}")
    print(f"Current Date: {datetime.utcnow().date()}")
    
    visitors = Visitor.query.all()
    print(f"\nVisitors ({len(visitors)}):")
    for v in visitors:
        print(f"ID: {v.id}, IP: {v.ip_address}, Country: {v.country}, First Visit: {v.first_visit}")
        
    visits = SiteVisit.query.all()
    print(f"\nSite Visits ({len(visits)}):")
    for v in visits:
        print(f"ID: {v.id}, Visitor ID: {v.visitor_id}, Date: {v.date_visited}")
