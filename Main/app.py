# Import libraries
# below: copied imported libraries from: CS50 Week 9 C$50 Finance app.py (that was provided to us by CS50)
import os
from cs50 import SQL
#from flask import Flask, flash, redirect, render_template, request, session
from flask import Flask, flash, json, jsonify, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helper_loginRequired import login_required

# above: copied imported libraries from: CS50 Week 9 C$50 Finance app.py (that was provided to us by CS50)
import re # custom-built libraries I'm calling needs this, so I'm adding it just in case
from helper_customClasses import rpg_char_create, rpg_char_load
from helper_getFeatures import get_feature_text, get_feature_title, get_lvl1_features, check_lvl1_features_choice, complete_lvl1_features_choice, get_accordion_features
from helper_getSpells import get_char_lvl1_spells, class_spell_IDs_by_spell_level, validate_spell_choices, get_accordion_spells
from helper_magicNumbers import generate_magic_classIDs
magic_classIDs = generate_magic_classIDs()
# Note: some of these functions won't be called in this version, as functionality to create those classes is to be added later

# configure flask application
from flask import Flask
app = Flask(__name__)


#########################################################################################
### below: copied configuration settings from: CS50 Week 9 C$50 Finance app.py (that was provided to us by CS50),
### then modified it upon reviewing configuration documentation
# configure session settings
# flask-session configuration documentation:
# https://flask-session.readthedocs.io/en/latest/config.html
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "cachelib"
# documentation says that "filesystem" is depreciated in favor of CacheLib, so changed it to that
### above: copied configuration settings from: CS50 Week 9 C$50 Finance app.py (that was provided to us by CS50),
### then modified it upon reviewing configuration documentation
#########################################################################################


# start flask app after configuration settings done
Session(app)
#session.clear()

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///RPG_characters.db")


#########################################################################################
### below: copied the app.after_request from: CS50 Week 9 C$50 Finance app.py (that was provided to us by CS50),
### then modified it upon reviewing caching documentation
#
# caching documentation:
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control#use_cases
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Expires
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Pragma
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    return response
# this should be enough coverage to prevent caching of responses
# I might want caching of non-login entries, but we can worry about that later
# while to some extent this was copied from CS50 Week 9 C$50 Finance app.py (that was provided to us by CS50),
# I also looked into it a bit myself and chose not to include ["]response.headers["Pragma"] = "no-cache"], as it's apparently depreciated
#
### above: copied the app.after_request from: CS50 Week 9 C$50 Finance app.py (that was provided to us by CS50),
### then modified it upon reviewing caching documentation
#########################################################################################

@app.route("/")
def home():
    #print("Session variable:")
    #print(session)
    #session.clear()
    return render_template("home.html")

#########################################################################################
### below: copied the "login" and "logout" functionality from: CS50 Week 9 C$50 Finance app.py (that was provided to us by CS50),
### although I modified the error messages, and a few sql-interacting-bits to match my database
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    # session.clear() # so this is why things screw up when I redirect here
    if "user_id" in session: # pop their old character once one *starts* making a new one
        session.pop("user_id") # Let's have it just pop existing user_ids

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            # return apology("must provide username", 403)
            #return render_template("login.html", error="No username entered."), 403
            flash("No username entered.")
            #return render_template("login.html", error), 403
            return render_template("login.html"), 403

        # Ensure password was submitted
        elif not request.form.get("password"):
            # return apology("must provide password", 403)
            #return render_template("login.html", error="No password entered."), 403
            flash("No password entered.")
            return render_template("login.html"), 403

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            # return apology("invalid username and/or password", 403)
            #return render_template("login.html", error="invalid username and/or password."), 403
            flash("invalid username and/or password.")
            return render_template("login.html"), 403

        # Remember which user has logged in
        session["user_id"] = rows[0]["user_id"]

        # Redirect user to home page
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
### above: copied the "login" and "logout" functionality from: CS50 Week 9 C$50 Finance app.py (that was provided to us by CS50),
### although I modified the error messages, and a few sql-interacting-bits to match my database


### below: copied (and slightly modified) the register function in app.py I created for the CS50 Week 9 C$50 Finance problem
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        # Input validation: acquire input and validate that it exists:
        register_username = request.form.get("username")
        if not register_username:
            # return apology("Error: no username entered")
            #return render_template("register.html", error="No username entered."), 400
            flash("No username entered.")
            return render_template("register.html"), 400
        register_password_1 = request.form.get("password")
        if not register_password_1:
            # return apology("Error: password cannot be empty")
            #return render_template("register.html", error="Password cannot be empty."), 400
            flash("Password cannot be empty.")
            return render_template("register.html"), 400
        register_password_2 = request.form.get("confirmation")
        if not register_password_2:
            # return apology("Error: need to confirm password")
            #return render_template("register.html", error="Please confirm your password"), 400
            flash("Please confirm your password")
            return render_template("register.html"), 400
        # In case we somehow have accepted blank input, reject that
        if register_username == "" or register_password_1 == "" or register_password_2 == "":
            # return apology("Error: Input cannot be blank")
            #return render_template("register.html", error="Input cannot be blank."), 400
            flash("Input cannot be blank.")
            return render_template("register.html"), 400

        # Check that username does not already exist
        existing_usernames = db.execute("SELECT username FROM users")
        for existing_username in existing_usernames:
            if register_username == existing_username['username']:
                # return apology("Error: Username already exists")
                #return render_template("register.html", error="Existing username."), 400
                flash("Existing username.")
                return render_template("register.html"), 400
        # Check that passwords match
        if register_password_1 != register_password_2:
            # return apology("Error: Passwords do not match")
            #return render_template("register.html", error="Passwords do not match."), 400
            flash("Passwords do not match.")
            return render_template("register.html"), 400

        # Create password hash - now that we've checked that they match
        password_hash = generate_password_hash(register_password_1)
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)",
                   register_username, password_hash)
        # Make my username: William
        # Make my password: password
        # Yes, google keeps telling me this is insecure,
        # but for testing purposes for something never to be hosted on a real server, it works
        return render_template("login.html")
    else:
        return render_template("register.html")
### above:  copied (and slightly modified) the register function in app.py I created for the CS50 Week 9 C$50 Finance problem


# some sql operations I'll want my webpage to run (or at least get the results of)
# first one returns just the list of races/classes/backgrounds in json format, second one has html code for the dropdown-items of said list
# third one gets the race/class/background name by id
# doing that in backend to simplify html page

# NOTE: Races-stuff
# some sql operations I'll want my webpage to run (or at least get the results of)
# first one returns just the list of races/classes/backgrounds in json format, second one has html code for the dropdown-items of said list
# third one gets the race/class/background name by id
# doing that in backend to simplify html page
@app.route("/get_races") # NOTE: Part of character creation
def get_races():
    race_list = db.execute("SELECT race_id, race_name FROM list_races")
    return jsonify(race_list)

@app.route("/get_race_dropdown")
def get_race_dropdown():
    race_list = db.execute("SELECT race_id, race_name FROM list_races")
    race_dropdown = ""
    last_index = len(race_list) - 1
    for i in range(len(race_list)):
        race_dropdown += "<option value=\"" + str(race_list[i]["race_id"]) + "\">" + race_list[i]["race_name"] + "</option>"
        if i != last_index:
            race_dropdown += "\n"
    return jsonify(race_dropdown)


# NOTE: Classes-stuff
# some sql operations I'll want my webpage to run (or at least get the results of)
# first one returns just the list of races/classes/backgrounds in json format, second one has html code for the dropdown-items of said list
# third one gets the race/class/background name by id
# doing that in backend to simplify html page
@app.route("/get_classes") # NOTE: Part of character creation
def get_classes():
    class_list = db.execute("SELECT class_id, class_name FROM list_classes WHERE class_id = 4 OR class_id = 11")
    # screw it, we only supporting fighters/wizards
    # Final version will just check class-list and not use magic-numbers anyways
    return jsonify(class_list)
@app.route("/get_class_dropdown") # NOTE: Part of character creation

def get_class_dropdown():
    class_list = db.execute("SELECT class_id, class_name FROM list_classes WHERE class_id = 4 OR class_id = 11")
    # screw it, we only supporting fighters/wizards
    # Final version will just check class-list and not use magic-numbers anyways
    class_dropdown = ""
    last_index = len(class_list) - 1
    for i in range(len(class_list)):
        class_dropdown += "<option value=\"" + str(class_list[i]["class_id"]) + "\">" + class_list[i]["class_name"] + "</option>"
        if i != last_index:
            class_dropdown += "\n"
    return jsonify(class_dropdown)


# NOTE: Backgrounds-stuff
# some sql operations I'll want my webpage to run (or at least get the results of)
# first one returns just the list of races/classes/backgrounds in json format, second one has html code for the dropdown-items of said list
# third one gets the race/class/background name by id
# doing that in backend to simplify html page
@app.route("/get_backgrounds") # NOTE: Part of character creation
def get_backgrounds():
    background_list = db.execute("SELECT background_id, background_name FROM list_backgrounds")
    return jsonify(background_list)

@app.route("/get_background_dropdown") # NOTE: Part of character creation
def get_background_dropdown():
    background_list = db.execute("SELECT background_id, background_name FROM list_backgrounds")
    background_dropdown = ""
    last_index = len(background_list) - 1
    for i in range(len(background_list)):
        background_dropdown += "<option value=\"" + str(background_list[i]["background_id"]) + "\">" + background_list[i]["background_name"] + "</option>"
        if i != last_index:
            background_dropdown += "\n"
    return jsonify(background_dropdown)


@app.route("/get_lvl1features") # NOTE: Part of character creation
def get_new_char_features():
    features = ""
    class_id = -1
    if "new_char" in session:
        new_char = session["new_char"]
        class_id = new_char.class_id
        #print(f"get_lvl1features - class-id: {new_char.class_id}")
        features = get_lvl1_features(class_id)
    return jsonify(features)


@app.route("/get_char_lvl1_spells") # NOTE: Part of character creation
def get_new_char_spells():
    spells_text = ""
    class_id = -1
    if "new_char" in session:
        new_char = session["new_char"]
        class_id = new_char.class_id
        spells_text = get_char_lvl1_spells(class_id)    
    return jsonify(spells_text)


@app.route("/character_creator", methods=['GET', 'POST'])
def create_character():
    if request.method == 'POST':
        new_char = session["new_char"]
        
        var_name = request.form.get("character_name")
        var_race_id = request.form.get("race_id")
        var_class_id = request.form.get("class_id")
        var_str = request.form.get("attr_str")
        var_dex = request.form.get("attr_dex")
        var_con = request.form.get("attr_con")
        var_int = request.form.get("attr_int")
        var_wis = request.form.get("attr_wis")
        var_cha = request.form.get("attr_cha")
        
        var_background_id = request.form.get("background_id")
        #var_features_from_select = request.form.get("FeaturesDropdown") # gets single-feature
        var_features_list = request.form.getlist("FeaturesSelect") # gets-list-of-features, used in multi-select
        var_cantrips_list = request.form.getlist("SpellsCantrips") # NOTE: Remember this has to match tag I'm grabbing value from
        var_leveled_spells_list = request.form.getlist("Spells1stLevel") # NOTE: Remember this has to match tag I'm grabbing value from
        # NOTE: the name here ("FeaturesSelect") needs to match the same of the element that has the values we're looking for
        # If we're grabbing from a select-box, the name needs to match the select box
        # NOT the name of the master-form, but specifically the select-box
        
        # NOTE: select_list defaults to empty list by default
        # it is NOT considered equal to none by default, but I can always compare it to an empty list
        
        # Step 1 - character name
        if new_char.creation_step == 1:
            if type(var_name) is str: # NOTE: this should always be a string, but I'd rather just like double-check?
                new_char.set_name(var_name)
                if "pc_char" in session: # pop their old character once one *starts* making a new one
                    session.pop("pc_char")
        # Step 2 - character race
        elif new_char.creation_step == 2:
            if type(var_race_id) is str: # NOTE: checking strings mainly so isnumeric() doesn't crash the program when handed non-string
                if var_race_id.isnumeric() == True: # shouldn't ever happen, but that's just my default behaviour with isnumeric() these days
                    new_char.set_race_id(int(var_race_id))
        # Step 3 - character class
        elif new_char.creation_step == 3:
            if type(var_class_id) is str:
                if var_class_id.isnumeric() == True:
                    new_char.set_class_id(int(var_class_id))
                    #print(f"character_creator - class-id: {new_char.class_id}")
        # Step 4 - ability scores
        elif new_char.creation_step == 4:
            new_char.set_attributes(var_str, var_dex, var_con, var_int, var_wis, var_cha)
            # in this step I realized it'd be cleaner to pass all this to the function
            # and confirm datatypes and everything there
        
        # Step 5 - character background
        elif new_char.creation_step == 5:
            if type(var_background_id) is str:
                if var_background_id.isnumeric() == True:
                    new_char.set_background_id(int(var_background_id))
        # Step 6 - features
        elif new_char.creation_step == 6:
            if type(var_features_list) is list:
                if check_lvl1_features_choice(new_char.class_id, var_features_list) == True:
                    new_char.features = complete_lvl1_features_choice(new_char.class_id, var_features_list)
                    new_char.creation_step += 1
                    new_char.set_amount_of_spells_known()
        # Step 7 - spells
        elif new_char.creation_step == 7:
            if new_char.class_id == magic_classIDs.Cleric or new_char.class_id == magic_classIDs.Druid:
                # NOTE: I'm not supporting these classes yet, but while I'm thinking of it, setting spells-known for spells-prepared casters
                var_leveled_spells_list = class_spell_IDs_by_spell_level(new_char.class_id, 1)
            if new_char.class_id == magic_classIDs.Ranger:
                var_cantrips_list = class_spell_IDs_by_spell_level(new_char.class_id, 0)
            if len(var_cantrips_list) != new_char.cantrips_known_amount or len(var_leveled_spells_list) != new_char.spells_known_amount:
                flash("Incorrect number of spells selected")
            #print(f"validate_spell_choices: {validate_spell_choices(var_cantrips_list, var_leveled_spells_list, new_char.class_id)}")
            if validate_spell_choices(var_cantrips_list, var_leveled_spells_list, new_char.class_id) == True:
                for cantrip in var_cantrips_list:
                    new_char.list_cantrips.append(int(cantrip)) # NOTE: I have no idea if I actually want these as integers or not
                for spell in var_leveled_spells_list:
                    new_char.list_1stlvlSpells.append(int(spell)) # NOTE: I have no idea if I actually want these as integers or not
                new_char.creation_step += 1
                #print("Before:")
                #print(f"Cantrips: {new_char.list_cantrips}")
                #print(f"1stlvlSpells: {new_char.list_1stlvlSpells}")
                new_char.set_spell_format()
                #print("After:")
                #print(f"Cantrips: {new_char.list_cantrips}")
                #print(f"1stlvlSpells: {new_char.list_1stlvlSpells}")
            else:
                flash("Error in spell selection")
        # remove the keyname from the session if it is there
        # session.pop('key_name')
        # Step 8 - completion
        elif new_char.creation_step == 8: # complete, ready to view character now
            # NOTE: Setup rpg_char_load class-variable named "pc_char" - removes now extraneous data,
            # and has spell list for each attribute
            pc_char = rpg_char_load()
            pc_char.rpg_char_match_values(new_char) # made a function so all the values match, saves me a dozen lines of code here
            pc_char.get_names_from_IDs()
            session.pop("new_char")
            # NOTE: I will want above UN-commented (at least in final version)
            # I think - otherwise we risk getting stuck on never resetting character, so character creator always goes to load character
            # However, for testing right now, I don't want to constantly make a new character
            
            session["pc_char"] = pc_char
            return redirect("/view_character")
        return render_template("character_creator.html", new_char=new_char)
    else:
        new_char = rpg_char_create()
        session["new_char"] = new_char
        return render_template("character_creator.html", new_char=new_char)


@app.route("/view_character", methods=['GET', 'POST'])
def view_character():
    if "pc_char" in session:
        pc_char = session["pc_char"]
        return render_template("view_character.html", pc_char=pc_char )
    else:
        flash("Oops - character not created!")
        return redirect("/character_creator")


@app.route("/view_char_features", methods=['GET', 'POST']) # NOTE: Part of character viewing
def view_char_features():
    features_text = ""
    #features_list = []
    #class_id = -1
    if "pc_char" in session:
        #print("pc in session for view_char_features")
        pc_char = session["pc_char"]
        features_text = get_accordion_features(pc_char.features)
        #features_list = pc_char.features
        #print("pc_char features:")
        #print(pc_char.features)
        # NOTE: Doing as accordion-style! 
        # NOTE: Don't forget master-accordion tag for all of this on view_character.html page
        # NOTE: tag looks like this:  <div class="accordion" id="featuresMasterAccordion" name="featuresMasterAccordion"></div>
        #features_text = get_accordion_features_2(pc_char.features)
        #return jsonify(features_text)
    return jsonify(features_text)


@app.route("/view_char_spells")
def view_char_spells():
    spells_text = ""
    spell_list = []
    spell_level = request.args.get("spellLevel")
    parent_feature = request.args.get("parentFeature")
    # supporting html:
    # let response = await fetch('/search?q=' + input.value);
    # val1=a&val2=b
    if "pc_char" in session:
        pc_char = session["pc_char"]
        if spell_level not in ["0","1","2","3","4","5","6","7","8","9"]: return spells_text
        elif spell_level == "0": spell_list = pc_char.list_cantrips
        elif spell_level == "1": spell_list = pc_char.list_1stlvlSpells
        elif spell_level == "2": spell_list = pc_char.list_2ndlvlSpells
        elif spell_level == "3": spell_list = pc_char.list_3rdlvlSpells
        elif spell_level == "4": spell_list = pc_char.list_4thlvlSpells
        elif spell_level == "5": spell_list = pc_char.list_5thlvlSpells
        elif spell_level == "6": spell_list = pc_char.list_6thlvlSpells
        elif spell_level == "7": spell_list = pc_char.list_7thlvlSpells
        elif spell_level == "8": spell_list = pc_char.list_8thlvlSpells
        elif spell_level == "9": spell_list = pc_char.list_9thlvlSpells
        spells_text = get_accordion_spells(spell_list, parent_feature)
    return jsonify(spells_text)


@app.route("/save_button", methods=['GET', 'POST'])
def save_button():
    # NOTE: You don't need to be logged-in to click the button,
    # you need to be logged in for it to WORK.
    session.modified = True
    if "pc_char" not in session:
        #pc_char = session["pc_char"]
        #print("printing pc_char:")
        #print(pc_char)
        flash("Error - no character to save")
        return redirect("/view_character")
    if "user_id" in session:
        user_id = session["user_id"]
        #print(f"User_id is as follows: {user_id}")
        #flash("Whoops, we aren't ready for that yet!")
        #return redirect("/view_character")
        return redirect("/save_character", code=307)
    else:
        flash("You must be logged-on to do this.")
        return redirect("/login")
    
    
@app.route("/save_character", methods=["POST"])
@login_required
def save_character():
    if request.method == "POST":
        if "user_id" not in session:
            flash("How the hell did you get here if you're not logged in?")
            return redirect("/view_character")
            
        elif "pc_char" not in session:
            flash("Error - no character to save")
            return redirect("/view_character")
        else:
            user_id = session["user_id"]
            pc_char = session["pc_char"]
            if pc_char.validate_basics == False:
                flash("Error - invalid character")
                return redirect("/view_character")
            else:
                pc_char.save_new_character_to_database(user_id)
                #print("holy shit did it actually work")
                return redirect("/load_character")
            #if "user_id" in session: # pop their old character once one *starts* making a new one
                #session.pop("user_id")
    else:
        flash("Error - GET method not valid for saving character.")
        return redirect("/view_character")


@app.route("/load_character", methods=['GET', 'POST'])
# I don't think it matters if we do GET or POST on this page, so we won't differentiate options
# the delete button, on the other hand....
@login_required
def load_character():
    # TODO
    # NOTE: I don't think I want separate GET vs POST here?
    #if request.method == "POST": # method post seems to be form submission or something?
    #if "user_id" not in session:
        #flash("How the hell did you get here if you're not logged in?")
        #return redirect("/view_character")
    user_id = session["user_id"]
    user_list_characters = db.execute("SELECT list_characters.character_id, list_characters.name, \
        list_races.race_name, list_classes.class_name FROM list_characters \
        INNER JOIN list_races ON list_characters.race_id = list_races.race_id \
        INNER JOIN list_classes ON list_characters.level1_class_id = list_classes.class_id \
        WHERE list_characters.user_id = ?;", user_id)
    return render_template("load_character.html", user_list_characters=user_list_characters)


@app.route("/load_button", methods=['GET', 'POST'])
@login_required
def load_button():
    if request.method == "POST":
        character_id = request.form.get("char_id")
        #print(f"Character id: {character_id}")
        user_id = session["user_id"]
        pc_char = rpg_char_load()
        loading_success = pc_char.load_existing_character(user_id, character_id)
        # NOTE: user_id isn't strictly necessary, but it makes sure users are only accessing their own characters
        # pass (character_id and user_id) to pc_char to load character
        # load_existing_character returns False if there's an error, or True otherwise
        if loading_success == False:
            flash("Error in character loading")
            return redirect("/load_character")
        pc_char.print_values()
        session["pc_char"] = pc_char
        return redirect("/view_character")
    else:
        flash("Error - invalid authorization (GET)")
        return redirect("/load_character")


@app.route("/delete_button", methods=['GET', 'POST'])
@login_required
def delete_button():
    if request.method == "POST":
        character_id = request.form.get("char_id")
        user_id = session["user_id"]
        character_id = db.execute("SELECT character_id FROM list_characters WHERE user_id = ? AND character_id = ?", user_id, character_id)
        # NOTE: IMPORTANT: Confirm that user_id belongs to user!
        # IT WOULD BE VERY EASY TO DELETE ANOTHER USER'S CHARACTERS WITHOUT THAT CHECK
        if len(character_id) != 1:
            flash("Error - cannot authorize character_id")
            return redirect("/load_character")
        # Get character_id back to correct format
        character_id = character_id[0]["character_id"]
        # Delete spells - if they don't have spells, SQL simply won't find items to delete
        db.execute("DELETE FROM spellbook WHERE caster_id = ?", character_id)
        # Delete features
        db.execute("DELETE FROM character_features WHERE character_id = ?", character_id)
        # Now we should be free to delete character without foreign keys constraints
        db.execute("DELETE FROM list_characters WHERE user_id = ? AND character_id = ?", user_id, character_id)
        flash("Character deleted!")
        return redirect("/load_character")
    else:
        flash("Error - invalid authorization (GET)")
        return redirect("/load_character")

# NOTE: code to pass stuff to webpage:
#   PYTHON code for passing values I want display on webpage:
#1  json_dump = json.dumps(value_I_want_passed_to_webpage)
#2  return render_template("web_page.html", json_dump=json_dump)
#   HTML/Javascript code for importing it to webpage:
#1  <script type="module"> // need to make my scripts of type "module" so my asyc functions work
#2  const json_dump_import = JSON.parse({{json_dump|tojson}});
#3  console.log(json_dump_import) // prints output to internet console-view for me to see/test
#4  document.getElementById("id_of_tag_to_update").insertAdjacentHTML("beforeend",json_dump_import)
#5  </script>
# NOTE: variable "json_dump_import" is created in HTML/Javascript line 3, passed to line 4 (at very end)
    
    
# bootstrap -> components -> accordion looks really good
# carousel is also kinda cool?
# collapse
# modal seems REALLY good like what I want

@app.route("/testing", methods=['GET', 'POST'])
def testing():
    num_var = 0
    string_var = "soup"
    noup = "vloop"
    return render_template("testing.html", num_var=num_var, string_var=string_var, noup=noup)