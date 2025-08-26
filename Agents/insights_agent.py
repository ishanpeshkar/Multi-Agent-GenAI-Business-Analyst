from llm import get_llm_response

def generate_insights(summary: str):
    """
    Uses an LLM to generate business insights from a data summary.
    """
    prompt = (
        "You are a business analyst. Based on the following data summary and email reports, "
        "identify key trends, potential risks, and anomalies. Be concise and use bullet points.\n\n"
        f"Data:\n{summary}"
    )
    
    insights = get_llm_response(prompt)
    return f"## Business Insights\n{insights}"