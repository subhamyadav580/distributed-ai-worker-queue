from ai_model.llm import LLM


llm = LLM()


def generate_chat_response(prompt: str):
    return llm.generate_response(prompt)