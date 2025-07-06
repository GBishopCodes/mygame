from evennia import Command, CmdSet
from evennia import InterruptCommand

class CmdSit2(Command):
    """
    Sit down.

    Usage:
        sit <sittable>
    """
    key = "sit"

    def parse(self):
        self.args = self.args.strip()
        if not self.args:
            self.caller.msg("Sit on what?")
            raise InterruptCommand

    def func(self):
        sittable = self.caller.search(self.args)
        if not sittable:
            return
        try:
            sittable.do_sit(self.caller)
        except AttributeError:
            self.caller.msg("You can't sit on that!")

class CmdStand2(Command):
    """
    Stand up.

    Usage:
        stand

    """
    key = "stand"

    def func(self):
        caller = self.caller
        # if we are sitting, this should be set on us
        sittable = caller.db.is_sitting
        if not sittable:
            caller.msg("You are not sitting down.")
        else:
            sittable.do_stand(caller)

class CmdNoSitStand(Command):
    """
    Sit down or stand up from a sittable object.
    """
    key = "sit"
    aliases = ["stand"]

    def func(self):
        if self.cmdname == "sit":
            self.msg("You have nothing to sit on.")
        else:
            self.msg("You are not sitting down.")    

class CmdSetSit(CmdSet):
    """
    This is the cmdset for objects that can be sat on.
    """
    priority = 1
    def at_cmdset_creation(self):
        """
        This method is called when the cmdset is created.
        """
        self.add(CmdSit2())
        self.add(CmdStand2())