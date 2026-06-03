import logging
import os

from dotenv import load_dotenv

_env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
load_dotenv(dotenv_path=_env_path, override=True)

logger = logging.getLogger(__name__)

FALLBACK_REMARKS = "Health prediction could not be generated. Please try again later."


def build_prompt(glucose, haemoglobin, cholesterol):
    return (
        f"You are a healthcare assistant. Based on the following blood test values: "
        f"Glucose: {glucose} Haemoglobin: {haemoglobin} Cholesterol: {cholesterol} "
        f"Provide: Possible health risk, Short explanation. Keep the response under 40 words."
    )


def get_health_prediction(glucose, haemoglobin, cholesterol):
    load_dotenv(dotenv_path=_env_path, override=True)
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()

    if not api_key:
        return FALLBACK_REMARKS

    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=build_prompt(glucose, haemoglobin, cholesterol),
        )
        return response.text.strip() or FALLBACK_REMARKS
    except Exception as e:
        logger.warning("Gemini API error: %s", e)
        return FALLBACK_REMARKS
