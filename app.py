import os
import json
import traceback
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func

# Local imports
from config import Config
from models import db, User, Project, News, ProjectLink, Visitor, SiteVisit, NewsView, WaterSavingEntry
from utils import handle_file_upload, track_site_visit, strip_html

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Veritabanı Yolu (Absolute Path) - Disk I/O ve no such table hatalarını çözmek için:
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'projects.db')

    # Ensure Instance & Upload folders exist
    os.makedirs(os.path.join(basedir, 'instance'), exist_ok=True)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Initialize Extensions
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # --- Register Context Processors ---
    @app.context_processor
    def inject_projects():
        # This makes all_projects available in every template (useful for navbar)
        return dict(all_projects=Project.query.all())

    # --- Public Routes ---
    @app.route('/')
    def index():
        track_site_visit()
        project = Project.query.filter_by(is_default=True).first()
        if not project:
            project = Project.query.first()
        
        news_items = News.query.filter_by(project_id=project.id).order_by(News.date_posted.desc()).all() if project else []
        return render_template('index.html', current_project=project, news_items=news_items)

    @app.route('/project/<slug>')
    def view_project(slug):
        track_site_visit()
        project = Project.query.filter_by(slug=slug).first_or_404()
        news_list = News.query.filter_by(project_id=project.id).order_by(News.date_posted.desc()).all()
        return render_template('index.html', current_project=project, news_items=news_list)

    @app.route('/news/<int:news_id>')
    def view_news(news_id):
        news_item = News.query.get_or_404(news_id)
        
        # Track News Views
        visitor = track_site_visit()
        view = NewsView.query.filter_by(news_id=news_id, visitor_id=visitor.id).first()
        if not view:
            view = NewsView(news_id=news_id, visitor_id=visitor.id, date_viewed=datetime.utcnow().date())
            db.session.add(view)
            db.session.commit()
            
        return render_template('news_detail.html', news=news_item)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('admin_dashboard'))
        
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            user = User.query.filter_by(username=username).first()
            
            if user and check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Invalid username or password', 'danger')
                
        return render_template('admin/login.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))

    # --- Admin Routes ---
    @app.route('/admin')
    @login_required
    def admin_dashboard():
        projects = Project.query.all()
        return render_template('admin/dashboard.html', projects=projects)

    @app.route('/admin/statistics')
    @login_required
    def admin_statistics():
        today = datetime.utcnow().date()
        daily_visitors = db.session.query(func.count(func.distinct(SiteVisit.visitor_id))).filter_by(date_visited=today).scalar() or 0
        this_month = today.replace(day=1)
        monthly_visitors = db.session.query(func.count(func.distinct(SiteVisit.visitor_id))).filter(SiteVisit.date_visited >= this_month).scalar() or 0
        total_visitors = Visitor.query.count() or 0

        countries = db.session.query(Visitor.country, func.count(Visitor.id)).group_by(Visitor.country).order_by(func.count(Visitor.id).desc()).all()
        country_labels = [c[0] for c in countries]
        country_data = [c[1] for c in countries]

        news_views = db.session.query(
            Project.name, News.title, func.count(func.distinct(NewsView.visitor_id)).label('views')
        ).join(News, Project.id == News.project_id).outerjoin(NewsView, News.id == NewsView.news_id).group_by(News.id).order_by(db.text('views DESC')).all()

        return render_template('admin/statistics.html', 
            daily=daily_visitors, monthly=monthly_visitors, yearly=0, total=total_visitors,
            country_labels=country_labels, country_data=country_data, news_views=news_views
        )

    @app.route('/admin/project/new', methods=['GET', 'POST'])
    @login_required
    def new_project():
        if request.method == 'POST':
            name, subtitle, description = request.form.get('name'), request.form.get('subtitle'), request.form.get('description')
            slug = name.lower().replace(' ', '-')
            
            logo_filename = handle_file_upload(request.files.get('logo'), app.config['UPLOAD_FOLDER'], request.form.get('logo_name'))
            logo2_filename = handle_file_upload(request.files.get('logo2'), app.config['UPLOAD_FOLDER'], request.form.get('logo2_name'))
            
            project = Project(name=name, slug=slug, subtitle=subtitle, description=description, logo=logo_filename, logo2=logo2_filename, logo_size=request.form.get('logo_size', 80, type=int))
            db.session.add(project)
            db.session.commit()
            flash('Project created successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        return render_template('admin/edit_project.html', project=None)

    @app.route('/admin/project/edit/<int:id>', methods=['GET', 'POST'])
    @login_required
    def edit_project(id):
        project = Project.query.get_or_404(id)
        if request.method == 'POST':
            project.name, project.subtitle, project.description = request.form.get('name'), request.form.get('subtitle'), request.form.get('description')
            project.logo_size = request.form.get('logo_size', 80, type=int)
            
            if request.files.get('logo'): 
                project.logo = handle_file_upload(request.files.get('logo'), app.config['UPLOAD_FOLDER'], request.form.get('logo_name'))
            if request.files.get('logo2'): 
                project.logo2 = handle_file_upload(request.files.get('logo2'), app.config['UPLOAD_FOLDER'], request.form.get('logo2_name'))

            db.session.commit()
            flash('Project updated!', 'success')
            return redirect(url_for('admin_dashboard'))
        return render_template('admin/edit_project.html', project=project)

    @app.route('/admin/project/set_default/<int:id>')
    @login_required
    def set_default_project(id):
        Project.query.update({Project.is_default: False})
        Project.query.get_or_404(id).is_default = True
        db.session.commit()
        return redirect(url_for('admin_dashboard'))

    @app.route('/admin/project/delete/<int:id>')
    @login_required
    def delete_project(id):
        project = Project.query.get_or_404(id)
        db.session.delete(project)
        db.session.commit()
        flash('Project deleted.', 'success')
        return redirect(url_for('admin_dashboard'))

    @app.route('/admin/news/new/<int:project_id>', methods=['GET', 'POST'])
    @login_required
    def add_news(project_id):
        project = Project.query.get_or_404(project_id)
        if request.method == 'POST':
            content = request.form.get('content')
            clean_text = strip_html(content)
            news = News(
                project_id=project.id,
                title=clean_text[:60].strip() + ("..." if len(clean_text) > 60 else ""),
                summary=clean_text[:160].strip() + ("..." if len(clean_text) > 160 else ""),
                content=content,
                image=handle_file_upload(request.files.get('image'), app.config['UPLOAD_FOLDER'], request.form.get('image_name')),
                external_link=request.form.get('link')
            )
            db.session.add(news)
            db.session.commit()
            return redirect(url_for('admin_dashboard'))
        return render_template('admin/news_form.html', project=project)

    @app.route('/admin/news/edit/<int:id>', methods=['GET', 'POST'])
    @login_required
    def edit_news(id):
        news = News.query.get_or_404(id)
        if request.method == 'POST':
            news.content = request.form.get('content')
            clean_text = strip_html(news.content)
            news.title = clean_text[:60].strip() + ("..." if len(clean_text) > 60 else "")
            news.summary = clean_text[:160].strip() + ("..." if len(clean_text) > 160 else "")
            news.external_link = request.form.get('link')
            if request.files.get('image'):
                news.image = handle_file_upload(request.files.get('image'), app.config['UPLOAD_FOLDER'], request.form.get('image_name'))
            db.session.commit()
            return redirect(url_for('admin_dashboard'))
        return render_template('admin/news_form.html', project=news.project, news=news)

    @app.route('/admin/news/delete/<int:id>')
    @login_required
    def delete_news(id):
        news = News.query.get_or_404(id)
        db.session.delete(news)
        db.session.commit()
        return redirect(url_for('admin_dashboard'))

    @app.route('/admin/link/add/<int:project_id>', methods=['GET', 'POST'])
    @login_required
    def add_link(project_id):
        project = Project.query.get_or_404(project_id)
        if request.method == 'POST':
            link = ProjectLink(
                project_id=project.id,
                title=request.form.get('title'),
                url=request.form.get('url')
            )
            db.session.add(link)
            db.session.commit()
            return redirect(url_for('admin_dashboard'))
        return render_template('admin/link_form.html', project=project)

    @app.route('/admin/link/delete/<int:id>')
    @login_required
    def delete_link(id):
        link = ProjectLink.query.get_or_404(id)
        db.session.delete(link)
        db.session.commit()
        return redirect(url_for('admin_dashboard'))

    @app.route('/water-diary')
    def water_diary():
        entries = WaterSavingEntry.query.order_by(WaterSavingEntry.created_at.desc()).limit(20).all()
        return render_template('water_diary.html', entries=entries)

    @app.route('/api/save-water-entry', methods=['POST'])
    def save_water_entry():
        try:
            data = request.get_json()
            entry = WaterSavingEntry(
                student_name=data.get('studentName', 'Anonymous'),
                school_name=data.get('schoolName', ''),
                teacher_name=data.get('teacherName', ''),
                family_size=int(data.get('familySize', 4)),
                total_consumption=float(data.get('totalConsumption', 0)),
                month_data=json.dumps(data.get('monthData', [])),
                suggestions=json.dumps(data.get('suggestions', []))
            )
            db.session.add(entry)
            db.session.commit()
            return jsonify({'success': True, 'id': entry.id})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 400

    # Error Handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        error_details = traceback.format_exc()
        return f"<h1>500 Server Error</h1><h3>Lütfen bu ekranın fotoğrafını at:</h3><pre>{error_details}</pre>", 500

    return app

def seed_db():
    if User.query.count() == 0:
        admin_user = User(username='admin', password=generate_password_hash('kozluca'))
        db.session.add(admin_user)
        db.session.commit()
        print("Admin user created.")

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_db()
    app.run(debug=True)
