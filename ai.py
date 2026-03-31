# ai.py — Gemini API

import httpx
from config import GEMINI_API_KEY

API_URL = f”https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}”

async def ask_gemini(prompt: str) -> str:
payload = {
“contents”: [{“parts”: [{“text”: prompt}]}]
}
async with httpx.AsyncClient(timeout=30) as client:
response = await client.post(API_URL, json=payload)
data = response.json()
return data[“candidates”][0][“content”][“parts”][0][“text”]

async def get_horoscope(sign: str, birthdate: str) -> str:
prompt = f””“Ти — містичний астролог. Склади персональний гороскоп українською мовою.
Знак зодіаку: {sign}
Дата народження: {birthdate}

Гороскоп має містити:

- Загальна енергія дня (2-3 речення)
- Кохання та стосунки (2-3 речення)
- Робота та фінанси (2-3 речення)
- Порада дня (1 речення)
- Щасливе число та колір

Пиши містично, тепло та надихаюче. Використовуй емодзі.”””
return await ask_gemini(prompt)

async def get_tarot(question: str) -> str:
prompt = f””“Ти — досвідчений таролог. Зроби розклад Таро українською мовою.
Питання або сфера: {question}

Витягни 3 карти (минуле, теперішнє, майбутнє). Для кожної карти:

- Назва карти
- Що вона означає в цій позиції (2-3 речення)

В кінці — загальний висновок розкладу (3-4 речення).
Пиши містично та натхненно. Використовуй емодзі.”””
return await ask_gemini(prompt)

async def get_moon_stone(sign: str) -> str:
prompt = f””“Ти — кристалотерапевт та астролог. Розкажи про лунний камінь для знаку зодіаку українською мовою.
Знак зодіаку: {sign}

Розкажи:

- Який камінь є головним лунним каменем цього знаку і чому
- Які енергії та властивості він несе (3-4 речення)
- Як носити або використовувати цей камінь
- Яку силу він дає саме цьому знаку
- Додатково: 1-2 камені підсилювачі

Пиши захоплено, містично та детально. Використовуй емодзі 💎✨🌙”””
return await ask_gemini(prompt)

async def get_compatibility(sign1: str, sign2: str) -> str:
prompt = f””“Ти — астролог-психолог. Зроби аналіз сумісності двох знаків зодіаку українською мовою.
Перший знак: {sign1}
Другий знак: {sign2}

Аналіз має включати:

- Загальний відсоток сумісності (число від 0 до 100%)
- Сильні сторони цього союзу (3-4 пункти)
- Можливі труднощі (2-3 пункти)
- Порада для гармонії у стосунках
- Сумісність у коханні, дружбі та роботі (окремо)

Пиши тепло, чесно та надихаюче. Використовуй емодзі 💑✨”””
return await ask_gemini(prompt)
