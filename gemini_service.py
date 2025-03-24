import google.generativeai as genai
import re

class GeminiService:
    def __init__(self):
        # Initialize the Gemini model
        API_KEY = "MY_API_KEY"  # Replace with your actual Gemini API key
        genai.configure(api_key=API_KEY)
        self.model = genai.GenerativeModel('gemini-2.0-flash')  # Use 'gemini-pro' or the appropriate model name

        # Initialize conversation history and other attributes
        self.history = []  # Stores conversation history
        self.score = 0     # Tracks user score
        self.current_question = None  # Stores active question
        self.bot_answer = None  # Stores Gemini's answer
        self.user_answer = None  # Stores user's answer

    def receive_question(self, question):
        if not question or not isinstance(question, str):
            raise ValueError("Invalid question provided")
        
        # Set the current question
        self.current_question = question
        
        # Add the question to the conversation history
        self.history.append({"role": "user", "text": question})
        
        return "Question received."

    def generate_answer(self):
        if not self.current_question:
            raise ValueError("No question received. Please provide a question first.")
        
        # Generate a response using the Gemini model
        prompt = f"Answer this finance question: {self.current_question}"
        response = self.model.generate_content(prompt)
        raw_answer = response.text  # Get the raw answer
        self.bot_answer = self._clean_text_format(raw_answer)  # Clean and store the bot's answer
        self.history.append({"role": "bot", "text": self.bot_answer})  # Add bot's answer to history
        return self.bot_answer

    def submit_user_answer(self, user_input):
        if not user_input or not isinstance(user_input, str):
            raise ValueError("Invalid user input")
        
        # Store the user's answer
        self.user_answer = user_input.strip()
        
        # Add the user's answer to the conversation history
        self.history.append({"role": "user", "text": self.user_answer})
        
        return "Your input has been recorded. Ask for evaluation or continue the conversation."

    def evaluate_answer(self):
        if not self.current_question or not self.user_answer:
            raise ValueError("No question or answer provided for evaluation.")
        
        # Ensure we have Gemini's answer
        if not self.bot_answer:
            self.generate_answer()
        
        # Evaluate the user's answer
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
        
        # Extract the score from the response
        try:
            # Use regex to find the first integer in the response
            match = re.search(r'\b\d+\b', response.text)
            if match:
                grade = int(match.group())
            else:
                grade = 0  # Default to 0 if no integer is found
        except Exception as e:
            print(f"Error parsing response: {e}")
            grade = 0  # Default to 0 in case of any error
        
        self.score += grade  # Add to total score
        
        result = f"Your answer has been evaluated. Score: {grade}/10.\nGemini's answer: {self.bot_answer}"
        return result

    def continue_conversation(self, user_input):
        if not user_input or not isinstance(user_input, str):
            raise ValueError("Invalid user input")
        
        # Add the user's follow-up to the conversation history
        self.history.append({"role": "user", "text": user_input})
        
        # Generate a contextual response using the entire conversation history
        prompt = "Continue the conversation based on the following context:\n"
        for msg in self.history:
            prompt += f"{msg['role']}: {msg['text']}\n"
        
        response = self.model.generate_content(prompt)
        raw_response = response.text.strip()
        bot_response = self._clean_text_format(raw_response)  # Clean the response
        self.history.append({"role": "bot", "text": bot_response})  # Add bot's response to history
        return bot_response

    def reset_conversation(self):
        self.history = []
        self.current_question = None
        self.user_answer = None
        self.bot_answer = None
        return "Conversation reset."
    
    def _clean_text_format(self, text):
        """
        Clean the formatting from the text while preserving proper spacing.
        Remove markdown formatting but maintain paragraph breaks and list structure.
        """
        # Remove markdown formatting for bold and italic (asterisks)
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # Remove bold (**text**)
        text = re.sub(r'\*(.*?)\*', r'\1', text)      # Remove italic (*text*)
        
        # Handle bullet points with proper spacing
        text = re.sub(r'^\s*[\*\-\+]\s+(.*?)$', r'• \1\n', text, flags=re.MULTILINE)
        
        # Remove backticks for code formatting
        text = re.sub(r'`(.*?)`', r'\1', text)
        
        # Handle numbered lists with proper spacing
        text = re.sub(r'^\s*(\d+)\.[\s]+(.*?)$', r'\1. \2\n', text, flags=re.MULTILINE)
        
        # Ensure proper paragraph spacing (replace single newlines with double newlines)
        text = re.sub(r'([^\n])\n([^\n])', r'\1\n\n\2', text)
        
        # Remove excessive blank lines (more than 2 consecutive newlines)
        text = re.sub(r'\n{3,}', r'\n\n', text)
        
        # Ensure the text ends with a single newline
        text = text.rstrip('\n') + '\n'
        
        return text