import random

def generate_random_id(length=6):
    """Generate a random alphanumeric ID of given length."""
    characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(random.choice(characters) for _ in range(length))

async def get_response_from_gemini(prompt: str) -> str:
    """Simulate getting a response from the Gemini AI model."""
    # Placeholder for actual Gemini API call
    return f"Gemini response to: {prompt}"

def format_code_snippet(code: str, language: str = "python") -> str:
    """Format a code snippet for display."""
    return f"```{language}\n{code}\n```"