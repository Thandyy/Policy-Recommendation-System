from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

authentication_bp = Blueprint('authentication', __name__, url_prefix='/authentication')

# retuning base indecx page
@authentication_bp.route('/', methods=['GET'])


@authentication_bp.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('authentication/register.html')




@authentication_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('client.dashboard'))
    
    elif current_user.is_authenticated and current_user.role == 'admin':

        return redirect(url_for('admin.notifications_center'))
    else:
        flash('invalid username or password', 'danger')

    return render_template('authentication/login.html') 


@authentication_bp.route('/logout')
@login_required 
def logout():
    return redirect(url_for('authentication.login'))


