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
    
    def at_death(self):
        """
        This hook is called when health reaches 0.
        """
        #Set Destination
        limbo_room = search.search_object_by_tag("limbo", category="rooms")
        study_room = search.search_object_by_tag("respawn_point", category="rooms")

        #A safeguard
        if not limbo_room or not study_room:
            self.location.msg_contents(f"|r{self.key}'s essence evaporates into fog...|0n")
            self.move_to(self.home, quiet=True)
            return
    
        # To Limbo
        self.move_to(limbo_room[0], quiet=True)
        self.msg("|xYou feel yourself lose grip to The Y'aand...|n")

        self.db.health = self.db.max_health or 100

        #Delay Return
        delay(3, self.return_from_limbo, destination=study_room[0])

    def return_from_limbo(self, destination):
        """
        A helper spell called by the 'delay' function to handle the final step.
        """
        self.msg("\n|wThe grey fog dissolves, and you find yourself in a familiar place.|n")
        self.move_to(destination, quiet=True)
        # We must manually trigger a "look" for the player.
        self.execute_cmd("look")


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