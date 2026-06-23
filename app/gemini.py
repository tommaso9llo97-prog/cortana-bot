import google.generativeai as genai
from app.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY.get_secret_value())

SYSTEM_INSTRUCTION = (
    "Il tuo nome è Cortana. Sei l'alleato di Tommy. "
    "Parlami con sarcasmo e lucidità, spingendomi all'azione."
)

async def get_gemini_response(user_id: int, user_text: str, redis=None) -> str:
    # Passiamo la stringa racchiusa in una lista pulita per evitare il TypeError dello 'type' object
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash"
        system_instruction=[SYSTEM_INSTRUCTION]
    )
    
    # Eseguiamo la chiamata in modo sicuro
    response = await model.generate_content_async(user_text)
    return response.text