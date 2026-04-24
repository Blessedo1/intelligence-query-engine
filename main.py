import os
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from typing import Optional
from database import get_db, Profile
from query_parser import parse_natural_query

app = FastAPI(title="Intelligence Query Engine - Insighta Labs")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"status": "error", "message": "Invalid query parameters"}
    )

ALLOWED_ORIGINS = [origin.strip() for origin in os.getenv("ALLOWED_ORIGINS", "*").split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=ALLOWED_ORIGINS != ["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/profiles")
def get_profiles(
    gender: Optional[str] = Query(None),
    age_group: Optional[str] = Query(None),
    country_id: Optional[str] = Query(None),
    min_age: Optional[int] = Query(None),
    max_age: Optional[int] = Query(None),
    min_gender_probability: Optional[float] = Query(None),
    min_country_probability: Optional[float] = Query(None),
    sort_by: str = Query("created_at", enum=["age", "gender_probability", "created_at"]),
    order: str = Query("desc", enum=["asc", "desc"]),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    query = db.query(Profile)
    if min_age is not None and max_age is not None and min_age > max_age:
        raise HTTPException(status_code=400, detail={"status": "error", "message": "min_age cannot be greater than max_age"})

    # === Advanced Filtering ===
    if gender:
        query = query.filter(Profile.gender == gender.lower())
    if age_group:
        query = query.filter(Profile.age_group == age_group.lower())
    if country_id:
        query = query.filter(Profile.country_id == country_id.upper())
    if min_age is not None:
        query = query.filter(Profile.age >= min_age)
    if max_age is not None:
        query = query.filter(Profile.age <= max_age)
    if min_gender_probability is not None:
        query = query.filter(Profile.gender_probability >= min_gender_probability)
    if min_country_probability is not None:
        query = query.filter(Profile.country_probability >= min_country_probability)

    total = query.count()

    # === Sorting ===
    if sort_by == "age":
        sort_col = Profile.age
    elif sort_by == "gender_probability":
        sort_col = Profile.gender_probability
    else:
        sort_col = Profile.created_at

    if order == "desc":
        query = query.order_by(desc(sort_col))
    else:
        query = query.order_by(asc(sort_col))

    # === Pagination ===
    offset = (page - 1) * limit
    results = query.offset(offset).limit(limit).all()

    return {
        "status": "success",
        "page": page,
        "limit": limit,
        "total": total,
        "data": results
    }


@app.get("/api/profiles/search")
def search_profiles(
    q: str = Query(..., description="Natural language query"),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    parsed = parse_natural_query(q)
    
    if isinstance(parsed, dict) and parsed.get("status") == "error":
        raise HTTPException(status_code=400, detail="Invalid query parameters")

    query = db.query(Profile)

    if parsed.get("gender"):
        query = query.filter(Profile.gender == parsed["gender"])
    if parsed.get("age_group"):
        query = query.filter(Profile.age_group == parsed["age_group"])
    if parsed.get("country_id"):
        query = query.filter(Profile.country_id == parsed["country_id"])
    if parsed.get("min_age") is not None:
        query = query.filter(Profile.age >= parsed["min_age"])
    if parsed.get("max_age") is not None:
        query = query.filter(Profile.age <= parsed["max_age"])
    if parsed.get("min_age") is not None and parsed.get("max_age") is not None and parsed["min_age"] > parsed["max_age"]:
        raise HTTPException(status_code=400, detail={"status": "error", "message": "Invalid age range in query"})

    total = query.count()
    offset = (page - 1) * limit
    results = query.offset(offset).limit(limit).all()

    return {
        "status": "success",
        "page": page,
        "limit": limit,
        "total": total,
        "data": results
    }


@app.get("/")
async def root():
    return {
        "status": "success",
        "message": "Intelligence Query Engine is running",
        "endpoints": {
            "advanced_query": "/api/profiles",
            "natural_language": "/api/profiles/search"
        }
    }
