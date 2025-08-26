from llm import get_llm_response

def generate_recommendations(insights: str):
    """
    Uses an LLM to generate strategic recommendations based on insights.
    """
    prompt = (
        "You are a business strategist. Based on the following insights, "
        "propose three actionable strategic recommendations to improve the business. "
        "Format your response as a numbered list.\n\n"
        f"Insights:\n{insights}"
    )
    
    recommendations = get_llm_response(prompt)
    return f"## Strategic Recommendations\n{recommendations}"