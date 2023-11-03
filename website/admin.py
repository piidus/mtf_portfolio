try:
    from flask import Blueprint, render_template, request, flash, redirect, url_for, abort, current_app
    from flask_login import login_required, current_user
    from .models import User, Algo, Role, db, Optionexpire
    from .utils import expiry_dates
except Exception as e:
    print('Admin Import', e)


admin = Blueprint('admin', __name__)

    

@admin.route('sudiip/admin_home')
def admin_home():
    return render_template('admin/admin_home.html', user=  current_user)
# Role Settings
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

# Stock Management
@admin.route('sudiip/stock', methods=['POST', 'GET'])
def stock_management():
    # Expiry calculation#####################################
    if request.method == 'POST' and 'option_check' in request.form:
        # print(request.form.get('option_check'))
        stock_name = request.form.get('option_check')
        strike_price = request.form.get('strike')
        try:
            algo = Algo.query.filter_by(user_id=current_user.id).first()
            date_to_insert = expiry_dates(algo.api_key, algo.api_secret, algo.api_sesion, stock_name=stock_name, strike_pric=strike_price)
        except Exception as e:
            flash(e+date_to_insert, category='error')
        else:
            if date_to_insert == None:
                flash('Enter Correct Amount', category='Info')
                # raise ValueError('Enter Amount')
            else:
                
                date_to_insert = set(date_to_insert)
                # first check the data in database
                dates_in_db = Optionexpire.query.filter_by(name = stock_name).all()
                # Get a list of book titles that are not written by the authors with books from the list
                db_list =[obj.end_date for obj in dates_in_db]
                db_list = set(db_list)
            #     # print(type(date_to_insert))
            #     # print(type(db_list))
                final_list =sorted(date_to_insert-db_list)

                # print(final_list)
            #     # Insert data into the table with default date
                for row in final_list:
                    option_data = Optionexpire(
                        name=stock_name,
                        end_date=row
                    )
                    db.session.add(option_data)

                db.session.commit()

                flash('it works', category='success')
    # RETURN SECTION
    
    data = {}
    return render_template('admin/admin_stock.html', user = current_user, data = data)