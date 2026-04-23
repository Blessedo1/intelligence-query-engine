from typing import Dict, Optional

def parse_natural_query(q: str) -> Dict:
    if not q or not isinstance(q, str):
        return {"status": "error", "message": "Unable to interpret query"}
    
    text = q.lower().strip()
    filters =
    # Gender
    if "male" in text and "female" not in text:
        filters = "male"
    elif "female" in text and "male" not in text:
        filters = "female"

    # Age Group
    if "adult" in text:
        filters = "adult"
    elif "teenager" in text or "teen" in text:
        filters = "teenager"
    elif "child" in text:
        filters = "child"
    elif any(word in text for word in ):
        filters = "senior"

    # Age keywords
    if "young" in text:
        filters = 16
        filters = 24
    if any(word in text for word in ):
        for word in text.split():
            if word.isdigit():
                filters = int(word)
                break
    if any(word in text for word in ["below", "under", "younger than"]):
        for word in text.split():
            if word.isdigit():
                filters = int(word)
                break

    # Country
    country_map = {
        "nigeria": "NG", "nigerian": "NG", "naija": "NG",
        "kenya": "KE", "kenyan": "KE",
        "angola": "AO", "angolan": "AO",
        "egypt": "EG", "ghana": "GH", "south africa": "ZA", "sa": "ZA",
        "benin": "BJ", "togo": "TG"
    }
    
    for keyword, code in country_map.items():
        if keyword in text:
            filters = code
            break

    return filters
