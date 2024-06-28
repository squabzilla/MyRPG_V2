class generate_magic_classIDs:
    def __init__(self,
                 Barbarian = 0, Bard = 1, Cleric = 2, Druid = 3,
                 Fighter = 4, Monk = 5, Paladin = 6, Ranger = 7,
                 Rogue = 8, Sorcerer = 9, Warlock = 10, Wizard = 11):
        self.Barbarian = Barbarian
        self.Bard = Bard
        self.Cleric = Cleric
        self.Druid = Druid
        self.Fighter = Fighter
        self.Monk = Monk
        self.Paladin = Paladin
        self.Ranger = Ranger
        self.Rogue = Rogue
        self.Sorcerer = Sorcerer
        self.Warlock = Warlock
        self.Wizard = Wizard

class generate_magic_abilityIDs:
    def __init__(self, strength = 0, dexterity = 1, constitution = 2, 
                 intelligence = 3, wisdom = 4, charisma = 5):
        self.strength = strength
        self.dexterity = dexterity
        self.constitution = constitution
        self.intelligence = intelligence
        self.wisdom = wisdom
        self.charisma = charisma