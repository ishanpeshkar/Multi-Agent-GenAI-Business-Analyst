from llm import get_llm_response

def generate_recommendations(insights: str):
    """
    Uses an LLM to generate strategic recommendations based on insights.
    For EACH key insight, proposes a primary recommendation and provides a brief
    scenario analysis with Best-Case, Most-Likely, and Worst-Case scenarios.
    """
    prompt = (
        "You are a senior business strategist. Based on the following insights, create a strategy document. "
        "For EACH key insight, propose a primary recommendation. Then, for that recommendation, provide a brief "
        "scenario analysis:\n"
        "- **Best-Case Scenario:** What is the most optimistic outcome?\n"
        "- **Most-Likely Scenario:** What is the probable outcome?\n"
        "- **Worst-Case Scenario:** What are the potential risks or downsides?\n\n"
        f"Insights to analyze:\n{insights}"
    )
    
    recommendations = get_llm_response(prompt)
    return f"## Strategic Recommendations & Scenario Planning\n{recommendations}"