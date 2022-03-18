# AutoML product

## Overview

This is the code I wrote for a web app during my internship at Asquared IoT. As a Full Stack Developer, I was hired to build a fully functional web app around their existing Manufacturing AI code. 

## Technologies used

The app was built using the Flask web framework and its suite of packages for handling forms rendering and authentication, SQLite3 as the database of choice, Redis Queue to queue up and ansynchronously handle multiple heavy background jobs and bootstrap and CSS beautify the app. 

- Flask 
  - Flask login
  - Flask dance
  - Flask Migrate
  - Flask SQLAlchemy
  - Flask WTForms
- Redis Queue
- SQLite3
- Bootstrap 4
- SQLAlchemy
- Celery

## Project Structure

- `checkpoints/*` -  Pre-trained weights are stored during the training phased.
- `input_videos/*` - Uploaded videos by users were stored here.
- `migrations/*` - All the changed done in the schema files were to be changed/migrated to the DB.
- `myproject/*` - The source-code; Project code resides, i.e the templates, views, schema, etc
- `backend/*` - Company provided Manufacturing AI backend was being exported to the app.
- `user_profiles` - Auto-generated users during sign-up and projects created were stored in this directory. 

## Run the project locally

```
$ git clone https://github.com/rohanrkamath/AutoML
$ cd AutoML
$ virtualenv env
$ env/bin/activate
$ pip -r requirements.txt
$ python app.py
$ redis-server
$ rq worker --with-scheduler
```

Here is a blog post I wrote on the [project](https://rohankamath.me/blog/posts/asquared-iot-experience.html)

