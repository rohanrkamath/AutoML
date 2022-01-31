from flask import Flask, render_template, request, redirect, flash, url_for, session, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from rq import registry
from myproject import db, app
from werkzeug.utils import secure_filename
from datetime import datetime
import time
from time import strftime
import cv2

from rq.registry import StartedJobRegistry
from rq.command import send_stop_job_command

from myproject.project.train_test import train_test
from myproject import r, q

from myproject.models import Project, Job

training = Blueprint('training', __name__)

@training.route('/projectdetails/training', methods=["GET", "POST"])
@login_required
def start_training():

    jobs = q.jobs
    message = None

    if request.args:
        # project_name = request.args.get('project')
        epoch = int(request.args.get('epoch'))
        project_id = int(request.args.get('project_id'))

        input_videos_path = request.args.get('input_videos_path')
        checkpoints_path = request.args.get('checkpoints_path')

        video_name = request.args.get('video_name')
        video_format = request.args.get('video_format')
        video_size = request.args.get('video_size')

        status = 'Training In-progress.'

        task = q.enqueue(train_test, epoch, input_videos_path, checkpoints_path)

        registry = StartedJobRegistry('default', connection=r)

        time.sleep(1)

        running_job_id = registry.get_job_ids()
        current_job_id = running_job_id[0]

        # add status column.
        job = Job(current_project_id=project_id, job_id=current_job_id, status=status)

        db.session.add(job)
        db.session.commit()

        time.sleep(2)

        # jobs = q.jobs
        # q_len = len(q)
        # message = f"Task queued at {task.enqueued_at.strftime('%a %d %b %Y %H:%M:%S')}. {q_len} jobs queued."

       
    return redirect(url_for('users.old_projects', video_name=video_name, video_format=video_format, video_size=video_size))