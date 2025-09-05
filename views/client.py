from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user 

client_bp = Blueprint('client', __name__, url_prefix='/client')


@client_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('client/dashboard.html', user=current_user)


@client_bp.route('/recommended-policies', methods=['GET', 'POST'])
@login_required
def recommended_policies(): 
    return render_template('client/recommended_policies.html', user=current_user)   


@client_bp.route('/client-updates', methods=['GET', 'POST'])
@login_required
def client_updates():           

    return render_template('client/client_updates.html', user=current_user)