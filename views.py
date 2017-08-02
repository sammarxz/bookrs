from flask import render_template, g, flash, redirect, url_for, abort
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
import models
import forms


@app.before_request
def before_request():
    g.user = current_user


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('books_page', username=current_user.username))
    else:
        form = forms.RegistrationForm()
        if form.validate_on_submit():
            flash('Great, You\'re registered.')
            new_user = models.User(
                name=form.name.data,
                username=form.username.data,
                email=form.email.data,
                password=generate_password_hash(form.password.data).decode('utf-8')
            )
            db.session.add(new_user)
            db.session.commit()
            user = models.User.query.filter_by(email=form.email.data).first()
            login_user(user)
            return redirect(url_for('books_page', username=user.username))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('books_page', username=current_user.username))
    else:
        form = forms.LoginForm()
        if form.validate_on_submit():
            user = models.User.query.filter_by(email=form.email.data).first()
            if user and check_password_hash(user.password, form.password.data):
                login_user(user)
                flash('Logged In', 'success')
                return redirect(url_for('books_page', username=user.username))
            else:
                flash('Your email or password doesn\'t match', 'error')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You\'ve been logged out! Come back soon', 'success')
    return redirect(url_for('index'))


@app.route('/books/new', methods=['GET', 'POST'])
@login_required
def new_book():
    form = forms.BookForm()
    if form.validate_on_submit():
        flash('Great, you added a new book.', 'Success')
        book = models.Book(
            title=form.title.data.strip(),
            status=form.status.data,
            user_id=g.user._get_current_object().id,
        )
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('books_page',
                        username=current_user.username))
    return render_template('create_book.html', form=form)


@app.route('/book/<int:id>/delete')
@login_required
def delete_book(id):
    book = models.Book.query.filter_by(id=id).first_or_404()
    if book.user == current_user:
        flash('Book Deleted', 'Success')
        db.session.delete(book)
        db.session.commit()
    else:
        abort(404)
    return redirect(url_for('books_page', username=current_user.username))


@app.route('/book/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_book(id):
    book = models.Book.query.filter_by(id=id).first_or_404()
    form = forms.BookForm(obj=book)
    if book.user == current_user:
        if form.validate_on_submit():
            flash('Book Updated', 'Success')
            book.title = form.title.data
            book.status = form.status.data
            db.session.commit()

            return redirect(url_for('books_page',
                                    username=current_user.username))
        return render_template('create_book.html', form=form)
    else:
        abort(404)


@app.route('/<username>')
def books_page(username):
    user = models.User.query.filter_by(username=username).first_or_404()
    books = user.books.order_by('created_at').all()
    return render_template('books.html', user=user, books=books)


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('books_page', username=current_user.username))
    else:
        return render_template('index.html')
