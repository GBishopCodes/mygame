from evennia import Command, CmdSet

class CmdSit(Command):
    """
    Sit down on chair or similar object.
    """
    key = "sit"
    def func(self):
        self.obj.do_sit(self.caller)

class CmdStand(Command):
    """
    Stand up from chair or similar object.
    """
    key = "stand"
    def func(self):
        self.obj.do_stand(self.caller)

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
        self.add(CmdSit())
        self.add(CmdStand())