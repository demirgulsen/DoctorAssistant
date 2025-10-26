"""
Symptom summary action handlers
"""
from typing import List

def format_symptom_list(symptoms: List[str]) -> str:
    """ Formats symptoms into a numbered list.
    Parameter:
        symptoms: List of symptoms
    Returns:
        str: Formatted symptom list
    """
    return "\n".join([f"{idx}. **{symptom}**" for idx, symptom in enumerate(symptoms, 1)])


def create_summary_content(symptoms: List[str], texts: dict) -> str:
    """ Creates formatted summary content.
    Parameter:
        symptoms: List of symptoms
        texts: Localized text messages
    Returns:
        str: Formatted summary content
    """
    if not symptoms:
        return f"## {texts['title']}\n\n_{texts['none']}_"

    symptoms_list = format_symptom_list(symptoms)
    return f"""## {texts['title']}        
{symptoms_list}
---
**{texts['total']}:** {len(symptoms)} symptom(s)"""
