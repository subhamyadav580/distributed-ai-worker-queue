from litellm import completion
from config.settings import Settings

settings = Settings()



class LLM:
    def __init__(self):
        pass

    def generate_response(self, prompt: str) -> str:
        print("settings.model_name:: ", settings.model_name)
        print("settings.ollama_base_url:: ", settings.ollama_base_url)
        response = completion(
            model=f"{settings.provider}/{settings.model_name}", 
            messages=[
                { 
                    "role": "user",
                    "content": f"{prompt}"
                }
            ], 
            api_base=settings.ollama_base_url
        )
        return response.choices[0].message.content