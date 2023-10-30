try:
    from flask import Blueprint, render_template, request, flash, redirect, url_for, abort, current_app
    from flask_login import login_required, current_user
    from .models import User, Algo, Role, db
except Exception as e:
    print('Admin Import', e)


admin = Blueprint('admin', __name__)

    

@admin.route('sudiip/admin_home')
def admin_home():
    return render_template('admin/admin_home.html', user=  current_user)

@admin.route('sudiip/role', methods=['POST', 'GET'])
def role_section():
    # add, edit or delete role to user
    if request.method == 'POST' and 'roleSet' in request.form:
        user_id = request.form.get('user_id')
        roll_name = request.form.get('rolename')
        role = Role.query.filter_by(name=roll_name).first()
        user = User.query.filter_by(id=user_id).first()
        # print(roll_name)
        user.role = role
        db.session.commit()
    if request.method == 'POST' and 'roleDel' in request.form:
        # print('del :', request.form.get('rolename'))
        del_role = request.form.get('rolename')
        role = Role.query.filter_by(name=del_role).first()
        db.session.delete(role)
        db.session.commit()
        flash('Role Delete', 'info')

    # New Role Entry Section
    if request.method == "POST"  and 'role_entry' in request.form:
        new_role = request.form.get('role_entry')

        role = Role.query.filter_by(name=new_role).first()
        if role:
            flash('Role already exists.', category='error')
        else:
            description = request.form.get('description')
            role_entry = Role(name = new_role, details= description)
            db.session.add(role_entry)
            db.session.commit()
    
    users = User.query.all()
    roles = Role.query.all()
    data = {'users': users,
            'roles': roles}
    return render_template('admin/user_setting.html', user = current_user, data = data)