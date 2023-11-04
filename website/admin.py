try:
    from flask import Blueprint, render_template, request, flash, redirect, url_for, abort, current_app
    from flask_login import login_required, current_user
    from sqlalchemy.exc import PendingRollbackError, DataError
    import zipfile
    import pandas as pd
    import numpy as np
    from .models import User, Algo, Role, db, Optionexpire, Equity, Indices, Sgb
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

# Insert stock name to database
def insert_stocks_from_dataframe(data, model_name):
    # Iterate through the DataFrame and insert data if it doesn't exist in the table
    for index, row in data.iterrows():
        token = row['Token']
        existing_data = model_name.query.filter_by(token=token).first()

        if existing_data is None:
            try:
                
                print(row['ExchangeCode'], '****************************************')
                if row['CompanyName'] == np.nan:
                    com_name = row['ExchangeCode']
                else:
                    com_name = row['CompanyName']
                new_data = model_name(token = row['Token'], shortname = row['ShortName'], company_name = com_name,
                                    isin = row['ISINCode'], exchange_name= row['ExchangeCode'] )
                db.session.add(new_data)
                db.session.commit()
            except DataError as e:
                # Handle the DataError (e.g., log the error, notify the user, etc.)
                print(f"DataError: {e}")
                db.session.rollback()  # Clear the pending rollback state
            except PendingRollbackError:
                # Rollback the transaction to clear the pending rollback state
                db.session.rollback()
            except Exception as e:
                msg = f"{row['ShortName']}  :  {e}"
                current_app.logger.error(msg=msg)
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

    # Stock Zip entry
    if request.method == 'POST' and "icici_stock_zip" in request.form:
        # Check File Name
        file =request.files['file1']
        file_name = file.filename
        if file_name.split('.')[-1] == 'zip':
            with zipfile.ZipFile(file) as zip_file:
                zip_file.extractall('website/static/temp_stock')
            df = pd.read_csv(filepath_or_buffer="website/static/temp_stock/NSEScripMaster.txt")

            filered_column = ['Token', ' "ShortName"', ' "Series"', ' "CompanyName"', ' "ISINCode"', ' "ExchangeCode"']
            df = df[filered_column]
            df.columns = ['Token', 'ShortName', 'Series', 'CompanyName', 'ISINCode', 'ExchangeCode']
            df['Series'] = df['Series'].replace('0', 'IDX')
            df = df[df['Series'].isin(['IDX', 'EQ', 'GB'])]

            # Fill NaN values in the 'name' column with values from the 'title' column
            df['CompanyName'].fillna(df['ExchangeCode'], inplace=True)
            df['ISINCode'].fillna(df['ShortName'], inplace=True)
            
            df_indices = df[df['Series']=='IDX'].reset_index(drop=True)
            df_equity = df[df['Series']=='EQ'].reset_index(drop=True)
            df_sgb = df[df['Series']=='GB'].reset_index(drop=True)
            # Drop rows where Column_A has value 0 or NaN
            # df_equity['Token'].astype(dtype='int64')
            df_equity = df_equity.dropna(subset=['Token'])
            df_equity = df_equity[~df_equity['Token'].isin(["0", "00"])].reset_index(drop=True)
            print(df_sgb)
            try:
              # Check if the book table exists
                insert_stocks_from_dataframe(df_equity, model_name= Equity)
                insert_stocks_from_dataframe(df_indices, model_name= Indices)
                insert_stocks_from_dataframe(df_sgb, model_name= Sgb)
            except Exception as e:
                print(e)

        else:
            flash('Check Your file', category='error') 
    
    # RETURN SECTION
    
    data = {}
    return render_template('admin/admin_stock.html', user = current_user, data = data)