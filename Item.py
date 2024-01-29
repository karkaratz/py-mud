class Item:

    def __init__(self, name, description, pickable=False, openable=False, breakable=False,
                 strength_bonus=0, speed_bonus=0, mana_bonus=0, stamina_bonus=0,
                 weight=1.0, durability=100, value=1, usable=False,
                 special_ability=None, rarity="Common", quest_related=False,
                 appearance_change=None):
        self.name = name
        self.description = description
        self.pickable = pickable
        self.openable = openable
        self.breakable = breakable
        self.strength_bonus = strength_bonus
        self.speed_bonus = speed_bonus
        self.mana_bonus = mana_bonus
        self.stamina_bonus = stamina_bonus
        self.weight = weight
        self.durability = durability
        self.value = value
        self.usable = usable
        self.special_ability = special_ability
        self.rarity = rarity
        self.quest_related = quest_related
        self.appearance_change = appearance_change

