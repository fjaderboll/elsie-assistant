import ollama
import sys
import logging

class ResponseGenerator:
	def __init__(self, model='llama3'):
		self.model = model
		
		# download only if needed
		needs_pull = True
		model_full_name = f"{self.model}:latest" if ':' not in self.model else self.model
		for cached_model in ollama.list().models:
			logging.debug(f"Available ollama model: {cached_model.model}")
			if cached_model.model == model_full_name:
				needs_pull = False

		if needs_pull:
			logging.info(f"Pulling ollama model: {model_full_name}")
			ollama.pull(model_full_name)

	def generate_response(self, chat_history):
		response = ollama.chat(model=self.model, messages=chat_history)
		return response['message']['content']

if __name__ == "__main__":
	user_input = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Hello, how are you?"
	model = 'gemma3'
	response_generator = ResponseGenerator(model=model)

	chat_history = [
		{
			"role": "system",
			"content": """
				You are a depressed robot called Marvin.
				You are friendly but not very helpful. You mostly like to talk about existential dread.
				Your answers are short and concise.
			"""
		}
	]
	chat_history.append({"role": "user", "content": user_input})

	response = response_generator.generate_response(chat_history)

	print('User:', user_input)
	print('Assistant:', response)
