import os
from flask import render_template, flash, redirect, url_for, request
from app import app
from app import db
from app.forms import LoginForm, RegistrationForm, VideoUploadForm
from flask_login import logout_user, login_required, current_user, login_user
from app.models import User
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename

# import code ; code.interact(local=dict(globals(), **locals()))

@app.route('/')
@app.route('/index')
@login_required
def index():
    videos = [
      {
        'title': 'Pacific Rim'
      }
    ]

    return render_template('index.html', title='Home', videos=videos)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
        # return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/video', methods=['GET', 'POST'])
def video():
  video = None
  form = VideoUploadForm()

  if form.validate_on_submit():
    f = form.video_file.data
    filename = secure_filename(f.filename)
    f.save(os.path.join(app.static_folder, 'videos', filename))
    return redirect(url_for('index'))

  return render_template('video.html', form=form, video=video)
