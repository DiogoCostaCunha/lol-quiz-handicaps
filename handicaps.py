import random
import keyboard

class HandicapManager:
    
    def __init__(self, app):
        self.app = app
        self.active_handicaps = []
        
    def apply_random_handicap(self, time_left_to_answer) -> None:
        handicaps = [
            {"keys": ["q"]},
            {"keys": ["w"]},
            {"keys": ["e"]},
            {"keys": ["r"]},
            {"keys": ["d"]},
            {"keys": ["f"]},
        ]
        
        chosen = random.choice(handicaps)
        
        # if we're already using all handicaps
        if len(self.active_handicaps) == len(handicaps):
            return None
        
        # check if we're already using this handicap
        for ah in self.active_handicaps:
            for key in chosen["keys"]:
                if key in ah["keys"]:
                    return self.apply_random_handicap(time_left_to_answer)
        
        if time_left_to_answer < 1:
            time_left_to_answer = 1
        
        # Handicap lasts longer the longer you take to answer
        rand_time_factor = random.randint(30, 110)
        chosen['duration'] = rand_time_factor + round(20 * (1/(time_left_to_answer)), 0)
    
        for key in chosen["keys"]:
            keyboard.block_key(key)
        
        self.active_handicaps.append(chosen)    
        
    def return_active_handicaps(self) -> str:
        if len(self.active_handicaps) == 0:
            return None
        else:
            handicaps = ""
            for key in self.active_handicaps["keys"]:
                handicaps += f"{key} "
            return handicaps 
        
    def remove_active_handicap(self, h) -> None:
        for ah in self.active_handicaps:
            for key in h['keys']:
                if key in ah['keys']:
                    self.active_handicaps.remove(ah)
                    keyboard.unblock_key(key)
                    return None

