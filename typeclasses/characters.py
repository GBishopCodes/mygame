"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""

from evennia.objects.objects import DefaultCharacter
from evennia.utils import search, delay
from .objects import ObjectParent
import random
from evennia.contrib.rpg.rpsystem import ContribRPCharacter

class Character(ObjectParent, ContribRPCharacter):
    """
    The Character just re-implements some of the Object's methods and hooks
    to represent a Character entity in-game.

    See mygame/typeclasses/objects.py for a list of
    properties and methods available on all Object child classes like this.

    """
    
    def at_object_creation(self):
        """
        This is called when the object is created.
        """
        super().at_object_creation()
        self.db.strength = 10
        self.db.dexterity = 10
        self.db.intelligence = 10
        self.db.grit = 10
        self.db.wyrd = 10
        self.db.energy = 100
        self.db.health = 100
    
    def at_post_login(self, **kwargs):
        super().at_post_login(**kwargs)
        if self.db.first_login is None:
            study_room_id = "#86"
            study_room_list = search.search_object(study_room_id)

            if study_room_list:
                self.move_to(study_room_list[0])

            self.db.first_login = False
        
    def get_stats(self):
        """
        Returns a dictionary of the character's stats.
        """
        return {
            "strength": self.db.strength,
            "dexterity": self.db.dexterity,
            "intelligence": self.db.intelligence,
            "grit": self.db.grit,
            "wyrd": self.db.wyrd,
            "energy": self.db.energy,
            "health": self.db.health
        }
    
    def at_pre_move(self, destination, **kwargs):
        """
        Called by self.move_ when trying to move somewher.
        If this returns False the move is cancelled.
        """
        if self.db.is_sitting:
            self.msg("You need to stand up first.")
            return False
        return True
    
    def at_post_move(self, source_location, **kwargs):
        super().at_post_move(source_location, **kwargs)
        self.execute_cmd("map")
    
    def at_post_puppet(self):
        super().at_post_puppet()
        self.execute_cmd("map")

    
