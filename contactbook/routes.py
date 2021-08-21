from flask import jsonify, render_template, redirect, url_for, request, flash, session
from contactbook.models import Contact_Book, User
from contactbook import app
from contactbook import db
from contactbook.forms import FormValidation
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

"""
    Login route 
"""


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if(user):
            if check_password_hash(user.password, password):
                flash('Login Successfully!', 'success')
                login_user(user, remember=True)
                return redirect(url_for('contacts'))
            else:
                flash('Incorrect Password. Try Again!', 'danger')
        else:
            flash('User not Exist!', 'danger')
    return render_template('pages/login.html', user=current_user)


"""
    SignUp route
"""


@app.route("/sign-up", methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()

        if len(email) < 4:
            flash('Email must be greater than 3 characters.', 'danger')
        elif len(firstname) < 2:
            flash('First name must be greater than 1 character.', 'danger')
        elif password1 != password2:
            flash('Passwords don\'t match.', 'danger')
        elif len(password1) < 7:
            flash('Password must be at least 8 characters.', category='danger')
        elif user:
            flash('Email already exists.', 'danger')
        else:
            new_user = User(email=email, password=generate_password_hash(password1, method='sha256'), firstname=firstname)
            db.session.add(new_user)
            try:
                db.session.commit()
                login_user(new_user, remember=True)
                flash('Contact created correctly', 'success')
                return redirect(url_for('contacts'))
            except:
                db.session.rollback()
                flash('Enter Correct Email Id!', 'danger')
    return render_template('pages/signup.html', user=current_user)


"""
    Logout Route
"""


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


"""
    Index Route
"""


@app.route("/")
@login_required
def index():
    return redirect(url_for('contacts'))


"""
    create Contacts Route
"""


@app.route("/create_contact", methods=('GET', 'POST'))
@login_required
def create_contact():
    form = FormValidation()
    if request.method == 'POST':
        form = FormValidation()
        if form.validate_on_submit():
            name = (request.form['name'])
            phone_number = request.form['phone_number']
            email = request.form['email']
            new_contact = Contact_Book(name=name, email=email, phone_number=phone_number, user_id=current_user.id)
            db.session.add(new_contact)
            try:
                db.session.commit()
                flash('Contact created Successfully!', 'success')
                return redirect(url_for('contacts'))
            except:
                db.session.rollback()
                flash('Enter Correct Email Id or Email already Exist.', 'danger')
    return render_template('pages/create_contact.html', form=form, user=current_user)


"""
    Edit Contact Route
"""


@app.route("/edit_contact/<id>", methods=('GET', 'POST'))
@login_required
def edit_contact(id):
    contact = Contact_Book.query.filter_by(id=id).first()
    form = FormValidation(obj=contact)
    if form.validate_on_submit():
        try:
            current_user_id = contact.user_id
            if current_user_id == current_user.id:
                form.populate_obj(contact)
                db.session.add(contact)
                db.session.commit()
                flash('Saved successfully', 'success')
        except:
            db.session.rollback()
            flash('Error in updating contact.', 'danger')
    return render_template('pages/edit_contact.html', form=form, user=current_user)


"""
    View Contact Route
"""


@app.route('/contacts', methods=['GET'], defaults={"page": 1})
@app.route("/contacts/<int:page>")
@login_required
def contacts(page):
    page = page
    per_page = 20
    contacts = Contact_Book.query.filter_by(user_id=current_user.id).order_by(Contact_Book.name).paginate(page, per_page, error_out=False)
    return render_template('pages/contacts.html', contacts=contacts, user=current_user), 200


"""
    Search Route
"""


@app.route('/search', methods=['GET', 'POST'], defaults={"page": 1})
@app.route("/search/<int:page>", methods=['GET', 'POST'])
@login_required
def search(page):
    per_page = 10
    if request.method == 'POST':
        search = request.form.get("search").strip()
        session['search'] = request.form.get('search')
        if search == "":
            return redirect(url_for('contacts'))
        elif '@' in search:
            contacts = Contact_Book.query.filter_by(email=search, user_id=current_user.id).paginate(page, per_page, error_out=False)
            return render_template('pages/SearchResult.html', contacts=contacts, user=current_user)
        else:
            contacts = Contact_Book.query.filter_by(name=search, user_id=current_user.id).paginate(page, per_page, error_out=False)
            return render_template('pages/SearchResult.html', contacts=contacts, search=search, user=current_user)
    # search = session.get('search', None)
    # contacts = Contact_Book.query.filter(Contact_Book.name.contains(search)).order_by(Contact_Book.name).paginate(page, per_page, error_out=False)
    return redirect(url_for('contacts'))


"""
    Delete Route
"""


@ app.route("/contacts/delete", methods=('POST',))
@login_required
def contacts_delete():
    try:
        d_id = request.form.get('id')
        contact = Contact_Book.query.filter_by(id=d_id).first()
        current_user_id = contact.user_id
        if current_user_id == current_user.id:
            db.session.delete(contact)
            db.session.commit()
            flash('Deleted successfully.', 'danger')
    except:
        db.session.rollback()
        flash('Error in deleting contact.', 'danger')

    return redirect(url_for('contacts'))


"""
    404 Route
"""


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('pages/404.html', user=current_user), 404
