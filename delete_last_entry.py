from app import app
from models import db, WaterSavingEntry

with app.app_context():
    last = WaterSavingEntry.query.order_by(WaterSavingEntry.id.desc()).first()
    if last:
        name = last.student_name
        db.session.delete(last)
        db.session.commit()
        print(f"Deleted last entry: {name}")
    else:
        print("No entries to delete.")
