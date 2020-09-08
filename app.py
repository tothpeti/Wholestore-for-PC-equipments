from flask import Flask, render_template, url_for, redirect, request
from flask_bootstrap import Bootstrap
import pyodbc
import urllib

app = Flask(__name__)
Bootstrap(app)


def create_db_connection():
    server = '###.###.#.###.###'
    database = '#####'
    user = ''
    password = ''

    # Create connection with the database
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + user +
        ';PWD=' + password
    )
    return conn


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/logout')
def logout():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        if (request.form['login_name'] == '') or (request.form['password'] == ''):
            return render_template('index.html', message='Please enter your login information!')
        else:
            conn = create_db_connection()
            found_user = None
            users_cursor = conn.cursor().execute(
                """SELECT Users.id as [users_id], account_name as [users_account_name], password as [users_password],
                          account_type as [users_account_type]
                   FROM Users
                """
            )

            for user in users_cursor.fetchall():
                if (user.users_account_name == request.form['login_name']) and (user.users_password == request.form['password']):
                    found_user = user

            users_cursor.close()

            if found_user is None:
                conn.close()
                return render_template('index.html', message='Invalid account name or password!')
            else:

                if found_user.users_account_type == 'customer':
                    found_customer_cursor = conn.cursor().execute(
                        f"""
                            SELECT Customers.id as [customers_id], Customers.first_name as [customers_first_name],
                                   Customers.last_name as [customers_last_name], Customers.balance as [customers_balance],
                                   Customers.userId as [customers_user_id], O.id as [orders_id], O.total_quantity as [orders_total_quantity],
                                   O.total_price as [orders_total_price], O.date as [orders_date], O.productId as [orders_product_id],
                                   O.customerId as [orders_customer_id], P.name as [products_name], S.name as [suppliers_name], S.id as [suppliers_id]
                            FROM Customers
                                join Users U on Customers.userId = U.id
                                left join Orders O on Customers.id = O.customerId
                                left join Products P on O.productId = P.id
                                left join Suppliers S on P.supplierId = S.id
                            WHERE Customers.userId =  {found_user.users_id}
                        """
                    )
                    found_customer = found_customer_cursor.fetchall()
                    found_customer_cursor.close()
                    conn.close()

                    return render_template('customers.html', customer=found_customer, products=get_all_products())
                else:
                    found_supplier_cursor = conn.cursor().execute(
                        f"""
                            SELECT Suppliers.id as [suppliers_id], Suppliers.name as [suppliers_name], 
                                   Suppliers.userId as [suppliers_user_id],
                                   P.id as [products_id], P.name as [products_name], P.type as [products_type], 
                                   P.quantity as [products_quantity], p.price as [products_price], P.supplierId as [products_supplier_id]
                            FROM Suppliers
                                Join Users U on Suppliers.userId = U.id
                                left join Products P on Suppliers.id = P.supplierId
                            WHERE Suppliers.userId = {found_user.users_id}
                        """
                    )
                    found_supplier = found_supplier_cursor.fetchall()
                    found_supplier_cursor.close()
                    conn.close()

                    return render_template('suppliers.html', supplier=found_supplier)
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)