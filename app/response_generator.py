import ollama
import sys
import logging

class ResponseGenerator:
	def __init__(self, model='llama3'):
		self.model = model
		
		# download only if needed
		needs_pull = True
		for available_model in ollama.list().models:
			name = available_model.model.split(':')[0]
			logging.debug(f"Available ollama model: {name}")
			if name == self.model:
				needs_pull = False

		if needs_pull:
			logging.info(f"Pulling model: {self.model}")
			ollama.pull(self.model)

	def generate_response(self, chat_history):
		response = ollama.chat(model=self.model, messages=chat_history)
		return response['message']['content']

if __name__ == "__main__":
	user_input = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Hello, how can you help me?"
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
