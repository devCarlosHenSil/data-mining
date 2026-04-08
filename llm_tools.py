from openai import AsyncOpenAI

client = AsyncOpenAI()

async def ask_llm(question: str, context: str = ""):
    messages = [
        {"role": "system", "content": "Você é Mila-Bot. Responda em português brasileiro. Nunca invente dados. Trate null como 'dado não disponível'."},
        {"role": "user", "content": f"{context}\nPergunta: {question}"}
    ]
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    return response.choices[0].message