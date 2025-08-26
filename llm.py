import ollama

def get_llm_response(prompt: str):
    """
    Sends a prompt to the Ollama tinyllama model and returns the response.
    """
    try:
        # The only change is on the next line
        response = ollama.chat(
            model='tinyllama', # Changed from 'mistral'
            messages=[{'role': 'user', 'content': prompt}]
        )
        return response['message']['content']
    except Exception as e:
        return f"Error communicating with Ollama: {e}"