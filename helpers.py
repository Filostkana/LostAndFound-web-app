import datetime
import pytz

from cs50 import SQL
from flask import flash, redirect, render_template, request, session
from functools import wraps


db = SQL("sqlite:///lostandfound.db")



def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            flash("login required")
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

def time_now(value):
    return datetime.datetime.now(pytz.timezone("Africa/Khartoum"))

def check_valid_id(id, name):
    """Check for id validtion"""


    max_id = db.execute("SELECT seq FROM sqlite_sequence WHERE name = ?", name)
    max_id = int(max_id[0]["seq"])

    try:
        id = int(id)
    except ValueError:
        return False
    if id < 1 or id > max_id:
        return False
    
    return True

def check_valid_value(value, column, table):
    """Check if the value valid"""
    validtion_dect = db.execute(
        f"SELECT {column} FROM {table}"
    )

    validtion_list = []
    for value_ in validtion_dect:
        validtion_list.append(value_[column])
    
    if value not in validtion_list:
        return False
    
    return True


def get_id_value(id, table, column):
    """Get the id value from the database"""

    if id:
        id_value = db.execute(
            f"SELECT {column} FROM {table} WHERE id = {id}"
        )
        return id_value[0][column]
    else:
        return "__"
    

def get_id(value, column, table):
    """get id from database"""

    id = db.execute(
        f"SELECT id FROM {table} WHERE {column} = ?", value
    )

    return id[0]["id"]


def rows_filter(rows, value, key, wild):
    """Filtering rows by value"""

    if wild:
        filtered_rows = []
        for row in rows:
            if row[key]:
                if value in str(row[key]):
                    filtered_rows.append(row)
    else:
        filtered_rows = []
        for row in rows:
            if row[key] == value:
                filtered_rows.append(row)

    return filtered_rows