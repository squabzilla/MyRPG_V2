from cs50 import SQL
import re

# name of database
name_of_database = "RPG_characters.db"

sql_path = "sqlite:///" + name_of_database
db = SQL(sql_path)

def validate_name(var_name):
    if type(var_name) is not str: return False
    var_name = re.sub('[^.@a-zA-Z0-9À-ÖØ-öø-ÿ"\'` ]', '', var_name)
    # this cursed regex* filters name-input, white-listing allowed characters to only allow:
    # Alpha-numeric-characters, a bunch of accented characters (both upper-case and lower-case),
    # the ' symbol, and space
    # * note: the term "cursed regex" is redundant because all regex is cursed
    if len(var_name) <= 0:
        return False
    return True


def validate_race(var_race):
    if type(var_race) is str:
        if var_race.isnumeric() == True:
            var_race = int(var_race)
    if type(var_race) is not int:
        return False
    race_list = db.execute("SELECT race_id FROM list_races") # get-list
    for i in range(len(race_list)):
        race_list[i] = race_list[i].get("race_id")
    if var_race not in (race_list):
        return False
    return True

def validate_class(var_class):
    if type(var_class) is str:
        if var_class.isnumeric() == True:
            var_class = int(var_class)
    if type(var_class) is not int:
        return False
    class_list = db.execute("SELECT class_id FROM list_classes")
    for i in range(len(class_list)):
        class_list[i] = class_list[i].get("class_id")
    if var_class not in class_list:
        return False
    return True

def validate_background(var_background):
    if type(var_background) is str:
        if var_background.isnumeric() == True:
            var_background = int(var_background)
    if type(var_background) is not int:
        return False
    background_list = db.execute("SELECT background_id FROM list_backgrounds") # get-list
    for i in range(len(background_list)):
        background_list[i] = background_list[i].get("background_id")
    if var_background not in background_list:
        return False
    return True

def check_ability_scores(var_str, var_dex, var_con, var_int, var_wis, var_cha):
    if type(var_str) is str:
        if var_str.isnumeric() == True: var_str = int(var_str)
    if type(var_dex) is str:
        if var_dex.isnumeric() == True: var_dex = int(var_dex)
    if type(var_con) is str:
        if var_con.isnumeric() == True: var_con = int(var_con)
    if type(var_int) is str:
        if var_int.isnumeric() == True: var_int = int(var_int)
    if type(var_wis) is str:
        if var_wis.isnumeric() == True: var_wis = int(var_wis)
    if type(var_cha) is str:
        if var_cha.isnumeric() == True: var_cha = int(var_cha)
    if type(var_str) is not int: return False
    if type(var_dex) is not int: return False
    if type(var_con) is not int: return False
    if type(var_int) is not int: return False
    if type(var_wis) is not int: return False
    if type(var_cha) is not int: return False
    var_sum = var_str + var_dex + var_con + var_int + var_wis + var_cha
    if var_sum != 80:
        return False
    if var_str < 5 or var_str > 18: return False
    if var_dex < 5 or var_dex > 18: return False
    if var_con < 5 or var_con > 18: return False
    if var_int < 5 or var_int > 18: return False
    if var_wis < 5 or var_wis > 18: return False
    if var_cha < 5 or var_cha > 18: return False
    return True