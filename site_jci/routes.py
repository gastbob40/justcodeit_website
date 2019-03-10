# This file contains the different routes of the site

# Imort
from flask import render_template, url_for, flash, redirect, request, abort
from site_jci import app, db, bcrypt
from site_jci.forms import LoginForm, RegistrationForm, UpdateAccountForm, PostForm
from site_jci.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
import os
import secrets
from PIL import Image

@app.context_processor
def context_processor():
    posts = db.session.query(Post).all()
    if current_user.is_authenticated:
        image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
        return dict(posts=posts, image_file_user=image_file)
    return dict(posts=posts)


# Home rouge
@app.route("/")
def homePage():
    return render_template("home.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('homePage'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Vous êtes connecté !', 'success')
            return redirect(url_for('homePage'))
        else:
            flash("Connexion échouée. Veuillez vérifier le nom d'utilisateur et le mot de passe.", 'danger')
    return render_template('login.html', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if not current_user.is_authenticated:
        return redirect(url_for('homePage'))
    if current_user.permission != "administrator":
        return redirect(url_for('homePage'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode("utf-8")
        user = User(username=form.username.data, password=hashed_password,
                    permission=form.permission_level.data)
        db.session.add(user)
        db.session.commit()
        flash('Compte créer pour {} !'.format(form.username.data), 'success')
        return redirect(url_for('register'))
    return render_template('registration.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('homePage'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
def account():
    # Si non connecté => gome
    if not current_user.is_authenticated:
        return redirect(url_for("homePage"))
    
    # Get Form
    form = UpdateAccountForm()

    # Quand on update
    if request.method == "POST":
        print("validate")
        # Si l'on a mis une image
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        
        if form.password.data:
            if form.password.data == form.confirm_password.data:
                hashed_password = bcrypt.generate_password_hash(
                        form.password.data).decode("utf-8")
                current_user.password = hashed_password

        current_user.username = form.username.data
        db.session.commit()
        flash('Votre compte a été mis à jours !', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
    image_file=image_file, form=form)


@app.route("/account/<string:name>", methods=['GET', 'POST'])
def account_admin(name):
    # Si non connecté => gome
    if not current_user.is_authenticated:
        return redirect(url_for("homePage"))
    if current_user.permission != "administrator":
        return redirect(url_for("homePage"))
    
    # Get Form
    form = UpdateAccountForm()
    user = db.session.query(User).filter_by(username=name).first()

    # Quand on update
    if request.method == "POST":
        # Si l'on a mis une image
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            user.image_file = picture_file
        
        if form.password.data:
            if form.password.data == form.confirm_password.data:
                hashed_password = bcrypt.generate_password_hash(
                    form.password.data).decode("utf-8")
                user.password = hashed_password
        user.permission = form.permission_level.data
        user.username = form.username.data
        db.session.commit()
        flash('Votre compte a été mis à jours !', 'success')
        return redirect(url_for('account_admin', name=user.username))
    elif request.method == 'GET':
        form.username.data = user.username
        form.permission_level.data = user.permission
    
    image_file = url_for('static', filename='profile_pics/' + user.image_file)
    return render_template('account-admin.html', user=user,
    image_file=image_file, form=form)


@app.route("/manage-account")
def manageAccount():
    users = db.session.query(User).all()
    return render_template("manageAccount.html", users=users)



@app.route("/post/new", methods=['GET', 'POST'])
def new_post():
    if not current_user.is_authenticated:
        return redirect(url_for("homePage"))

    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Votre post a été créé !', 'success')
        return redirect(url_for('homePage'))
    return render_template('create_post.html', title='Nouveau Post',
                           form=form, legend='Nouveau post')

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user.permission != "administrator":
        if post.author != current_user:
            abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Votre post a été mis à jour !', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Mise à jour du post',
                           form=form, legend='Mise à jour du post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user.permission != "administrator":
        if post.author != current_user:
            abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Votre post a bien été supprimé !', 'success')
    return redirect(url_for('homePage'))

@app.route("/account/<int:user_id>/delete", methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if current_user.permission != "administrator":
        return url_for("homePage")
    db.session.delete(user)
    db.session.commit()
    flash('Cet utilisateur a bien été supprimé!', 'success')
    return redirect(url_for('manageAccount'))

@app.route("/user/<string:username>")
def user_posts(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user_posts.html', user=user)


@app.route("/renit-avatar/<int:idUser>", methods=['GET', 'POST'])
def renitAvatar(idUser):
    # Check si la personne est co
    if not current_user.is_authenticated:
        return redirect(url_for("homePage"))

    # Test permission
    if current_user.permission != "administrator":
        if current_user.id != idUser:
            return redirect(url_for("homePage"))

    user = db.session.query(User).filter_by(id=idUser).first_or_404()
    user.image_file = "default.jpg"
    db.session.commit()
    
    return redirect(url_for("account"))

@app.route("/posts")
def list_posts():
    posts = db.session.query(Post).all()
    return render_template("posts.html", posts=posts)

@app.route("/members")
def membersPage():
    return render_template("ourMember.html")