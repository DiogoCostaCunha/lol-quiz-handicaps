from questions import QuestionManager
from handicaps import HandicapManager
from openai import OpenAI
from dotenv import load_dotenv
import os
import logging
from gui import AppGUI
import threading
import time
from enums import AppState
import pygame
import keyboard

class App:
    
    def __init__(self, OPENAI_KEY):
        self.gui = AppGUI(self)
        self.q_manager = QuestionManager(self, OpenAI(api_key=OPENAI_KEY))
        self.h_manager = HandicapManager(self)
        self.answers_right = 0
        self.answers_wrong = 0
        self.time_till_question_limits = [30, 70] # seconds - goes up or down depending on right and wrong answers
        self.std_time_till_question = round(sum(self.time_till_question_limits) / len(self.time_till_question_limits))
        self.time_till_question = self.std_time_till_question
        
        # seconds - time to answer depends on question difficulty, goes up 20 seconds per level
        self.std_time_to_answer = [35+i*15 for i, _ in enumerate(self.q_manager.difficulties)] 
        
        self.state = AppState.CONFIGS
        self.load_sounds()
        
    def load_sounds(self):
        pygame.init()
        pygame.mixer.init()
        self.sounds = {
            'correct': pygame.mixer.Sound('assets/sounds/correct.mp3'),
            'wrong': pygame.mixer.Sound('assets/sounds/wrong.mp3'),
            'new_question': pygame.mixer.Sound('assets/sounds/new_question.mp3')
        }
        for sound in self.sounds:
            self.sounds[sound].set_volume(0.1)
        self.sounds['wrong'].set_volume(0.05)

    
    def run(self):
        self.gui.spawn_window()
        self.gui.tk.mainloop()
        
    def start_game(self):   
        main_thread = threading.Thread(target=self.main)
        main_thread.daemon = True
        main_thread.start()
        
    def spawn_new_question(self):
        question_json, question_str, topic, difficulty = self.q_manager.fetch_question()
        self.time_to_answer = self.std_time_to_answer[self.q_manager.difficulties.index(difficulty)]
        self.sounds['new_question'].play()
        self.gui.update_label(f"{question_str}", "question")
        self.gui.update_label(f"{self.answers_right}", "answers_right")
        self.gui.update_label(f"{self.answers_wrong}", "answers_wrong")
        self.gui.update_label(f"{topic}", "topic")
        self.gui.update_label(f"{difficulty}", "difficulty")
        self.gui.update_label(f"Time left: {self.time_to_answer}", "timer")
        return question_json
        
    def decrement_timers(self):
        
        while True:
            
            if self.time_to_answer > 0 and self.state == AppState.WAITING_ANSWER:
                self.time_to_answer -= 1
                
            for h in self.h_manager.active_handicaps:
                h['duration'] -= 1
                if h['duration'] == 0:
                    self.h_manager.remove_active_handicap(h)
                    
            time.sleep(1)

    def main(self):
        question_json = self.spawn_new_question()
        decrement_timers_thread = threading.Thread(target=self.decrement_timers)
        decrement_timers_thread.start()
        self.state = AppState.WAITING_ANSWER
        
        while True:
            
            # update handicaps labels
            h_str = "Handicaps: "
            for h in self.h_manager.active_handicaps:
                for h_key in h['keys']:
                    h_str += f"\n {h_key} ({h['duration']})"
            self.gui.update_label(h_str, 'handicaps')

            if self.state == AppState.WAITING_ANSWER:
                self.gui.update_label(f"Time left: {self.time_to_answer}", "timer")
                
                answer = self.listen_for_answer()
                
                veredict = answer == question_json['correct_choice']
                
                if veredict:
                    self.answered_right()
                    
                elif (veredict is False and answer is not None) or self.time_to_answer == 0:
                    self.answered_wrong()
                    self.gui.update_label(f"Correct was {question_json['correct_choice']}) {question_json['options'][question_json['correct_choice']]}", "question")
                    time.sleep(4)
                
        
                if answer is not None or self.time_to_answer == 0:
                    self.state = AppState.WAITING_QUESTION
                    self.gui.remove_label("timer")
                    self.gui.remove_label("topic")
                    self.gui.remove_label("difficulty")
                    self.time_till_question = self.std_time_till_question
                    
            elif self.state == AppState.WAITING_QUESTION:
                self.time_till_question -= 1 
                to_display = f"Next question in {self.time_till_question}"
                self.gui.update_label(to_display, "question")
                time.sleep(1)
                
                if self.time_till_question == 0:
                        
                    self.time_till_question = self.std_time_till_question
                        
                    question_json = self.spawn_new_question()
                    self.state = AppState.WAITING_ANSWER
            
    def listen_for_answer(self):
        answer_keys = ['7', '8', '9', '0']
        answer_options = ['a', 'b', 'c', 'd']
        for i, key in enumerate(answer_keys):
            if keyboard.is_pressed(key):
                return answer_options[i]
        return None
    
    def answered_wrong(self):
        self.sounds['wrong'].play()
        self.answers_wrong += 1
        self.std_time_till_question -= 15
        if self.std_time_till_question <= self.time_till_question_limits[0]:
            self.std_time_till_question = self.time_till_question_limits[0]
        self.gui.update_label(f"{self.answers_wrong}", "answers_wrong")
        self.h_manager.apply_random_handicap(self.time_to_answer)
        
    def answered_right(self):
        self.sounds['correct'].play()
        self.answers_right += 1
        self.std_time_till_question += 10
        if self.std_time_till_question >= self.time_till_question_limits[1]:
            self.std_time_till_question = self.time_till_question_limits[1]
        self.gui.update_label(f"{self.answers_right}", "answers_right")
    
        
if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    load_dotenv()
    OPENAI_KEY = os.getenv('OPENAI_KEY')
    app = App(OPENAI_KEY)
    app.run()