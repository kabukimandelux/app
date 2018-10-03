#Added to git
from tr2app.models import Member, User, Billing
from tr2app import app, db, bcrypt
from tr2app.forms import LoginForm, AddMemberForm, EditMemberForm, BillingForm
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user,current_user,logout_user, login_required
import struct

def stats():
    actif = Member.query.filter_by(membertype='1').count()
    ancien = Member.query.filter_by(membertype='2').count()
    candidat = Member.query.filter_by(membertype='3').count()
    honoraire = Member.query.filter_by(membertype='4').count()
    balancequery = db.session.query(db.func.sum(Billing.amount)).all()
    print (balancequery) 
    balance=0
    item =0
    for i in balancequery:
        item = balancequery.pop()
        print (item)
    #db.session.query(db.func.sum(Billing.amount)).filter_by(member_id=1).all()
    return actif,ancien,candidat,honoraire,balance


@app.route("/home")
@login_required
def home():
    actif,ancien,candidat,honoraire,balance = stats()
    return render_template('home.html',actifs=actif,anciens=ancien,candidats=candidat,honoraires=honoraire,balance=balance)

@app.route("/viewallmembers")
@login_required
def viewallmembers():
    member = Member.query.all()
    return render_template('viewallmembers.html', member=member)

@app.route("/viewmembers/<id>")
@login_required
def viewmembers(id):
    queryid = id
    form_action = url_for('viewallmembers')
    member = Member.query.filter_by(membertype=queryid).all()
    return render_template('viewallmembers.html', member=member)

#Login Working, still needs to be connected to user database, define username not existing
@app.route("/")
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
            return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)  
            flash(user.username +' logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)

#Login Working, still needs to be connected to user database, define username not existing
@app.route("/addmember", methods=['GET', 'POST'])
def addmember():
    form = AddMemberForm()
    if form.validate_on_submit():
        #hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf_8')
        user = Member(name=form.name.data,firstname=form.firstname.data,address=form.address.data,postcode=form.postcode.data,city=form.city.data,email=form.email.data,image_file=form.image_file.data,membertype=form.membertype.data)
        db.session.add(user)
        db.session.commit()
        flash(user.firstname +', has been added!', 'success')
        return redirect(url_for('home')) 
    else:
        print(form.errors)
        print("not validated")
    return render_template('addmember.html', form=form)

@app.route("/editmember/<id>",methods=['GET', 'POST'])
@login_required
def editmember(id):
    # Prepare the form and user
    #form = EditMember()
    member_id = id
    form_action = url_for('addmember')
    member = Member.query.get(member_id)
    form = EditMemberForm(obj=member) 
    if form.validate_on_submit():
        form.populate_obj(member)
        db.session.add(member)
        db.session.commit()
        flash('Member has been edited!', 'success')
        return redirect(url_for('home')) 
    return render_template('addmember.html', form=form, form_action=form_action)
    return render_template('editmember.html')

@app.route("/billing",methods=['GET', 'POST'])
@login_required
def billing():
    selectfield_choices=Member.query.all()
    groups_list=[(i.id, i.name) for i in selectfield_choices]
    form = BillingForm()
    form.member_id.choices = groups_list
    members = Member.query.all()
    if form.validate_on_submit():
        #hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf_8')
        bill = Billing(date=form.date.data,description=form.description.data,amount=form.amount.data,image_file=form.image_file.data,member_id=form.member_id.data)
        db.session.add(bill)
        db.session.commit()
        flash(str(bill.amount) +', has been billed!', 'success')
        return redirect(url_for('home')) 
    else:
        print(form.errors)
        print("not validated")
    return render_template('billing.html', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
