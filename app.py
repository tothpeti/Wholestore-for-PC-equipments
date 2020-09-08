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


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        new_name = request.form.get('create_name', None)
        new_account_name = request.form.get('create_account_name', None)
        new_password = request.form.get('create_password', None)
        new_account_type = request.form.get('account_type', None)

        if ((new_name is None) or (new_name == '')) or (new_account_name is None) or (new_password is None) or (
                new_account_type is None):
            return render_template('index.html', message="Please fill the form!")
        else:
            found_user = None

            conn = create_db_connection()

            users_cursor = conn.cursor().execute(
                """SELECT Users.id as [users_id], account_name as [users_account_name], password as [users_password],
                          account_type as [users_account_type]
                   FROM Users
                """
            )

            for user in users_cursor.fetchall():
                if (user.users_account_name == new_account_name) and (
                        user.users_password == new_password):
                    found_user = user

            users_cursor.close()

            # Check if the given account name already exists
            if found_user is None:
                if new_account_type == "customer":
                    # IF everything is OK and our new user is CUSTOMER then Insert him/her into our database
                    new_last_name, new_first_name = new_name.split(' ')

                    new_cusomer_cursor = conn.cursor().execute(
                        """
                          DECLARE @tmp_table TABLE (
                              new_user_id TINYINT
                          )
  
                          INSERT Users (account_name, password, account_type)
                          OUTPUT inserted.id
                          INTO @tmp_table
                          VALUES (?, ?, ?)
  
                          INSERT INTO Customers
                          VALUES(?, ?, ?, (SELECT t.new_user_id FROM @tmp_table t))
                        """, (new_account_name, new_password, new_account_type,
                              new_first_name, new_last_name, 0)
                    )
                    new_cusomer_cursor.close()
                    conn.commit()

                    tmp_user_cursor = conn.cursor().execute(
                        """
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
                            WHERE U.account_name = ?
                        """, [new_account_name]
                    )

                    new_user = tmp_user_cursor.fetchall()

                    tmp_user_cursor.close()
                    conn.close()
                    return render_template('customers.html', customer=new_user, products=get_all_products())

                else:
                    new_supplier_cursor = conn.cursor().execute(
                        f"""
                            DECLARE @tmp_table TABLE (
                                new_user_id TINYINT
                            )

                            INSERT Users (account_name, password, account_type)
                            OUTPUT inserted.id
                            INTO @tmp_table
                            VALUES (?, ?, ?)

                            INSERT INTO Suppliers(name, userId)
                            SELECT ?, t.new_user_id
                            FROM @tmp_table t
                        """, [new_account_name, new_password, new_account_type,
                              new_name]
                    )
                    new_supplier_cursor.close()
                    conn.commit()

                    tmp_user_cursor = conn.cursor().execute(
                        f"""
                            SELECT Suppliers.id as [suppliers_id], Suppliers.name as [suppliers_name], 
                                   Suppliers.userId as [suppliers_user_id],
                                   P.id as [products_id], P.name as [products_name], P.type as [products_type], 
                                   P.quantity as [products_quantity], p.price as [products_price], P.supplierId as [products_supplier_id]
                            FROM Suppliers
                                Join Users U on Suppliers.userId = U.id
                                left join Products P on Suppliers.id = P.supplierId
                            WHERE U.account_name = ?
                        """, new_account_name
                    )

                    new_user = tmp_user_cursor.fetchall()
                    tmp_user_cursor.close()
                    conn.close()

                    return render_template('suppliers.html', supplier=new_user)

            else:
                return render_template('index.html', message="Account name already exists!")

    else:
        return render_template('index.html', message="Please fill the form!")


@app.route('/customers/updated', methods=['POST'])
def update_balance():
    if request.method == 'POST':
        new_balance = request.form['balance']
        custId = request.form['custId']
        conn = create_db_connection()

        update_balance = conn.cursor().execute(
            """
                UPDATE
                    Customers
                SET
                    Customers.balance = Customers.balance + ?
                WHERE
                    Customers.id = ?
            """, [new_balance, custId]
        )
        update_balance.close()
        conn.commit()

        tmp_user_cursor = conn.cursor().execute(
            """
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
                WHERE Customers.id = ?
            """, [custId]
        )

        updated_customer = tmp_user_cursor.fetchall()
        tmp_user_cursor.close()
        conn.close()
        return render_template('customers.html', customer=updated_customer, products=get_all_products())


@app.route('/suppliers/remove', methods=['POST'])
def remove_product():
    if request.method == 'POST':
        product_id = request.form['product_id']
        supplier_id = request.form['supplier_id']

        conn = create_db_connection()
        tmp_delete_product_cursor = conn.cursor().execute(
            """
            DELETE FROM Products WHERE Products.id = ?
            """, [product_id]
        )

        tmp_delete_product_cursor.close()
        conn.commit()

        tmp_supplier = conn.cursor().execute(
            """
            SELECT Suppliers.id as [suppliers_id], Suppliers.name as [suppliers_name],
                Suppliers.userId as [suppliers_user_id],
                P.id as [products_id], P.name as [products_name], P.type as [products_type],
                P.quantity as [products_quantity], p.price as [products_price], P.supplierId as [products_supplier_id]
            FROM Suppliers
                Join Users U on Suppliers.userId = U.id
                left join Products P on Suppliers.id = P.supplierId
            WHERE Suppliers.id = ?
            """, [supplier_id]
        )
        updated_supplier = tmp_supplier.fetchall()
        tmp_supplier.close()
        conn.close()
        return render_template('suppliers.html', supplier=updated_supplier)


if __name__ == '__main__':
    app.run(debug=True)