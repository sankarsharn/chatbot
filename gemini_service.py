import google.generativeai as genai

class GeminiService:
    def __init__(self):  
        API_KEY = "AIzaSyDcGXJBf0drJ9vOEq7KL4qmCyz7AXvnEsQ"  # 🔴 Replace with env variable
        genai.configure(api_key=API_KEY)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        self.history = []  # Stores conversation
        self.score = 0  # ✅ Tracks user score
        self.current_question = None  # ✅ Stores active question
        self.bot_answer = None  # ✅ Stores Gemini's answer
        self.user_answer = None  # ✅ Stores user's answer

    # ✅ Step 1: Receive a finance question
    def receive_question(self, question):
        self.current_question = question
        self.user_answer = None  # Reset previous answer
        self.bot_answer = None  # Reset bot's answer
        return "Question received."

    # ✅ Step 2: Generate Gemini’s answer
    def generate_answer(self):
        if not self.current_question:
            return "No question received. Please provide a question first."
        
        response = self.model.generate_content(f"Answer this finance question: {self.current_question}")
        self.bot_answer = response.text.strip()  # Store Gemini's answer
        return self.bot_answer

    # ✅ Step 3: Receive user’s answer
    def submit_user_answer(self, user_answer):
        if not self.current_question:
            return "No active question. Please provide a question first."
        
        self.user_answer = user_answer.strip()  # Store user's answer
        return "Your answer has been recorded. Ask for evaluation."

    # ✅ Step 4: Evaluate user’s answer (Grades from 1 to 10)
    def evaluate_answer(self):
        if not self.current_question or not self.user_answer:
            return "No answer to evaluate. Please provide an answer first."

        if not self.bot_answer:
            self.generate_answer()  # Ensure we have Gemini's answer

        # ✅ Ask Gemini to grade the user's answer
        prompt = f"""
        Compare these two answers:
        1️⃣ Bot's Answer: "{self.bot_answer}"
        2️⃣ User's Answer: "{self.user_answer}"
        
        Grade the user's answer on a scale of 1 to 10.
        - 10: Perfect match, excellent explanation
        - 7-9: Good answer, missing minor details
        - 4-6: Partially correct, lacks key details
        - 1-3: Incorrect or mostly wrong
        - 0: Completely unrelated

        Return only the score (integer from 0 to 10).
        """
        response = self.model.generate_content(prompt)
        
        try:
            grade = int(response.text.strip())  # Extract Gemini’s score
        except ValueError:
            grade = 0  # Default to 0 if Gemini's response is not valid
        
        self.score += grade  # Add to total score
        
        result = f"Your answer was graded {grade}/10.\nGemini's answer: {self.bot_answer}"
        
        # ✅ Reset question & answer tracking
        self.current_question = None
        self.user_answer = None
        self.bot_answer = None

        return result

    # ✅ Get user's current score
    def get_score(self):
        return f"Your total score is: {self.score}"
