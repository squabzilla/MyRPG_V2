# NOTE: I don't think I'm gonna end up using any of this, but I don't want to delete it quite yet

from cs50 import SQL
import re

# name of database
name_of_database = "RPG_characters.db"

sql_path = "sqlite:///" + name_of_database
db = SQL(sql_path)

def class_spells_by_spell_level(class_id, spell_level):
    try: spell_level = int(spell_level)
    except:
        print("Invalid spell-level")
        return False
    list_spells = []
    # if class_id not in [1,2,3,4,7,8,10,11,12]: return False
    # just return empty list if it's not in one of these
    if class_id == 2: # Bard spells
        list_spells = db.execute("SELECT spell_id, spell_name FROM list_spells WHERE bard_spell = 1 AND spell_level = ?", spell_level)
    elif class_id == 3: # Cleric spells
        list_spells = db.execute("SELECT spell_id, spell_name FROM list_spells WHERE cleric_spell = 1 AND spell_level = ?", spell_level)
    elif class_id == 4: # Druid spells
        list_spells = db.execute("SELECT spell_id, spell_name FROM list_spells WHERE druid_spell = 1 AND spell_level = ?", spell_level)
    elif class_id == 7: # Ranger spells
        list_spells = db.execute("SELECT spell_id, spell_name FROM list_spells WHERE ranger_spell = 1 AND spell_level = ?", spell_level)
    elif class_id == 8: # Paladin spells
        list_spells = db.execute("SELECT spell_id, spell_name FROM list_spells WHERE paladin_spell = 1 AND spell_level = ?", spell_level)
    elif class_id == 10: # Sorcerer spells
        list_spells = db.execute("SELECT spell_id, spell_name FROM list_spells WHERE sorcerer_spell = 1 AND spell_level = ?", spell_level)
    elif class_id == 11: # Warlock spells
        list_spells = db.execute("SELECT spell_id, spell_name FROM list_spells WHERE warlock_spell = 1 AND spell_level = ?", spell_level)
    elif class_id == 12: # Wizard spells
        list_spells = db.execute("SELECT spell_id, spell_name FROM list_spells WHERE wizard_spell = 1 AND spell_level = ?", spell_level)
    else:
        return None
    return list_spells

class new_bard_spells:
    # class_id: 2
    # cantrips known: 2
    # spells known: 4
    def __init__(self, cantrips_known = [], spells_known = [], list_class_cantrips = [], list_class_spells = [],
                 class_id = 2, prepared_caster = False,
                 cantrip_1 = None, cantrip_2 = None, spell_1 = None, spell_2 = None, spell_3 = None, spell_4 = None):
        self.cantrips_known = cantrips_known
        self.spells_known = spells_known
        self.list_class_cantrips = list_class_cantrips
        self.list_class_spells = list_class_spells
        
        self.class_id = class_id
        self.prepared_caster = prepared_caster
        
        self.cantrip_1 = cantrip_1
        self.cantrip_2 = cantrip_2
        self.spell_1 = spell_1
        self.spell_2 = spell_2
        self.spell_3 = spell_3
        self.spell_4 = spell_4
    
    def retrieve_class_spell_list(self):
        self.list_class_cantrips = class_spells_by_spell_level(self.class_id,0)
        self.list_class_spells = class_spells_by_spell_level(self.class_id,1)
        return True
    
    def set_cantrip_1(self, value):
        if value in self.list_class_cantrips:
            self.cantrip_1 = value
            return True
        else:
            print("Error: cantrip not in list")
            return False
    def rm_cantrip_1(self):
        self.cantrip_1 = None
        return True
    
    def set_cantrip_2(self, value):
        if value in self.list_class_cantrips:
            self.cantrip_2 = value
            return True
        else:
            print("Error: cantrip not in list")
            return False
    def rm_cantrip_2(self):
        self.cantrip_2 = None
        return True
    
    def set_spell_1(self, value):
        if value in self.list_class_spells:
            self.spell_1 = value
            return True
        else:
            print("Error: spell not in list")
            return False
    def rm_spell_1(self):
        self.spell_1 = None
        return True
    
    def set_spell_2(self, value):
        if value in self.list_class_spells:
            self.spell_2 = value
            return True
        else:
            print("Error: spell not in list")
            return False
    def rm_spell_2(self):
        self.spell_2 = None
        return True
    
    def set_spell_3(self, value):
        if value in self.list_class_spells:
            self.spell_3 = value
            return True
        else:
            print("Error: spell not in list")
            return False
    def rm_spell_3(self):
        self.spell_3 = None
        return True
    
    def set_spell_4(self, value):
        if value in self.list_class_spells:
            self.spell_4 = value
            return True
        else:
            print("Error: spell not in list")
            return False
    def rm_spell_4(self):
        self.spell_4 = None
        return True
    
    def confirm_list(self):
        if (self.cantrip_1 == None) or (self.cantrip_2 == None) or \
        (self.spell_1 == None) or (self.spell_2 == None) or (self.spell_3 == None) or (self.spell_4 == None):
            print("Error: unassigned cantrips or spells")
            return False
        self.spells_known = []
        self.spells_known.append(int(self.cantrip_1))
        self.spells_known.append(int(self.cantrip_2))
        self.spells_known.append(int(self.spell_1))
        self.spells_known.append(int(self.spell_2))
        self.spells_known.append(int(self.spell_3))
        self.spells_known.append(int(self.spell_4))
        var_count = 0
        last_index = len(self.spells_known)
        while var_count < (last_index - 1):
            var_next = var_count + 1
            while var_next <= last_index:
                if self.spells_known[var_count] == self.spells_known[var_next]:
                    print("Error: spell chosen multiple times.")
                    return False
                var_next += 1
        return self.spells_known
    
    def reset_spells(self):
        self.spells_known = []
        self.cantrip_1 = None
        self.cantrip_2 = None
        self.spell_1 = None
        self.spell_2 = None
        self.spell_3 = None
        self.spell_4 = None
        return True


class new_cleric_spells:
    # class_id: 3
    # cantrips known: 3
    # spells known: all
    def __init__(self, cantrips_known = [], spells_known = [], list_class_cantrips = [], list_class_spells = [],
                 class_id = 3, prepared_caster = True,
                 cantrip_1 = None, cantrip_2 = None, cantrip_3 = None):
        self.cantrips_known = cantrips_known
        self.spells_known = spells_known
        self.list_class_cantrips = list_class_cantrips
        self.list_class_spells = list_class_spells
        
        self.class_id = class_id
        self.prepared_caster = prepared_caster
        
        self.cantrip_1 = cantrip_1
        self.cantrip_2 = cantrip_2
        self.cantrip_3 = cantrip_3
    
    def retrieve_class_spell_list(self):
        self.list_class_cantrips = class_spells_by_spell_level(self.class_id,0)
        self.list_class_spells = class_spells_by_spell_level(self.class_id,1)
        return True
    
    def set_cantrip_1(self, value):
        if value in self.list_class_cantrips:
            self.cantrip_1 = value
            return True
        else:
            print("Error: cantrip not in list")
            return False
    def rm_cantrip_1(self):
        self.cantrip_1 = None
        return True
    
    def set_cantrip_2(self, value):
        if value in self.list_class_cantrips:
            self.cantrip_2 = value
            return True
        else:
            print("Error: cantrip not in list")
            return False
    def rm_cantrip_2(self):
        self.cantrip_2 = None
        return True
    
    def set_cantrip_3(self, value):
        if value in self.list_class_cantrips:
            self.cantrip_3 = value
            return True
        else:
            print("Error: cantrip not in list")
            return False
    def rm_cantrip_3(self):
        self.cantrip_3 = None
        return True
    
    def confirm_list(self):
        if (self.cantrip_1 == None) or (self.cantrip_2 == None) or (self.cantrip_3 == None):
            print("Error: unassigned cantrips or spells")
            return False
        self.spells_known = []
        self.spells_known.append(int(self.cantrip_1))
        self.spells_known.append(int(self.cantrip_2))
        self.spells_known.append(int(self.cantrip_3))
        for spell_id in self.list_class_spells:
            self.spells_known.append(spell_id)
        var_count = 0
        last_index = len(self.spells_known)
        while var_count < (last_index - 1):
            var_next = var_count + 1
            while var_next <= last_index:
                if self.spells_known[var_count] == self.spells_known[var_next]:
                    print("Error: spell chosen multiple times.")
                    return False
                var_next += 1
        return self.spells_known
    
    def reset_spells(self):
        self.spells_known = []
        self.cantrip_1 = None
        self.cantrip_2 = None
        self.cantrip_3 = None
        return True


class new_druid_spells:
    # class_id: 4
    # cantrips known: 2
    # spells known: all
    def __init__(self, cantrips_known = [], spells_known = [], list_class_cantrips = [], list_class_spells = [],
                 class_id = 4, prepared_caster = True,
                 cantrip_1 = None, cantrip_2 = None):
        self.cantrips_known = cantrips_known
        self.spells_known = spells_known
        self.list_class_cantrips = list_class_cantrips
        self.list_class_spells = list_class_spells
        
        self.class_id = class_id
        self.prepared_caster = prepared_caster
        
        self.cantrip_1 = cantrip_1
        self.cantrip_2 = cantrip_2
    
    def retrieve_class_spell_list(self):
        self.list_class_cantrips = class_spells_by_spell_level(self.class_id,0)
        self.list_class_spells = class_spells_by_spell_level(self.class_id,1)
        return True
    
    def set_cantrip_1(self, value):
        if value in self.list_class_cantrips:
            self.cantrip_1 = value
            return True
        else:
            print("Error: cantrip not in list")
            return False
    def rm_cantrip_1(self):
        self.cantrip_1 = None
        return True
    
    def set_cantrip_2(self, value):
        if value in self.list_class_cantrips:
            self.cantrip_2 = value
            return True
        else:
            print("Error: cantrip not in list")
            return False
    def rm_cantrip_2(self):
        self.cantrip_2 = None
        return True
    
    def confirm_list(self):
        if (self.cantrip_1 == None) or (self.cantrip_2 == None):
            print("Error: unassigned cantrips or spells")
            return False
        self.spells_known = []
        self.spells_known.append(int(self.cantrip_1))
        self.spells_known.append(int(self.cantrip_2))
        for spell_id in self.list_class_spells:
            self.spells_known.append(spell_id)
        var_count = 0
        last_index = len(self.spells_known)
        while var_count < (last_index - 1):
            var_next = var_count + 1
            while var_next <= last_index:
                if self.spells_known[var_count] == self.spells_known[var_next]:
                    print("Error: spell chosen multiple times.")
                    return False
                var_next += 1
        return self.spells_known
    
    def reset_spells(self):
        self.spells_known = []
        self.cantrip_1 = None
        self.cantrip_2 = None
        return True


class new_ranger_spells:
    # class_id: 7
    # cantrips known: 2
    # spells known: none
    def __init__(self, cantrips_known = [], spells_known = [], list_class_cantrips = [], list_class_spells = [],
                 class_id = 7, prepared_caster = False,
                 cantrip_1 = None, cantrip_2 = None):
        self.cantrips_known = cantrips_known
        self.spells_known = spells_known
        self.list_class_cantrips = list_class_cantrips
        self.list_class_spells = list_class_spells
        
        self.class_id = class_id
        self.prepared_caster = prepared_caster
        
        self.cantrip_1 = cantrip_1
        self.cantrip_2 = cantrip_2
    
    def retrieve_class_spell_list(self):
        self.list_class_cantrips = class_spells_by_spell_level(self.class_id,0)
        self.list_class_spells = class_spells_by_spell_level(self.class_id,1)
        return True
    #def set_cantrip_1(self, value): self.cantrip_1 = value
    #def rm_cantrip_1(self): self.cantrip_1 = None
    #def set_cantrip_2(self, value): self.cantrip_2 = value
    #def rm_cantrip_2(self): self.cantrip_2 = None
    def set_ranger_spells(self):
        # db.execute("SELECT * FROM list_spells WHERE spell_name = 'Hunter''s Mark';
        # SELECT * FROM list_spells WHERE spell_name = "Druidcraft";
        self.cantrip_1 = db.execute("SELECT spell_id FROM list_spells WHERE spell_name = 'Hunter''s Mark';")[0].get("spell_id")
        self.cantrip_2 = db.execute("SELECT spell_id FROM list_spells WHERE spell_name = 'Druidcraft';")[0].get("spell_id")
        self.spells_known = []
        self.spells_known.append(int(self.cantrip_1))
        self.spells_known.append(int(self.cantrip_2))
        return self.spells_known
    
    def confirm_list(self):
        if (self.cantrip_1 == None) or (self.cantrip_2 == None):
            print("Error: unassigned cantrips or spells")
            return False
        self.spells_known = []
        self.spells_known.append(int(self.cantrip_1))
        self.spells_known.append(int(self.cantrip_2))
        return self.spells_known
        
    def reset_spells(self):
        self.spells_known = []
        self.cantrip_1 = None
        self.cantrip_2 = None
        return True


class new_sorcerer_spells:
    # class_id: 10
    # cantrips known: 4
    # spells known: 2
    def __init__(self, cantrips_known = [], spells_known = [], list_class_cantrips = [], list_class_spells = [],
                 class_id = 10, prepared_caster = False,
                 cantrip_1 = None, cantrip_2 = None, cantrip_3 = None, cantrip_4 = None, spell_1 = None, spell_2 = None):
        self.cantrips_known = cantrips_known
        self.spells_known = spells_known
        self.list_class_cantrips = list_class_cantrips
        self.list_class_spells = list_class_spells
        
        self.class_id = class_id
        self.prepared_caster = prepared_caster
        
        self.cantrip_1 = cantrip_1
        self.cantrip_2 = cantrip_2
        self.cantrip_3 = cantrip_3
        self.cantrip_4 = cantrip_4
        self.spell_1 = spell_1
        self.spell_2 = spell_2
    
    def retrieve_class_spell_list(self):
        self.list_class_cantrips = class_spells_by_spell_level(self.class_id,0)
        self.list_class_spells = class_spells_by_spell_level(self.class_id,1)
        return True
    
    def set_cantrip_1(self, value):
        if value in self.list_class_cantrips:
            self.cantrip_1 = value
            return True
        else:
            print("Error: cantrip not in list")
            return False
    def rm_cantrip_1(self):
        self.cantrip_1 = None
        return True
    
    def set_cantrip_2(self, value):
        if value in self.list_class_cantrips:
            self.cantrip_2 = value
            return True
        else:
            print("Error: cantrip not in list")
            return False
    def rm_cantrip_2(self):
        self.cantrip_2 = None
        return True
    
    def set_cantrip_3(self, value):
        if value in self.list_class_cantrips:
            self.cantrip_3 = value
            return True
        else:
            print("Error: cantrip not in list")
            return False
    def rm_cantrip_3(self):
        self.cantrip_3 = None
        return True
    
    def set_cantrip_4(self, value):
        if value in self.list_class_cantrips:
            self.cantrip_4 = value
            return True
        else:
            print("Error: cantrip not in list")
            return False
    def rm_cantrip_4(self):
        self.cantrip_4 = None
        return True
    
    def set_spell_1(self, value):
        if value in self.list_class_spells:
            self.spell_1 = value
            return True
        else:
            print("Error: spell not in list")
            return False
    def rm_spell_1(self):
        self.spell_1 = None
        return True
    
    def set_spell_2(self, value):
        if value in self.list_class_spells:
            self.spell_2 = value
            return True
        else:
            print("Error: spell not in list")
            return False
    def rm_spell_2(self):
        self.spell_2 = None
        return True
    
    def confirm_list(self):
        if (self.cantrip_1 == None) or (self.cantrip_2 == None) or (self.cantrip_3 == None) or (self.cantrip_4 == None) or\
        (self.spell_1 == None) or (self.spell_2 == None):
            print("Error: unassigned cantrips or spells")
            return False
        self.spells_known = []
        self.spells_known.append(int(self.cantrip_1))
        self.spells_known.append(int(self.cantrip_2))
        self.spells_known.append(int(self.cantrip_3))
        self.spells_known.append(int(self.cantrip_4))
        self.spells_known.append(int(self.spell_1))
        self.spells_known.append(int(self.spell_2))
        var_count = 0
        last_index = len(self.spells_known)
        while var_count < (last_index - 1):
            var_next = var_count + 1
            while var_next <= last_index:
                if self.spells_known[var_count] == self.spells_known[var_next]:
                    print("Error: spell chosen multiple times.")
                    return False
                var_next += 1
        return True
    def reset_spells(self):
        self.spells_known = []
        self.cantrip_1 = None
        self.cantrip_2 = None
        self.cantrip_3 = None
        self.cantrip_4 = None
        self.spell_1 = None
        self.spell_2 = None
        return True


class new_warlock_spells:
    # class_id: 11
    # cantrips known: 2
    # spells known: 2
    def __init__(self, cantrips_known = [], spells_known = [], list_class_cantrips = [], list_class_spells = [],
                 class_id = 11, prepared_caster = False,
                 cantrip_1 = None, cantrip_2 = None, spell_1 = None, spell_2 = None):
        self.cantrips_known = cantrips_known
        self.spells_known = spells_known
        self.list_class_cantrips = list_class_cantrips
        self.list_class_spells = list_class_spells
        
        self.class_id = class_id
        self.prepared_caster = prepared_caster
        
        self.cantrip_1 = cantrip_1
        self.cantrip_2 = cantrip_2
        self.spell_1 = spell_1
        self.spell_2 = spell_2
    
    def retrieve_class_spell_list(self):
        self.list_class_cantrips = class_spells_by_spell_level(self.class_id,0)
        self.list_class_spells = class_spells_by_spell_level(self.class_id,1)
        return True
    
    def set_cantrip_1(self, value):
        if value in self.list_class_cantrips:
            self.cantrip_1 = value
            return True
        else:
            print("Error: cantrip not in list")
            return False
    def rm_cantrip_1(self):
        self.cantrip_1 = None
        return True
    
    def set_cantrip_2(self, value):
        if value in self.list_class_cantrips:
            self.cantrip_2 = value
            return True
        else:
            print("Error: cantrip not in list")
            return False
    def rm_cantrip_2(self):
        self.cantrip_2 = None
        return True
    
    def set_spell_1(self, value):
        if value in self.list_class_spells:
            self.spell_1 = value
            return True
        else:
            print("Error: spell not in list")
            return False
    def rm_spell_1(self):
        self.spell_1 = None
        return True
    
    def set_spell_2(self, value):
        if value in self.list_class_spells:
            self.spell_2 = value
            return True
        else:
            print("Error: spell not in list")
            return False
    def rm_spell_2(self):
        self.spell_2 = None
        return True
    
    def confirm_list(self):
        if (self.cantrip_1 == None) or (self.cantrip_2 == None) or\
        (self.spell_1 == None) or (self.spell_2 == None):
            print("Error: unassigned cantrips or spells")
            return False
        self.spells_known = []
        self.spells_known.append(int(self.cantrip_1))
        self.spells_known.append(int(self.cantrip_2))
        self.spells_known.append(int(self.cantrip_3))
        self.spells_known.append(int(self.cantrip_4))
        self.spells_known.append(int(self.spell_1))
        self.spells_known.append(int(self.spell_2))
        var_count = 0
        last_index = len(self.spells_known)
        while var_count < (last_index - 1):
            var_next = var_count + 1
            while var_next <= last_index:
                if self.spells_known[var_count] == self.spells_known[var_next]:
                    print("Error: spell chosen multiple times.")
                    return False
                var_next += 1
        return True
    def reset_spells(self):
        self.spells_known = []
        self.cantrip_1 = None
        self.cantrip_2 = None
        self.spell_1 = None
        self.spell_2 = None
        return True


class new_wizard_spells:
    # class_id: 12
    # cantrips known: 3
    # spells known: 6
    def __init__(self, cantrips_known = [], spells_known = [], list_class_cantrips = [], list_class_spells = [],
                 class_id = 12, prepared_caster = True,
                 cantrip_1 = None, cantrip_2 = None, cantrip_3 = None,
                 spell_1 = None, spell_2 = None, spell_3 = None, spell_4 = None, spell_5 = None, spell_6 = None):
        self.cantrips_known = cantrips_known
        self.spells_known = spells_known
        self.list_class_cantrips = list_class_cantrips
        self.list_class_spells = list_class_spells
        
        self.class_id = class_id
        self.prepared_caster = prepared_caster
        
        self.cantrip_1 = cantrip_1
        self.cantrip_2 = cantrip_2
        self.cantrip_3 = cantrip_3
        self.spell_1 = spell_1
        self.spell_2 = spell_2
        self.spell_3 = spell_3
        self.spell_4 = spell_4
        self.spell_5 = spell_5
        self.spell_6 = spell_6
    
    def retrieve_class_spell_list(self):
        self.list_class_cantrips = class_spells_by_spell_level(self.class_id,0)
        self.list_class_spells = class_spells_by_spell_level(self.class_id,1)
        return True
    
    def set_cantrip_1(self, value):
        if value in self.list_class_cantrips:
            self.cantrip_1 = value
            return True
        else:
            print("Error: cantrip not in list")
            return False
    def rm_cantrip_1(self):
        self.cantrip_1 = None
        return True
    
    def set_cantrip_2(self, value):
        if value in self.list_class_cantrips:
            self.cantrip_2 = value
            return True
        else:
            print("Error: cantrip not in list")
            return False
    def rm_cantrip_2(self):
        self.cantrip_2 = None
        return True
    
    def set_cantrip_3(self, value):
        if value in self.list_class_cantrips:
            self.cantrip_3 = value
            return True
        else:
            print("Error: cantrip not in list")
            return False
    def rm_cantrip_3(self):
        self.cantrip_3 = None
        return True
    
    def set_spell_1(self, value):
        if value in self.list_class_spells:
            self.spell_1 = value
            return True
        else:
            print("Error: spell not in list")
            return False
    def rm_spell_1(self):
        self.spell_1 = None
        return True
    
    def set_spell_2(self, value):
        if value in self.list_class_spells:
            self.spell_2 = value
            return True
        else:
            print("Error: spell not in list")
            return False
    def rm_spell_2(self):
        self.spell_2 = None
        return True
    
    def set_spell_3(self, value):
        if value in self.list_class_spells:
            self.spell_3 = value
            return True
        else:
            print("Error: spell not in list")
            return False
    def rm_spell_3(self):
        self.spell_3 = None
        return True
    
    def set_spell_4(self, value):
        if value in self.list_class_spells:
            self.spell_4 = value
            return True
        else:
            print("Error: spell not in list")
            return False
    def rm_spell_4(self):
        self.spell_4 = None
        return True
    
    def set_spell_5(self, value):
        if value in self.list_class_spells:
            self.spell_5 = value
            return True
        else:
            print("Error: spell not in list")
            return False
    def rm_spell_5(self):
        self.spell_5 = None
        return True
    
    def set_spell_6(self, value):
        if value in self.list_class_spells:
            self.spell_6 = value
            return True
        else:
            print("Error: spell not in list")
            return False
    def rm_spell_6(self):
        self.spell_6 = None
        return True
    
    def confirm_list(self):
        if (self.cantrip_1 == None) or (self.cantrip_2 == None) or (self.cantrip_3 == None) or \
        (self.spell_1 == None) or (self.spell_2 == None) or (self.spell_3 == None) or \
        (self.spell_4 == None) or (self.spell_5 == None)or (self.spell_6 == None):
            print("Error: unassigned cantrips or spells")
            return False
        self.spells_known = []
        self.spells_known.append(int(self.cantrip_1))
        self.spells_known.append(int(self.cantrip_2))
        self.spells_known.append(int(self.cantrip_3))
        self.spells_known.append(int(self.spell_1))
        self.spells_known.append(int(self.spell_2))
        self.spells_known.append(int(self.spell_3))
        self.spells_known.append(int(self.spell_4))
        self.spells_known.append(int(self.spell_5))
        self.spells_known.append(int(self.spell_6))
        var_count = 0
        last_index = len(self.spells_known)
        while var_count < (last_index - 1):
            var_next = var_count + 1
            while var_next <= last_index:
                if self.spells_known[var_count] == self.spells_known[var_next]:
                    print("Error: spell chosen multiple times.")
                    return False
                var_next += 1
        return True
    
    def reset_spells(self):
        self.spells_known = []
        self.cantrip_1 = None
        self.cantrip_2 = None
        self.spell_1 = None
        self.spell_2 = None
        self.spell_3 = None
        self.spell_4 = None
        return True

  