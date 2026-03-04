"""
PythonAnywhere'de admin şifresini sıfırlamak için bu scripti çalıştır:

    python reset_admin.py

Bu script mevcut admin kullanıcısını siler ve yeniden oluşturur.
"""

from app import create_app
from models import db, User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    db.create_all()

    # Mevcut admin'i sil
    existing = User.query.filter_by(username='admin').first()
    if existing:
        db.session.delete(existing)
        db.session.commit()
        print("Eski admin kullanıcısı silindi.")

    # Yeni admin oluştur
    admin = User(
        username='admin',
        password=generate_password_hash('kozluca')
    )
    db.session.add(admin)
    db.session.commit()
    print("Admin kullanıcısı başarıyla oluşturuldu!")
    print("Kullanici adi: admin")
    print("Sifre: kozluca")
