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


if __name__ == '__main__':
    app.run(debug=True)