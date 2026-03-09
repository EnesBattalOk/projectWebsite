from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    subtitle = db.Column(db.String(200))
    description = db.Column(db.Text)
    logo = db.Column(db.String(500))
    logo2 = db.Column(db.String(500)) # Second optional logo
    logo_size = db.Column(db.Integer, default=80)
    is_default = db.Column(db.Boolean, default=False)
    news_items = db.relationship('News', backref='project', lazy=True, cascade="all, delete-orphan")
    links = db.relationship('ProjectLink', backref='project', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Project {self.name}>'

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    summary = db.Column(db.String(500))
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(500))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    external_link = db.Column(db.String(500))

    def __repr__(self):
        return f'<News {self.title}>'

class ProjectLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f'<ProjectLink {self.title}>'

class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(100), unique=True, nullable=False)
    country = db.Column(db.String(100), default='Unknown')
    first_visit = db.Column(db.DateTime, default=datetime.utcnow)

class SiteVisit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    visitor_id = db.Column(db.Integer, db.ForeignKey('visitor.id'), nullable=False)
    date_visited = db.Column(db.Date, nullable=False, default=lambda: datetime.utcnow().date())

class NewsView(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    news_id = db.Column(db.Integer, db.ForeignKey('news.id'), nullable=False)
    visitor_id = db.Column(db.Integer, db.ForeignKey('visitor.id'), nullable=False)
    date_viewed = db.Column(db.Date, nullable=False, default=lambda: datetime.utcnow().date())

class WaterSavingEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(200), nullable=False)
    school_name = db.Column(db.String(200), default='')
    teacher_name = db.Column(db.String(200), default='')
    family_size = db.Column(db.Integer, default=4)
    total_consumption = db.Column(db.Float, default=0.0)
    month_data = db.Column(db.Text, default='[]')
    bill_images = db.Column(db.Text, default='[]')
    suggestions = db.Column(db.Text, default='[]')
    school_logo = db.Column(db.String(500), default='')
    student_avatar = db.Column(db.String(500), default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
