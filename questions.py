import json
import logging
import random
from prompts import multiple_choice_question

class QuestionManager:
    
    def __init__(self, app, oai_client):
        self.app = app
        self.oai_client = oai_client
        
        with open('configs.json', 'r') as file:
            data = json.load(file)
            
        self.topics = data['topics']
        self.difficulties = data['difficulties']
        
    def fetch_question(self, gpt_model="gpt-4"):
        topic = random.choice(self.topics)
        difficulty = random.choice(self.difficulties)
        if gpt_model is not None:
            q_json, q_str = self.generate_gpt_question(topic, difficulty, gpt_model)
        return q_json, q_str, topic, difficulty
        
    def generate_gpt_question(self, topic, difficulty, model, max_attempts=3):    
        prompt = multiple_choice_question(topic, difficulty)
        try: 
            result = self.oai_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=350
            ).choices[0].message.content
            
            result_json = json.loads(result)
            result_str = self.format_question_str(result_json)
            
        except Exception as e:
            max_attempts -= 1
            logging.info(f"Error generating question: {e}. Trying again...")
            if max_attempts > 0:
                result_json, result_str = self.generate_gpt_question(topic, difficulty, model, max_attempts)
            else:
                logging.error("Max attempts exceeded at generating gpt question. Returning None")
                result_json = None
                result_str = None
                
        return result_json, result_str

    def format_question_str(self, question_json):
        options_dict = {
            'a': '7',
            'b': '8',
            'c': '9',
            'd': '0'
        }
        question = question_json['question']
        options = question_json['options']
        formatted_question = f"{question}\n"
        for option in options:
            formatted_question += f"{options_dict[option]}: {options[option]}\n"
        return formatted_question
