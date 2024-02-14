
   
    
def multiple_choice_question(topic: str, difficulty: str) -> str:
    return f"""
        Generate a very SHORT random multiple choice question based on the topic {topic} and difficulty {difficulty}.
        Format your output in a .json as follows:
        {{
            "question": <insert question>,
            "options": {{
                "a": <insert option a>,
                "b": <insert option b>,
                "c": <insert option c>,
                "d": <insert option d>
            }},
            "correct_choice": <insert only the correct choice letter>
        }}
    """

