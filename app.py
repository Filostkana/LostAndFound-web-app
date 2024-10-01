import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, time_now, check_valid_id, check_valid_value, get_id_value, get_id, rows_filter


# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///lostandfound.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    # Get all the publication
    pubs = db.execute("SELECT * FROM publications ORDER BY id DESC LIMIT 50")

    ROWS = []
    for pub in pubs:
        property = get_id_value(pub["property_id"], "propertys", "property")

        if property == "vehicles":
            # Get the post info
            row_ids = db.execute("SELECT * FROM vehicles WHERE id = ?", pub["post_id"])

            # User info
            username = get_id_value(row_ids[0]["user_id"], "users", "username")
            phone_number = get_id_value(row_ids[0]["user_id"], "users", "ph_number")

            # Other info
            datet = row_ids[0]["datet"]

            pro = get_id_value(row_ids[0]["property_id"], "propertys", "property")

            vehicle_type = get_id_value(row_ids[0]["type_id"], "vehicles_list", "vehicle")

            brand = get_id_value(row_ids[0]["brand_id"], "vehicle_brands", "brand")

            manuf_year = row_ids[0]["manuf_year"]

            color = get_id_value(row_ids[0]["color_id"], "colors", "color")

            plate_number = row_ids[0]["plate_number"]
            if not plate_number:
                plate_number = "__"

            chassis_number = row_ids[0]["chassis_number"]
            if not chassis_number:
                chassis_number = "__"

            image_url = row_ids[0]["imge_url"]

            condtion = get_id_value(row_ids[0]["condtion_id"], "condtions", "condtion")

            ROWS.append({
                            "id" : pub["id"],
                            "username" : username,
                            "phone_number" : phone_number,
                            "datet" : datet,
                            "property" : pro,
                            "type" :vehicle_type,
                            "brand" : brand,
                            "manuf_year" : manuf_year,
                            "color" : color,
                            "plate_number" : plate_number,
                            "chassis_number" : chassis_number,
                            "image_url" : image_url,
                            "condtion" : condtion
                        })
            
        elif property == "electronics":

            # Get the post info
            row_ids = db.execute("SELECT * FROM electronics WHERE id = ?", pub["post_id"])

            # User info
            username = get_id_value(row_ids[0]["user_id"], "users", "username")
            phone_number = get_id_value(row_ids[0]["user_id"], "users", "ph_number")

            # Other info
            datet = row_ids[0]["datet"]

            pro = get_id_value(row_ids[0]["property_id"], "propertys", "property")

            electronic_type = get_id_value(row_ids[0]["type_id"], "electronics_list", "device")

            brand = get_id_value(row_ids[0]["brand_id"], "electronic_brands", "brand")

            manuf_year = row_ids[0]["manuf_year"]

            color = get_id_value(row_ids[0]["color_id"], "colors", "color")

            serial_number = row_ids[0]["serial_number"]
            if not serial_number:
                serial_number = "__"

            image_url = row_ids[0]["imge_url"]

            condtion = get_id_value(row_ids[0]["condtion_id"], "condtions", "condtion")

            ROWS.append({
                            "id" : pub["id"],
                            "username" : username,
                            "phone_number" : phone_number,
                            "datet" : datet,
                            "property" : pro,
                            "type" :electronic_type,
                            "brand" : brand,
                            "manuf_year" : manuf_year,
                            "color" : color,
                            "serial_number" : serial_number,
                            "image_url" : image_url,
                            "condtion" : condtion
                        })

        elif property == "others":

            # Get the post info
            row_ids = db.execute("SELECT * FROM others WHERE id = ?", pub["post_id"])

            # User info
            username = get_id_value(row_ids[0]["user_id"], "users", "username")
            phone_number = get_id_value(row_ids[0]["user_id"], "users", "ph_number")

            # Other info
            datet = row_ids[0]["datet"]

            pro = get_id_value(row_ids[0]["property_id"], "propertys", "property")

            type = row_ids[0]["type"]
            if not type:
                type = "__"

            brand = row_ids[0]["brand"]
            if not brand:
                brand = "__"

            manuf_year = row_ids[0]["manuf_year"]
            if not manuf_year:
                manuf_year = "__"

            color = row_ids[0]["color"]
            if not color:
                color = "__"

            serial_number = row_ids[0]["serial_number"]
            if not serial_number:
                serial_number = "__"

            desc = row_ids[0]["desc"]

            image_url = row_ids[0]["imge_url"]

            condtion = get_id_value(row_ids[0]["condtion_id"], "condtions", "condtion")

            ROWS.append({
                            "id" : pub["id"],
                            "username" : username,
                            "phone_number" : phone_number,
                            "datet" : datet,
                            "property" : pro,
                            "type" :type,
                            "brand" : brand,
                            "manuf_year" : manuf_year,
                            "color" : color,
                            "serial_number" : serial_number,
                            "desc" : desc,
                            "image_url" : image_url,
                            "condtion" : condtion
                        })

        else:
            return apology("INVALID PROPERTY")


    return render_template("index.html", rows=ROWS)



@app.route("/query")
def query():

    condtion = request.args.get("condtion")     

    if condtion:



        # Ensure condtion validation
        if not check_valid_value(condtion, "condtion", "condtions"):
            return apology("INVALID CONDITION")
        
        condtion_id = get_id(condtion, "condtion", "condtions")

        propertys = db.execute(
        "SELECT property FROM  propertys"
        )
        ROWS = []
        for property in propertys:
            name = property["property"]
            count = db.execute("SELECT COUNT(*) AS n FROM ? WHERE condtion_id = ?", name, condtion_id)[0]["n"]
            firs_datet = db.execute("SELECT MIN(datet) AS fd FROM ? WHERE condtion_id = ?", name, condtion_id)[0]["fd"]
            last_datet = db.execute("SELECT MAX(datet) AS ld FROM ? WHERE condtion_id = ?", name, condtion_id)[0]["ld"]
            ROWS.append(
                {
                    "property" : name,
                    "count" : count,
                    "first" : firs_datet,
                    "last" : last_datet
                }
            )

        
        # Config the other condtion
        other = "lost"
        if condtion == "lost":
            other = "found"
        
        # Get condtion id
        other_condtion_id = db.execute(
            "SELECT id FROM condtions WHERE condtion = ?", other
        )

        other_condtion_id = other_condtion_id[0]["id"]

        
        property_ = request.args.get("property")
        
        if property_ :

            # Ensure property validation
            if not check_valid_value(property_, "property", "propertys"):
                return apology("INVALID PROPERTY")
            
            this_year = int(time_now(True).strftime("%Y"))

            
            if property_ == "vehicles":
                # Get the data from database and proper it to desplay
                vehicles_list = db.execute(
                    "SELECT * FROM vehicles_list"
                )

                vehicle_brands = db.execute(
                "SELECT * FROM vehicle_brands"
                ) 

                colors = db.execute(
                    "SELECT * FROM colors"
                )

                years = []
                for i in range(1980, this_year + 1):
                    years.append(i)

                # Get all vehicles data
                rows_ids = db.execute("SELECT * FROM vehicles WHERE condtion_id = ? ORDER BY id DESC", other_condtion_id)

                rows = []

                for row_ids in rows_ids:

                    username = get_id_value(row_ids["user_id"], "users", "username")
                    phone_number = get_id_value(row_ids["user_id"], "users", "ph_number")

                    datet = row_ids["datet"]

                    pro = get_id_value(row_ids["property_id"], "propertys", "property")

                    vehicle_type = get_id_value(row_ids["type_id"], "vehicles_list", "vehicle")

                    brand = get_id_value(row_ids["brand_id"], "vehicle_brands", "brand")

                    manuf_year = row_ids["manuf_year"]

                    color = get_id_value(row_ids["color_id"], "colors", "color")

                    plate_number = row_ids["plate_number"]
                    if not plate_number:
                        plate_number = "__"

                    chassis_number = row_ids["chassis_number"]
                    if not chassis_number:
                        chassis_number = "__"

                    image_url = row_ids["imge_url"]


                    rows.append({
                                    "id" : row_ids["id"],
                                    "username" : username,
                                    "phone_number" : phone_number,
                                    "datet" : datet,
                                    "property" : pro,
                                    "type" :vehicle_type,
                                    "brand" : brand,
                                    "manuf_year" : manuf_year,
                                    "color" : color,
                                    "plate_number" : plate_number,
                                    "chassis_number" : chassis_number,
                                    "image_url" : image_url
                                })
                    
            
                return render_template(
                    "property.html", 
                    types=vehicles_list,
                    brands=vehicle_brands,
                    colors=colors,
                    years=years,
                    rows=rows,
                    condtion=condtion,
                    other_condtion=other,
                    property="vehicle"
                )
                

            elif property_ == "electronics":
                # Get the data from database and proper it to display
                electronics_list = db.execute(
                    "SELECT * FROM electronics_list ORDER BY id DESC"
                )

                electronic_brands = db.execute(
                "SELECT * FROM electronic_brands WHERE id != 1 ORDER BY brand"
                ) 

                colors = db.execute(
                    "SELECT * FROM colors"
                )

                years = []
                for i in range(2000, this_year + 1):
                    years.append(i)

                # Get all vehicles data
                rows_ids = db.execute("SELECT * FROM electronics WHERE condtion_id = ? ORDER BY id DESC", other_condtion_id)

                rows = []

                for row_ids in rows_ids:

                    username = get_id_value(row_ids["user_id"], "users", "username")
                    phone_number = get_id_value(row_ids["user_id"], "users", "ph_number")

                    datet = row_ids["datet"]

                    pro = get_id_value(row_ids["property_id"], "propertys", "property")

                    device = get_id_value(row_ids["type_id"], "electronics_list", "device")

                    brand = get_id_value(row_ids["brand_id"], "electronic_brands", "brand")

                    manuf_year = row_ids["manuf_year"]

                    color = get_id_value(row_ids["color_id"], "colors", "color")

                    serial_number = row_ids["serial_number"]
                    if not serial_number:
                        serial_number = "__"

                    image_url = row_ids["imge_url"]

                    rows.append({
                                    "id" : row_ids["id"],
                                    "username" : username,
                                    "phone_number" : phone_number,
                                    "datet" : datet,
                                    "property" : pro,
                                    "type" : device,
                                    "brand" : brand,
                                    "manuf_year" : manuf_year,
                                    "color" : color,
                                    "serial_number" : serial_number,
                                    "image_url" : image_url
                                })
                    
                return render_template(
                    "property.html", 
                    types=electronics_list,
                    brands=electronic_brands,
                    colors=colors,
                    years=years,
                    rows=rows,
                    condtion=condtion,
                    other_condtion=other,
                    property="electronic"
                )
                        
                
            # If property is others        
            elif property_ == "others":

                # Preparing the data that will displayed in the low section

                # Get all vehicles data
                rows_ids = db.execute("SELECT * FROM others WHERE condtion_id = ? ORDER BY id DESC", other_condtion_id)

                rows = []

                for row_ids in rows_ids:
                    # User info
                    username = get_id_value(row_ids["user_id"], "users", "username")
                    phone_number = get_id_value(row_ids["user_id"], "users", "ph_number")

                    # The thing info
                    datet = row_ids["datet"]

                    pro = get_id_value(row_ids["property_id"], "propertys", "property")

                    type = row_ids["type"]
                    if not type:
                        type = "__"

                    brand = row_ids["brand"]
                    if not brand:
                        brand = "__"

                    manuf_year = row_ids["manuf_year"]
                    if not manuf_year:
                        manuf_year = "__"

                    color = row_ids["color"]
                    if not color:
                        color = "__"

                    serial_number = row_ids["serial_number"]
                    if not serial_number:
                        serial_number = "__"

                    image_url = row_ids["imge_url"]

                    rows.append({
                                    "id" : row_ids["id"],
                                    "username" : username,
                                    "phone_number" : phone_number,
                                    "datet" : datet,
                                    "property" : pro,
                                    "type" : type,
                                    "brand" : brand,
                                    "manuf_year" : manuf_year,
                                    "color" : color,
                                    "serial_number" : serial_number,
                                    "image_url" : image_url,
                                    "desc" : row_ids["desc"]
                                })
                    
                
                return render_template(
                    "property.html",
                    this_year=this_year,
                    rows=rows,
                    condtion=condtion,
                    other_condtion=other,
                    property="other"
                )

                    
            else:
                return apology("Not yet")

        else:
           return render_template("condtion.html", rows=ROWS, condtion=condtion) 
        
    return apology("MISSING CONDITION")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]

        # Redirect user to home page
        session["info"] = "info"
        flash(f"Welcome {session["username"]}")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    #Via post
    if request.method == "POST":
        name = request.form.get("username")
        password = request.form.get("password")
        ph_number = request.form.get("ph_number")

        # Ensure username was submitted
        if not name: 
            return apology("MESSING USERNAME")
        
        # Ensure password was submitted
        if not password:
            return apology("MESSING PASSWORD")
        
        # Ensure phone number was submitted
        if not ph_number:
            return apology("MESSING PHONE NUMBER")
        
        try:
            int(ph_number)

        except ValueError:
            session["info"] = "danger"
            flash("INVALID PHONE NUMBER")
            return redirect("/register")

        # Ensure that the password is match with confirmation
        if password != request.form.get("confirmation"):
            return apology("THE PASSWORDS ARE NOT MATCHED")
        
        # Generate a hash of the password 
        pswd_hash = generate_password_hash(password)

        # Add the user to the database
        try:
            db.execute("INSERT INTO users (username, hash, ph_number, firstname, lastname) VALUES (?, ?, ?, ?, ?)",
                        name, pswd_hash, ph_number, request.form.get("firstname"), request.form.get("lastname"))
        
        # Ensure that the username has not taken
        except ValueError:
            return apology("USERNAME TAKEN")

        # Login the user
        session["user_id"] = db.execute("SELECT id FROM users WHERE username = ?", name)[0]["id"]
        session["username"] = name

        session["info"] = "success"
        flash("Registered!")
        return redirect("/")

    else:
        return render_template("register.html")
    

    
@app.route("/post", methods=["GET", "POST"])
@login_required
def post():
    # Get all the information for the from

    user_id = session["user_id"]

    condtion = request.form.get("condtion")
    if not condtion:
        return apology("MISSED CONDITION")
    if condtion not in ["lost", "found"]:
        return apology("INVALID CONDITION")
    

    condtion_id = db.execute("SELECT id FROM condtions WHERE condtion = ?", condtion)[0]["id"]

    insert_table = request.form.get("property")

    if insert_table == "vehicles":

        type_id = request.form.get("type_id")
        

        if type_id:
            if not check_valid_id(type_id, "vehicles_list"):
                return apology("INVALID TYPE")
        else:
            return apology("MISS TYPE")


        brand_id = request.form.get("brand_id")


        if brand_id:
            if not check_valid_id(brand_id, "vehicle_brands"):
                return apology("INVALID BRAND")
        else:
            return apology("MISS BRAND")


        
        manuf_year = request.form.get("manuf_year")
        if manuf_year:
            try:
                manuf_year = int(manuf_year)
            except ValueError:
                return apology("INVAlID YEAR")
            
            if manuf_year < 1800 or manuf_year > int(time_now(True).strftime("%Y")):
                return apology("INVALID YEAR") 
        else:
            return apology("MISS MANUFACTURING YEAR")
        
            
        color_id = request.form.get("color_id")

        if color_id:
            if not check_valid_id(color_id, "colors"):
                return apology("INVALID COLOR")
        else:
            color_id = None



        plate_number = request.form.get("plate_number")
        if plate_number:
            if len(plate_number) > 10:
                return apology("TO LONG PLATE NUMBER") 
            else:
                plate_number = plate_number.upper()  
        else:
            plate_number = None

        
        chassis_number = request.form.get("chassis_number")
        if chassis_number:
            if len(chassis_number) > 17:
                return apology("TO LONG CHASSIS NUMBER") 
            else:
                chassis_number = chassis_number.upper()  
        else:
            chassis_number = None



        time = time_now(True)


        datet = time.strftime('%b %d %Y')
        

        # Post the information into database
        db.execute(
            "INSERT INTO vehicles (type_id, user_id, brand_id, manuf_year, color_id, plate_number, chassis_number, datet, condtion_id, time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            type_id, user_id, brand_id, manuf_year, color_id, plate_number, chassis_number, datet, condtion_id, time
        )

        # Update publications table
        property_id = db.execute(
            "SELECT id FROM propertys WHERE property = 'vehicles'"
        )[0]["id"]


        post_id = db.execute(
            "SELECT id FROM vehicles WHERE user_id = ? AND time = ?", session["user_id"], time
        )[0]["id"]
        

        db.execute(
            "INSERT INTO publications(property_id, post_id) VALUES (?, ?)", property_id, post_id
        )

        ID = db.execute(
            "SELECT id FROM publications WHERE property_id = ? AND post_id = ?",
            property_id, post_id
            )[0]["id"]

        session["info"] = "success"
        flash("Your post has been published Successfully")
        return redirect(f"/#{ID}")
    

    if insert_table == "electronics":

        type_id = request.form.get("type_id")
        

        if type_id:
            if not check_valid_id(type_id, "electronics_list"):
                return apology("INVALID TYPE")
        else:
            return apology("MISS TYPE")


        brand_id = request.form.get("brand_id")


        if brand_id:
            if not check_valid_id(brand_id, "electronic_brands"):
                return apology("INVALID BRAND")
        else:
            return apology("MISS BRAND")


        
        manuf_year = request.form.get("manuf_year")
        if manuf_year:
            try:
                manuf_year = int(manuf_year)
            except ValueError:
                return apology("INVAlID YEAR")
            
            if manuf_year < 1800 or manuf_year > int(time_now(True).strftime("%Y")):
                return apology("INVALID YEAR") 
        else:
            return apology("MISS MANUFACTURING YEAR")
        
            
        color_id = request.form.get("color_id")

        if color_id:
            if not check_valid_id(color_id, "colors"):
                return apology("INVALID COLOR")
        else:
            color_id = None



        serial_number = request.form.get("serial_number")
        if serial_number:
            if len(serial_number) > 10:
                return apology("TO LONG PLATE NUMBER") 
            else:
                serial_number = serial_number.upper()  
        else:
            serial_number = None

        
        time = time_now(True)


        datet = time.strftime('%b %d %Y')
        

        # Post the information into database
        db.execute(
            "INSERT INTO electronics (type_id, user_id, brand_id, manuf_year, color_id, serial_number, datet, condtion_id, time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            type_id, user_id, brand_id, manuf_year, color_id, serial_number, datet, condtion_id, time
        )

        # Update publications table
        property_id = db.execute(
            "SELECT id FROM propertys WHERE property = 'electronics'"
        )[0]["id"]


        post_id = db.execute(
            "SELECT id FROM electronics WHERE user_id = ? AND time = ?", session["user_id"], time
        )[0]["id"]
        

        db.execute(
            "INSERT INTO publications(property_id, post_id) VALUES (?, ?)", property_id, post_id
        )

        ID = db.execute(
            "SELECT id FROM publications WHERE property_id = ? AND post_id = ?",
            property_id, post_id
            )[0]["id"]

        session["info"] = "success"
        flash("Your post has been published Successfully")
        return redirect(f"/#{ID}")
    
    if insert_table == "others":

        type = request.form.get("type")
        
        # Set counter to keep track of how many inputs are filled
        count = 0

        if type:
            if len(type) > 10:
                return apology("INVALID TYPE")
        else:
            return apology("MISS TYPE")


        brand = request.form.get("brand")


        if brand:
            if len(brand) > 10:
                return apology("INVALID BRAND")
            count += 1
        else:
            brand = None 


        
        manuf_year = request.form.get("manuf_year")
        if manuf_year:
            try:
                manuf_year = int(manuf_year)
            except ValueError:
                return apology("INVAlID YEAR")
            
            if manuf_year < 1 or manuf_year > int(time_now(True).strftime("%Y")):
                return apology("INVALID YEAR")
            count += 1 
        else:
            manuf_year = None
        
            
        color = request.form.get("color")

        if color:
            if len(color) < 3 or len(color) > 10:
                return apology("INVALID COLOR")
            count += 1
        else:
            color_id = None



        serial_number = request.form.get("serial_number")
        if serial_number:
            if len(serial_number) > 10:
                return apology("TO LONG PLATE NUMBER") 
            else:
                serial_number = serial_number.upper()
                count += 1  
        else:
            serial_number = None

        desc = request.form.get("desc")
        if desc:
            if len(desc) > 150:
                return apology("INVALID DESCRIPTION")
            count += 1
        else:
            desc = None

        if count < 2:
            flash("you must fell at less 3 felled")
            session["info"] = "danger"
            return redirect(f"/query?condtion={get_id_value(condtion_id, "condtions", "condtion")}&property={insert_table}")

        
        time = time_now(True)


        datet = time.strftime('%b %d %Y')
        

        # Post the information into database
        db.execute(
            "INSERT INTO others (type, user_id, brand, manuf_year, color, serial_number, desc, datet, condtion_id, time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            type, user_id, brand, manuf_year, color, serial_number, desc, datet, condtion_id, time
        )

        # Update publications table
        property_id = db.execute(
            "SELECT id FROM propertys WHERE property = 'others'"
        )[0]["id"]


        post_id = db.execute(
            "SELECT id FROM others WHERE user_id = ? AND time = ?", session["user_id"], time
        )[0]["id"]
        

        db.execute(
            "INSERT INTO publications(property_id, post_id) VALUES (?, ?)", property_id, post_id
        )

        ID = db.execute(
            "SELECT id FROM publications WHERE property_id = ? AND post_id = ?",
            property_id, post_id
            )[0]["id"]

        session["info"] = "success"
        flash("Your post has been published Successfully")
        return redirect(f"/#{ID}")
    else:
        return apology("INVALID PROPERTY")
    


@app.route("/search")
def search():
    # Get the condtion
    condtion = request.args.get("condtion")

    if condtion:

        # check condtion is valid
        if not check_valid_value(condtion, "condtion", "condtions"):
            return "IN VLAD INPUT"
        other_condtion = "lost"
        if condtion == "lost":
            other_condtion = "found"

        condtion_id = get_id(condtion, "condtion", "condtions")

        # Get the property 
        property = request.args.get("property")

        if property:

            # Check property is valid
            if not check_valid_value(property, "property", "propertys"):
                return "IN VLAD INPUT"
            # Set rows to empty list
            rows = []
            
            #if property is vehicles
            if property == "vehicles":

                # Get the data from database
                ROWS_IDS = db.execute("SELECT * FROM vehicles WHERE condtion_id = ? ORDER BY id DESC", condtion_id)

                # Sate counter to keep track of that input or not
                count = 0

                # get the data from the form

                brand_id = request.args.get("brand")

                if brand_id:

                    if not check_valid_id(brand_id, "vehicle_brands"):
                        return "IN VLAD INPUT"
                    # Filtering the rows base of the input
                    ROWS_IDS = rows_filter(ROWS_IDS, int(brand_id), "brand_id", False)

                    count += 1

                type_id = request.args.get("type")
                
                if type_id:
                    if not check_valid_id(type_id, "vehicles_list"):
                        return "IN VLAD INPUT"
                    ROWS_IDS = rows_filter(ROWS_IDS, int(type_id), "type_id", False)

                    count += 1


                manuf_year = request.args.get("manufYear")

                if manuf_year:

                    try:
                        manuf_year = int(manuf_year)
                    except ValueError:
                        return "IN VLAD INPUT"
                    # Ensure that the year is not less than 1980 and not more than this yeary
                    if manuf_year < 1980 or manuf_year > int(time_now(True).strftime("%Y")):
                        return "IN VLAD INPUT"
                    ROWS_IDS = rows_filter(ROWS_IDS, manuf_year, "manuf_year", False)

                    count += 1


                color_id = request.args.get("color")

                if color_id:

                    if not check_valid_id(color_id, "colors"):
                        return "IN VLAD INPUT"
                    ROWS_IDS = rows_filter(ROWS_IDS, int(color_id), "color_id", False)

                    count += 1


                plate_number = request.args.get("plateNumber")

                if plate_number:

                    if len(plate_number) > 10:
                        return "IN VLAD INPUT"
                    plate_number = str(plate_number)

                    ROWS_IDS = rows_filter(ROWS_IDS, plate_number.upper(), "plate_number", True)

                    count += 1



                chassis_number = request.args.get("chassisNumber")

                if chassis_number:

                    chassis_number = str(chassis_number)

                    if len(chassis_number) > 17:
                        return "IN VLAD INPUT"
                    ROWS_IDS = rows_filter(ROWS_IDS, chassis_number.upper(), "chassis_number", True)

                    count += 1

                # Check if that is input have a value
                # If not 
                if count == 0:
                    return "Search results Will appear hear"
                
                # If theris input have a value but no match
                if len(ROWS_IDS) <= 0:
                    return f"It look like there is no match, you can post it as {other_condtion} {property} by click on the Button below"
                

                # Proper rows for display

                for row_ids in ROWS_IDS:

                    # User info
                    username = get_id_value(row_ids["user_id"], "users", "username")

                    phone_number = get_id_value(row_ids["user_id"], "users", "ph_number")

                    datet = row_ids["datet"]

                    pro = get_id_value(row_ids["property_id"], "propertys", "property")

                    vehicle_type = get_id_value(row_ids["type_id"], "vehicles_list", "vehicle")

                    brand = get_id_value(row_ids["brand_id"], "vehicle_brands", "brand")

                    manuf_year = row_ids["manuf_year"]

                    color = get_id_value(row_ids["color_id"], "colors", "color")

                    plate_number = row_ids["plate_number"]
                    if not plate_number:
                        plate_number = "__"

                    chassis_number = row_ids["chassis_number"]
                    if not chassis_number:
                        chassis_number = "__"

                    image_url = row_ids["imge_url"]



                    rows.append({
                                    "id" : row_ids["id"],
                                    "username" : username,
                                    "phone_number" : phone_number,
                                    "datet" : datet,
                                    "property" : pro,
                                    "type" :vehicle_type,
                                    "brand" : brand,
                                    "manuf_year" : manuf_year,
                                    "color" : color,
                                    "plate_number" : plate_number,
                                    "chassis_number" : chassis_number,
                                    "image_url" : image_url,
                                    "condtion" : condtion
                                })
            
                return render_template("search.html", rows=rows)
            

            if property == "electronics":

                ROWS_IDS = db.execute("SELECT * FROM electronics WHERE condtion_id = ? ORDER BY id DESC", condtion_id)

                count = 0

                brand_id = request.args.get("brand")

                if brand_id:

                    if not check_valid_id(brand_id, "electronic_brands"):
                        return "IN VLAD INPUT"
                    ROWS_IDS = rows_filter(ROWS_IDS, int(brand_id), "brand_id", False)
                    count += 1

                type_id = request.args.get("type")
                
                if type_id:
                    if not check_valid_id(type_id, "electronics_list"):
                        return "IN VLAD INPUT"
                    ROWS_IDS = rows_filter(ROWS_IDS, int(type_id), "type_id", False)
                    count += 1


                manuf_year = request.args.get("manufYear")

                if manuf_year:

                    try:
                        manuf_year = int(manuf_year)
                    except ValueError:
                        return "IN VLAD INPUT"
                    # Ensure that the year is not less than 1980 and not more than this yeary
                    if manuf_year < 1980 or manuf_year > int(time_now(True).strftime("%Y")):
                        return "IN VLAD INPUT"
                    ROWS_IDS = rows_filter(ROWS_IDS, manuf_year, "manuf_year", False)
                    count += 1


                color_id = request.args.get("color")

                if color_id:

                    if not check_valid_id(color_id, "colors"):
                        return "IN VLAD INPUT"
                    ROWS_IDS = rows_filter(ROWS_IDS, int(color_id), "color_id", False)
                    count += 1


                serial_number = request.args.get("serialNumber")

                if serial_number:

                    print(serial_number.upper())

                    if len(serial_number) > 10:
                        return "IN VLAD INPUT"
                    serial_number = str(serial_number)

                    ROWS_IDS = rows_filter(ROWS_IDS, serial_number.upper(), "serial_number", True)
                    count += 1

                # Check if that is input have a value
                # If not 
                if count == 0:
                    return "Search results Will appear hear"
                
                # If theris input have a value but no match
                if len(ROWS_IDS) <= 0:
                    return f"It look like there is no matach, you can post it as {other_condtion} {property} by cleck on the butoon below"
                

                # Proper rows for display

                for row_ids in ROWS_IDS:

                    # User info
                    username = get_id_value(row_ids["user_id"], "users", "username")

                    phone_number = get_id_value(row_ids["user_id"], "users", "ph_number")

                    datet = row_ids["datet"]

                    pro = get_id_value(row_ids["property_id"], "propertys", "property")

                    electronic_type = get_id_value(row_ids["type_id"], "electronics_list", "device")

                    brand = get_id_value(row_ids["brand_id"], "electronic_brands", "brand")

                    manuf_year = row_ids["manuf_year"]

                    color = get_id_value(row_ids["color_id"], "colors", "color")

                    serial_number = row_ids["serial_number"]
                    if not serial_number:
                        serial_number = "__"


                    image_url = row_ids["imge_url"]



                    rows.append({
                                    "id" : row_ids["id"],
                                    "username" : username,
                                    "phone_number" : phone_number,
                                    "datet" : datet,
                                    "property" : pro,
                                    "type" :electronic_type,
                                    "brand" : brand,
                                    "manuf_year" : manuf_year,
                                    "color" : color,
                                    "serial_number" : serial_number,
                                    "image_url" : image_url,
                                    "condtion" : condtion
                                })
            
                return render_template("search.html", rows=rows)
            

            if property == "others":

                ROWS_IDS = db.execute("SELECT * FROM others WHERE condtion_id = ? ORDER BY id DESC", condtion_id)

                # Set counter to truk the inputs
                count = 0

                brand = request.args.get("brand")

                if brand:
                    
                    ROWS_IDS = rows_filter(ROWS_IDS, str(brand), "brand", True)
                    count += 1

                type = request.args.get("type")
                
                if type:
                    
                    ROWS_IDS = rows_filter(ROWS_IDS, str(type), "type", True)
                    count += 1


                manuf_year = request.args.get("manufYear")

                if manuf_year:

                    try:
                        manuf_year = int(manuf_year)
                    except ValueError:
                        return "IN VLAD INPUT"
                    # Ensure that the year is not less than 1980 and not more than this yeary
                    if manuf_year < 1 or manuf_year > int(time_now(True).strftime("%Y")):
                        return "IN VLAD INPUT"

                    manuf_year = str(manuf_year)
                    
                    ROWS_IDS = rows_filter(ROWS_IDS, manuf_year, "manuf_year", True)
                    
                    count += 1


                color = request.args.get("color")

                if color:

                    ROWS_IDS = rows_filter(ROWS_IDS, str(color), "color", True)

                    count += 1

                serial_number = request.args.get("serialNumber")

                if serial_number:

                    if len(serial_number) > 10:
                        return "IN VLAD INPUT"
                    serial_number = str(serial_number)

                    ROWS_IDS = rows_filter(ROWS_IDS, serial_number.upper(), "serial_number", True)

                    count += 1 

                # Check if that is input have a value
                # If not 
                if count == 0:
                    return "Search results Will appear hear"
                
                # If theris input have a value but no match
                if len(ROWS_IDS) <= 0:
                    return f"It look like there is no matach, you can post it as {other_condtion} {property} by cleck on the butoon below"
               

                # Proper rows for display
                for row_ids in ROWS_IDS:

                    # User info
                    username = get_id_value(row_ids["user_id"], "users", "username")

                    phone_number = get_id_value(row_ids["user_id"], "users", "ph_number")

                    datet = row_ids["datet"]

                    pro = get_id_value(row_ids["property_id"], "propertys", "property")

                    type = row_ids["type"]
                    if not type:
                        type = "__"

                    brand = row_ids["brand"]
                    if not brand:
                        brand = "__"

                    manuf_year = row_ids["manuf_year"]
                    if not manuf_year:
                        manuf_year = "__"

                    color = row_ids["color"]
                    if not color:
                        color = "__"

                    serial_number = row_ids["serial_number"]
                    if not serial_number:
                        serial_number = "__"

                    desc = row_ids["desc"]
                    if not desc:
                        desc = "__"

                    image_url = row_ids["imge_url"]



                    rows.append({
                                    "id" : row_ids["id"],
                                    "username" : username,
                                    "phone_number" : phone_number,
                                    "datet" : datet,
                                    "property" : pro,
                                    "type" : type,
                                    "brand" : brand,
                                    "manuf_year" : manuf_year,
                                    "color" : color,
                                    "serial_number" : serial_number,
                                    "desc" : desc,
                                    "image_url" : image_url,
                                    "condtion" : condtion
                                })
            
                return render_template("search.html", rows=rows)
            else:
                return apology("invalid property")
        else:
            return apology("MISSING PROPERTY")
    else:
        return apology("MISSING CONDITION")
    
    

@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    '''Changing the user password'''

    # Via post
    if request.method == "POST":
        # Ensure all filed on the from was submitted
        old_psw = request.form.get("old_password")
        if not old_psw:
            return apology("MESSING OLD PASSWORD")
        new_psw = request.form.get("new_password")
        if not new_psw:
            return apology("MESSING NEW PASSWORD")
        if not request.form.get("confirmation"):
            return apology("MESSING CONFIRMATION")
        
        # Ensure new password and hes confirmation are matched
        if new_psw != request.form.get("confirmation"):
            return apology("THE PASSWORDS NOT MATCHED")
        
        # Ensure the old password is the same as the old one
        old_psw_hash = db.execute("SELECT hash FROM users WHERE id = ?", 
                                  session["user_id"])[0]["hash"]
        if not check_password_hash(old_psw_hash, old_psw):
            return apology("RUNG OLD PASSWORD")
        
        # Crate a hash for new password and replace it withe old one
        new_psw_hash = generate_password_hash(new_psw)
        db.execute(
            "UPDATE users SET hash = ? WHERE id = ?", new_psw_hash, session["user_id"]
        )

        flash("Password has ben changed!")
        session["info"] = "success"
        return redirect("/")
    
    # Via get
    return render_template("change_password.html")

            
