import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

# В новой версии библиотеки модель называется так:
model = genai.GenerativeModel("gemini-2.0-flash")

async def ask_gemini(prompt: str) -> str:
    """Отправляет запрос к Gemini и возвращает ответ"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"✨ Звёзды временно молчат... Попробуй позже\n(Ошибка: {e})"
