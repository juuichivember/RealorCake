from elementState import BaseState, BCreamState, LCreamState, MCreamState, TCreamState, ToppingState

# State Manager สำหรับพวก Element States ใน Decoration State
class ElementStateManager:
    def __init__(self):
        self.states = {
            "base": BaseState(),
            "behindcream": BCreamState(),
            "lowercream": LCreamState(),
            "middlecream": MCreamState(),
            "topcream": TCreamState(),
            "topping": ToppingState()
        }
        self.current_state = "base"

    def set_state(self, new_state):
        self.current_state = new_state
        self.states[self.current_state].enter()

    def update(self):
        next_state = self.states[self.current_state].update()
        if next_state != self.current_state:
            self.set_state(next_state)

    def draw(self, screen):
        self.states[self.current_state].draw(screen)
