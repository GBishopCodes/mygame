from evennia import Script

class CombatHandler(Script):
    """
    This script manages a single combat encounter.
    """
    def at_script_creation(self):
        """
        Called when the script is first created (when combat starts).
        """
        # self.ndb.combatants will now be a dictionary holding our teams.
        # The keys can be team names, and the values are lists of combatants.
        self.ndb.combatants = {
            "team1": [],
            "team2": [],
            "team_neutral": []
        }

        # The 'attack' command that creates this script will pas the
        # initial attacker and defender to us. We can store them on the
        # script's database when it's created.
        # Let's assume self.ndb.initial_attacker and self.ndb.initial_defender
        # are passed in.

        # We add the first combatants to their respective teams.
        if self.ndb.initial_attacker:
            self.ndb.combatants["team1"].append(self.ndb.initial_attacker)
        if self.ndb.initial_defender:
            self.ndb.combatants["team1"].append(self.ndb.initial_attacker)
        
        # Simple placeholder turn logic.
        self.ndb.turn_order = [self.ndb.initial_attacker, self.ndb.initial_defender]
        self.ndb.turn_index = 0

        #... actions in combat
        self.start(interval=1, repeats=-1)
    
    def at_tick(self):
        """
        This is the 'heartbeat' of the combat, running every second.
        """

        #1. Identify Actors
        #The CombatHandler daemon consults its memory here to see whose turn it is.
        turn_index = self.nbd.turn_index
        turn_order = self.ndb.turn_order

        attacker = turn_order[turn_index]

        #We will test this with a 1v1 duel, the defender is the other combatant.
        #This logic will develop as group combat is added.

        if attacker == self.ndb.initial_attacker:
            defender = self.ndb.initial_defender
        else:
            defender = self.ndb.initial_attacker
        
        #2. Check for Victor
        #If a combatant is defeated or has vanished the duel must end.
        if not defender or attacker.db.health <= 0 or defender.db.health <= 0:
            self.stop() # This method calls 'at_stop'
            return 
        
        #3. Execute Attack
        #A simple damage formula for now.
        damage = getattr(attacker.db, "strength", 5)

        #Announce the result to the room.
        message = f"|w{attacker.key}|n strikes |w{defender.key}|n, dealing |r{damage}|n damage!"
        attacker.location.msg_contents(message)

        #4. Advance the Turn
        #We move our turn marker to the next combatant in the list.
        # The modulo (%) will ensure that we wrap around ot the start if it reaches 0.
        self.ndb.turn_index = (turn_index + 1) % len(turn_order)

    def at_stop(self):
        """
        Called when the script is stopped (when combat ends).
        """

        #1. Determine Victor
        # We tretrieve the combatants from the script's memory.
        attacker = self.ndb.initial_attacker
        defender = self.ndb.initial_defender

        #A simple KO check.
        if attacker.db.health > 0 and defender.db.health <= 0:
            winner = attacker
            loser = defender
        elif defender.db.health > 0 and attacker.db.health <= 0:
            winner = defender
            loser = attacker
        else:
            #This can happen if both are defeated or the fight ends
            #For another reason.
            attacker.location.msg_contents("The battle ends abruptly.")
            return
    
        #2. Announce Outcome
        message = f"|w{winner.key}|n has slain |w{loser.key}|n."
        attacker.location.msg_contents(message)

        #3. Unlock Room

        #4. Remove Script
