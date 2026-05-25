from ai_model.llm import LLM


llm = LLM()


def generate_ai_summary(prompt: str):
    return llm.generate_response(prompt)