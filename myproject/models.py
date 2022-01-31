from myproject import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    # profile_image = db.Column(db.String(20), nullable=False, default ='default_profile.png')
    first_name = db.Column(db.String(20), nullable=False,index=True)
    last_name = db.Column(db.String(20), nullable=False,index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    phone_no = db.Column(db.Integer(), nullable=False, index=True)
    company_name = db.Column(db.String(20), nullable=False, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    # relationship
    projects = db.relationship('Project', backref='project_owner', lazy=True)

    def __init__(self, first_name, last_name, email, phone_no, company_name, username, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_no = phone_no
        self.company_name = company_name
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
            return f"Username {self.username}"

class Project(UserMixin, db.Model):
    __tablename__ = 'projects'

    # users = db.relationship(User)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    project_name = db.Column(db.String(30), nullable=False, index=True) 
    description = db.Column(db.String(200), nullable=True, index=True)
    upload_name = db.Column(db.String(30), nullable=False, index=True)
    video_name = db.Column(db.String(30), nullable=False, index=True)
    video_format = db.Column(db.String(5), nullable=False, index=True)
    video_size = db.Column(db.String(5), nullable=False, index=True)
    select_gpu = db.Column(db.String(4), nullable=False, index=True)
    compute_hrs = db.Column(db.Integer(), nullable=True, index=True)

    # relationship
    jobs = db.relationship('Job', backref='redis_job', lazy=True)
    
    def __init__(self, user_id, project_name, description, upload_name, video_name, video_format, video_size, select_gpu, compute_hrs):
        self.user_id = user_id
        self.project_name = project_name
        self.description = description
        self.upload_name = upload_name
        self.video_name = video_name
        self.video_format = video_format
        self.video_size = video_size
        self.select_gpu = select_gpu
        self.compute_hrs = compute_hrs

# test table jobs
class Job(UserMixin, db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    current_project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False, index=True)
    job_id = db.Column(db.String(30), nullable=False, index=True)
    status = db.Column(db.String(15), nullable=False)

    def __init__(self, current_project_id, job_id, status):
        self.current_project_id = current_project_id
        self.job_id = job_id
        self.status = status



