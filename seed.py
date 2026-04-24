import json
import gdown
from database import Profile, get_db

def download_and_seed():
    url = "https://drive.google.com/uc?export=download&id=1Up06dcS9OfUEnDj_u6OV_xTRntupFhPH"
    gdown.download(url, "seed_profiles.json", quiet=False, fuzzy=True)
    
    with open("seed_profiles.json", "r") as f:
        raw_data = json.load(f)
    
    profiles =[]
    if isinstance(raw_data, dict):
        for value in raw_data.values():
            if isinstance(value, list):
                profiles = value
                break
    else:
        profiles = raw_data

    db = next(get_db())
    added = 0
    
    for p in profiles:
        existing = db.query(Profile).filter(Profile.name == p.get("name", "").lower()).first()
        if existing:
            continue
            
        profile = Profile(
            name=p.get("name", "").lower(),
            gender=p.get("gender"),
            gender_probability=p.get("gender_probability"),
            age=p.get("age"),
            age_group=p.get("age_group"),
            country_id=p.get("country_id"),
            country_name=p.get("country_name"),
            country_probability=p.get("country_probability"),
        )
        db.add(profile)
        added += 1
    
    db.commit()
    print(f"✅ Seeded {added} profiles successfully")
    db.close()

if __name__ == "__main__":
    download_and_seed()
