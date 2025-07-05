from typeclasses.objects import Object

class Monster(Object):
    """
    Base class for all monsters.
    """
    def move_around(self):
        print(f"{self.key} moves around.")

class Dragon(Monster):
    """
    A dragon monster.
    """

    def move_around(self):
        super().move_around()
        print(f"{self.key} flares its wings and looks ready to dive.")
        print(f"{self.key} the air cracks with a thunderous quake.")
    def firebeath(self):
        """
        Let the dragon breathe fire.
        """
        print(f"{self.key} breathes fire!") 