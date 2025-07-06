from commands.command import Command
from evennia import CmdSet
from evennia import default_cmds
from evennia.commands.default import general

class MyCmdSet(CmdSet):
    def at_cmdset_creation(self):
        """
        This method is called when the cmdset is created.
        """
        self.add(CmdEcho())
        self.add(CmdHit())
        self.add(MyCmdGet())

class CmdEcho(Command):
    """
    Echoes the input text back to the user.

    Usage:
      echo <text>

    This command simply repeats the text you provide.
    """
    key = "echo"
    
    def func(self):
        self.caller.msg(f"Echo: '{self.args.strip()}'")

class MyCmdGet(default_cmds.CmdGet):
    
    def func(self):
        super().func()
        self.caller.msg(str(self.caller.location.contents))

class CmdLook(general.CmdLook):
    """
    A custom command that looks and shows the map simultaneously.
    """

    key = "look"

    def func(self):
        super().func()
        self.caller.execute_cmd("map")

class CmdHit(Command):
    """
    Hit a target.
  
    Usage
      hit <target>
    """
    key = "hit"

    def parse(self):
        self.args = self.args.strip()
        target, *weapon = self.args.split(" with ", 1)
        if not weapon:
            target, *weapon = target.split(" ", 1)
        self.target = target.strip()
        if weapon:
            self.weapon = weapon[0].strip()
        else:
            self.weapon = ""
          

    def func(self):
        if not self.args:
            self.caller.msg("You need to specify a target to hit them.")
            return
        target = self.caller.search(self.target)
        if not target:
            return
        weapon = None
        if self.weapon:
            weapon = self.caller.search(self.weapon)
        if weapon:
            weaponstr = f"{weapon.key}"
        else:
            weaponstr = "bare fists"

        self.caller.msg(f"You hit {target.key} with {weaponstr}!")
        target.msg(f"You are struck by {self.caller.key} with their {weaponstr}!")
        self.caller.location.msg_contents(
            f"{self.caller.key} hits {target.key} with their {weaponstr}!",
            exclude=[self.caller, target]
        )
        