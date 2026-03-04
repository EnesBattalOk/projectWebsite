from app import app, db
from models import Project, News, ProjectLink, Visitor, SiteVisit, NewsView

def clear_data():
    with app.app_context():
        try:
            print("Clearing all sample data...")
            # Order matters for foreign keys
            NewsView.query.delete()
            SiteVisit.query.delete()
            Visitor.query.delete()
            ProjectLink.query.delete()
            News.query.delete()
            Project.query.delete()
            
            db.session.commit()
            print("Success: All projects, news, visitors, and views have been deleted.")
        except Exception as e:
            db.session.rollback()
            print(f"Error while clearing data: {e}")

if __name__ == '__main__':
    clear_data()
