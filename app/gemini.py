from google import genai
from google.genai import types
from app.config import settings

# Inizializzazione con il nuovo SDK ufficiale di Google
client = genai.Client(api_key=settings.GEMINI_API_KEY.get_secret_value())

SYSTEM_INSTRUCTION = (
    "Il tuo nome è Cortana. Sei l'alleato di Tommy. "
    "Parlami con sarcasmo e lucidità, spingendomi all'azione."
)

async def get_gemini_response(user_id: int, user_text: str, redis=None) -> str:
    # Utilizziamo il client moderno con la configurazione corretta per gemini-2.0-flash
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=user_text,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION
        )
    )
    return response.text