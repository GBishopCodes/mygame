from typeclasses.objects import Object
from commands.sittables import CmdSetSit

class Sittable(Object):

    def at_object_creation(self):
        """
        This is called when the object is created.
        """
        super().at_object_creation()
        self.cmdset.add_default(CmdSetSit)

    def do_sit(self, sitter):
        """
        Called when trying to sit on/in this object.
        
        Args:
            sitter (Object): The one trying to sit down.
        
        """
        preposition = self.db.preposition or "on"
        current = self.db.sitter
        if current:
            if current == sitter:
                sitter.msg(f"You are already sitting {preposition} {self.key}.")
            else:
                sitter.msg(f"{current.key} is already sitting {preposition} {self.key}.")
            return
        self.db.sitter = sitter
        sitter.db.is_sitting = True
        sitter.msg(f"You sit down {preposition} {self.key}.")

    def do_stand(self, stander):
        """
        Called when trying to stand up from this object.
        
        Args:
            sitter (Object): The one trying to stand up.
        
        """
        current = self.db.sitter
        if not stander == stander:
            stander.msg(f"You are not sitting {self.db.preposition} {self.key}.")
            return
        self.db.sitter = None
        del stander.db.is_sitting
        stander.msg(f"You stand up from {self.key}.")