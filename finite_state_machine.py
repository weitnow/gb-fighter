from enum import Enum, auto
import time



class Emily():
    def __init__(self):
        self.current_state = 'init'
        self.prev_state = ''
        self.new_state = ''

        self.running_count = 0

    def update_state(self):
        if self.new_state != '':
            if new_state != self.current_state:
                init_method = "_init_" + self.new_state 
                end_method = "_end_" + self.current_state

                self.if_has_method_call_it(end_method)

                self.prev_state = self.current_state
                self.current_state = self.new_state
                self.new_state = ''

                self.if_has_method_call_it(init_method)

            else:
                new_state = ''
      
    def if_has_method_call_it(self, method: str):
        if hasattr(self, method) and callable(getattr(self, method)):
            method = getattr(self, method)
            method()

    def process_state(self):
        self.if_has_method_call_it('_' + self.current_state)

    def _init(self):
        self.new_state = "running"
        print("Example init")

    def _init_running(self):
        print("Entering run mode")

    def _running(self):
        print("I am running so fast rn ngl")
        self.running_count += 1
        if self.running_count >= 10:
            self.new_state = "stopped"

    def _end_running(self):
        print("Okay, slowing down now, ending running")

    def _init_stopped(self):
        print("System has stopped")


il_gatto = Emily()
for i in range(12):
    il_gatto.process_state()


class States(Enum):
    IDLE = auto()
    CHASE = auto()
    ATTACK = auto()
    DEATH = auto()


class GameObject:
    def __init__(self):
        self.__state = States.IDLE

    def set_state(self, state):
        self.__state = state

    def get_state(self):
        return self.__state
    

class Entity(GameObject):
    def __init__(self):
        super().__init__()
        self.__health = 100

    def sub_health(self):
        self.__health -= 20

    def get_health(self):
        return self.__health
    
    def set_health(self, health):
        self.__health = health

player = Entity()
player.set_state(States.ATTACK)

enemy = Entity()
enemy.set_state(States.CHASE)

while False:
    if player.get_state() == States.ATTACK:
        print("player attacking!")
        enemy.sub_health()
        if enemy.get_state() != States.ATTACK:
            enemy.set_state(States.ATTACK)
        if enemy.get_health() <= 0:
            enemy.set_state(States.DEATH)
            print("enemy died")
            break
    elif player.get_state() == States.DEATH:
        print("player died")
        break
    if enemy.get_state() == States.ATTACK:
        print("enemy attacking!")
        player.sub_health()
        if player.get_health() <= 0:
            player.set_state(States.DEATH)
            print("player died")
            break

    time.sleep(1)

""" print("------------------------------")
print("player's health ", player.get_health())
print("enemy's health ", enemy.get_health()) """