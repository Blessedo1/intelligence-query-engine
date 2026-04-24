from typing import Dict, Optional

def parse_natural_query(q: str) -> Dict:
    if not q or not isinstance(q, str):
        return {"status": "error", "message": "Unable to interpret query"}
    
    text = q.lower().strip()
    filters = {}

    # Gender
    if "male" in text and "female" not in text:
        filters["gender"] = "male"
    elif "female" in text and "male" not in text:
        filters["gender"] = "female"

    # Age Group
    if "adult" in text:
        filters["age_group"] = "adult"
    elif "teenager" in text or "teen" in text:
        filters["age_group"] = "teenager"
    elif "child" in text:
        filters["age_group"] = "child"
    elif any(word in text for word in ["senior", "elderly", "old"]):
        filters["age_group"] = "senior"

    # Age keywords
    if "young" in text:
        filters["min_age"] = 16
        filters["max_age"] = 24
    if any(word in text for word in ["older than", "above", "over"]):
        for word in text.split():
            if word.isdigit():
                filters["min_age"] = int(word)
                break
    if any(word in text for word in ["below", "under", "younger than"]):
        for word in text.split():
            if word.isdigit():
                filters["max_age"] = int(word)
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
            filters["country_id"] = code
            break

    return filters
