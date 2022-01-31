from flask_login import login_user, current_user, logout_user, login_required
from flask import Flask, render_template, Blueprint, redirect, flash, url_for, request, session
from redis import RedisError
from myproject import db, app
from werkzeug.utils import secure_filename
# import model
from myproject.project.forms import ProjectForm
from myproject.models import Project, Job
import time
import os
import shutil

# from myproject.project.training import current_job_id
from myproject import r, q
from rq.command import send_stop_job_command

from datetime import datetime
import cv2

name_upload = Blueprint('name_upload', __name__)


@name_upload.route('/projectdetails', methods=['GET', 'POST'])
@login_required
def project_details():
    # global EPOCHS
    form = ProjectForm()

    if form.validate_on_submit():

        epoch = form.compute_hrs.data 

        video = form.upload_file.data
        filename = secure_filename(video.filename)

        video_name = filename.split('.')[0]
        video_format = filename.split('.')[1].upper()

        video.seek(0, os.SEEK_END)
        file_length = video.tell()
        video.seek(0,0)

        video_size = round(file_length/1024/1024,2) 

        project = Project(user_id=current_user.id, project_name=form.project_name.data, description=form.description.data, 
                            upload_name=filename, video_name=video_name, video_format=video_format, video_size=video_size, 
                            select_gpu=form.select_gpu.data, compute_hrs=form.compute_hrs.data)


        db.session.add(project)
        db.session.commit()


        time.sleep(2)


        project_folder_name = project.project_name.replace(' ', '_')
        # print(project_folder_name)

        # project_folder = str(project.id)+'-'+project.project_name
        project_folder = str(project.id)+'-'+project_folder_name

        input_videos = 'input_videos'
        checkpoints = 'checkpoints'

        user_folder_name = str(current_user.id)+'_'+current_user.username
        target_folder = './user_profiles'

        user_folder_path = os.path.join(target_folder, user_folder_name)
        user_project_path = os.path.join(user_folder_path, project_folder)
        # print(user_project_path)
        os.mkdir(user_project_path)

        input_videos_path = os.path.join(user_project_path, input_videos)
        checkpoints_path = os.path.join(user_project_path, checkpoints)

        os.mkdir(input_videos_path)
        os.mkdir(checkpoints_path)

        # print(input_videos_path)

        video.save(os.path.join(input_videos_path, filename))

        project_id = project.id
        # print(project_id)

        return redirect(url_for('training.start_training', epoch=epoch, current_user_id=current_user.id, 
        current_user_username=current_user.username, project_folder=project_folder, project_id=project.id, 
        input_videos_path=input_videos_path, checkpoints_path=checkpoints_path))
        # return 'test'

    return render_template('projectdetails.html', form=form)


@name_upload.route('/<int:project_id>')
@login_required
def show_project_details(project_id):
    project_post = Project.query.get_or_404(project_id)
    job = Job.query.get_or_404(project_id)
    if project_post.user_id == current_user.id:
        return render_template('project_information.html', project=project_post, job=job)
    else:
        return render_template('error_pages/403.html')


@name_upload.route('/<int:project_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_project(project_id):

    project_post = Project.query.get_or_404(project_id)
    # stop if the project is running in the background
    if project_post.user_id == current_user.id:
        job = Job.query.get_or_404(project_id)
        try:
            send_stop_job_command(r, job.job_id)
        except:
            print('No such job currently running in the background.')

        db.session.delete(job)
        db.session.commit()

        # project_post = Project.query.get_or_404(project_id)

        # delete the respective folder  
        user_folder_name = str(current_user.id)+'_'+current_user.username
        target_folder = './user_profiles'

        user_folder_path = os.path.join(target_folder, user_folder_name)

        project_folder_name = project_post.project_name.replace(' ', '_')
        
        project_folder = str(project_post.id)+'-'+project_folder_name
        path_for_deletion = os.path.join(user_folder_path, project_folder)

        shutil.rmtree(path_for_deletion)

        # delete from the database
        db.session.delete(project_post)
        db.session.commit()

        flash('Project deleted.')
        return redirect(url_for('users.old_projects'))
    else:
        return render_template('error_pages/403.html')

@name_upload.route('/<int:project_id>/stop_training', methods=['GET', 'POST'])
@login_required
def stop_training(project_id):

    project = Project.query.get(project_id)
    # job = Job.query.get_or_404(project_id)
    if project.user_id == current_user.id:
        try: 
            job = Job.query.get_or_404(project_id)
            stop_current_job = job.job_id

            print(stop_current_job)
            
            send_stop_job_command(r, stop_current_job)
            flash(f'Training for Project: {project.project_name} has stopped.')

            status = 'Training Stopped.'
            job.status = status
            db.session.commit()
            return redirect(url_for('users.old_projects'))

        except:
            flash(f'Training for Project: {project.project_name} is not running at the moment. Training has already been stopped.')
            return redirect(url_for('users.old_projects'))
    else:
        return render_template('error_pages/403.html')
    