from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user


admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/notifications-center', methods=['GET', 'POST'])
@login_required
def notifications_center():
  
    return render_template('admin/notifications_center.html',user=current_user)

@admin_bp.route('/policy-recommendations', methods=['GET', 'POST'])
@login_required
def policy_recommendations():

    return render_template('admin/policy_recommendations.html',user=current_user)

@admin_bp.route('/updates', methods=['GET', 'POST'])
@login_required
def updates():

    return render_template('admin/updates.html',user=current_user)

@admin_bp.route('/registered-policies', methods=['GET', 'POST'])
@login_required
def registered_policies():

    return render_template('admin/registered_policies.html',user=current_user)




