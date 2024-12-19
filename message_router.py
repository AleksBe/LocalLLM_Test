import json
import aiohttp

class MessageRouter:
    def __init__(self):
        self.api_url = "http://127.0.0.1:1234/v1/chat/completions"
        
    async def get_llm_response(self, message: str) -> str:
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "messages": [
                        {
                            "role": "system",
                            "content": "Ты - полезный ассистент. Отвечай кратко и по существу."
                        },
                        {
                            "role": "user",
                            "content": message
                        }
                    ],
                    "model": "llama-3.2-3b-instruct",
                    "temperature": 0.7,
                    "max_tokens": 800
                }
                
                async with session.post(
                    self.api_url,
                    json=payload,
                    headers={"Content-Type": "application/json"}
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result['choices'][0]['message']['content']
                    else:
                        return f"Ошибка: Статус {response.status}"
                        
        except Exception as e:
            return f"Произошла ошибка при обработке запроса: {str(e)}"
