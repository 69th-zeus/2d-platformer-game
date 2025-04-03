import json
from os.path import join

class Data:
    def __init__(self, ui):
        self.__coins = 0
        self.__health = 5
        self.ui = ui
        self.ui.create_hearts(self.__health)
        
        self.unlocked_level = 0
        self.current_level = 0
    
    @property # getter
    def coins(self):
        return self.__coins
    
    @coins.setter #setter
    def coins(self, value):
        self.__coins = value
        if self.coins >= 100:
            self.coins -= 100
            self.health += 1
        self.ui.show_coins(self.__coins)
    
    @property # getter
    def health(self):
        return self.__health
    
    @health.setter #setter
    def health(self, value):
        self.__health = value
        self.ui.create_hearts(value)
        
    def save_state(self):
        self.state = {
                        "coins" : self.__coins,
                        "health" : self.__health,
                        "unlocked_level" : self.unlocked_level,
                        "current_level": self.current_level
                    }
        with open(join('data', 'save.txt'), 'w') as save_state:
            json.dump(self.state, save_state)
    
    def load_state(self, dt):
        with open(join('data', 'save.txt')) as save_state:
            self.state = json.load(save_state)
            self.__coins = self.state['coins']
            self.__health = self.state['health']
            self.unlocked_level = self.state['unlocked_level']
            self.current_level = self.state['current_level']
            self.ui.update(dt)
            self.ui.create_hearts(self.__health)
    