from typeclasses.objects import Object
from commands.mycommands import CmdHit

class Weapon(Object):
    """
    Base class for all weapons.
    """
    
    def at_object_creation(self):
        """
        This is called when the object is created.
        """
        super().at_object_creation()
        self.db.damage = 10  # Default damage value
        self.db.type = "melee"  # Default type of weapon (melee/ranged)

class Sword(Weapon):
    """
    A sword weapon type.
    """
    
    def at_object_creation(self):
        """
        This is called when the object is created.
        """
        super().at_object_creation()
        self.db.damage = 15  # Swords typically do more damage
        self.db.type = "melee"
    
    def do_hit(self, target):
        """
        Hit a target with the sword.
        
        Args:
            target (Object): The target to hit.
        """
        CmdHit().func(self, target, weapon=self)  # Use the CmdHit command logic
    