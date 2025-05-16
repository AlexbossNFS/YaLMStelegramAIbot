from openai import OpenAI

client = OpenAI(
    api_key="sk-U5euLew39N91fkHew4N02kPkQWd6207a54i9Cj828F7a7U2m",  # Вставьте ваш ключ
    base_url="https://api.chatgpt.com"
)

response = client.chat.completions.create(
    model="deepseek-chat",  # Модель для чата
    messages=[{"role": "user", "content": "Привет! Какие у тебя лимиты API?"}],
    stream=False
)

print(response.choices[0].message.content)