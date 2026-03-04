import os
import json
import urllib.request
import re
from flask import request
from werkzeug.utils import secure_filename
from datetime import datetime
from models import db, Visitor, SiteVisit

def handle_file_upload(file_obj, upload_folder, custom_name=None):
    if file_obj and file_obj.filename:
        ext = os.path.splitext(file_obj.filename)[1]
        if custom_name:
            filename = f"{secure_filename(custom_name)}{ext}"
        else:
            filename = secure_filename(file_obj.filename)
        
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
            
        file_obj.save(os.path.join(upload_folder, filename))
        return filename
    return None

def get_or_create_visitor():
    ip = request.remote_addr
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0]
        
    visitor = Visitor.query.filter_by(ip_address=ip).first()
    if not visitor:
        country = 'Local Network'
        if ip and ip not in ['127.0.0.1', '::1', 'localhost']:
            try:
                # Use a free geolocation API
                req = urllib.request.urlopen(f'http://ip-api.com/json/{ip}?fields=country', timeout=2)
                data = json.loads(req.read().decode('utf-8'))
                if data and 'country' in data:
                    country = data['country']
            except:
                country = 'Unknown'
        
        visitor = Visitor(ip_address=ip, country=country)
        db.session.add(visitor)
        db.session.commit()
    return visitor

def track_site_visit():
    visitor = get_or_create_visitor()
    today = datetime.utcnow().date()
    visit = SiteVisit.query.filter_by(visitor_id=visitor.id, date_visited=today).first()
    if not visit:
        visit = SiteVisit(visitor_id=visitor.id, date_visited=today)
        db.session.add(visit)
        db.session.commit()
    return visitor

def strip_html(html_content):
    if not html_content:
        return ""
    # Remove HTML tags
    text = re.sub('<[^<]+?>', '', html_content)
    # Remove extra whitespaces
    text = ' '.join(text.split())
    return text
