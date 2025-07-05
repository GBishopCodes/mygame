"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""

from evennia.objects.objects import DefaultCharacter

from .objects import ObjectParent
import random

class Character(ObjectParent, DefaultCharacter):
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
    pass

    def at_pre_move(self, destination, **kwargs):
        """
        Called by self.move_ when trying to move somewher.
        If this returns False the move is cancelled.
        """
        if self.db.is_sitting:
            self.msg("You need to stand up first.")
            return False
        return True

class ProfessorNPC(Character):
    """
    A specific type of Character that represents a Professor NPC.
    This can be used to create non-player characters with specific attributes.
    """
    def at_object_creation(self):
        """
        This is called when the object is created.
        """
        super().at_object_creation()
        self.cmdset.add("professor_cmdset", permanent=True)
    
    def get_display_name(self, looker, **kwargs):
        """
        Returns a display name for the NPC.
        This can be customized to include titles or other attributes.
        """
        return f"|w{self.key}|n"