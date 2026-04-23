# Intelligence Query Engine - Insighta Labs

A production-ready demographic intelligence API that allows advanced filtering, sorting, pagination, and natural language search over 2026+ enriched profiles.

## Live API
**https://intelligence-query-engine.vercel.app**

## Features Implemented

- Advanced filtering (`gender`, `age_group`, `country_id`, `min_age`, `max_age`, `min_gender_probability`, `min_country_probability`)
- Sorting (`sort_by` + `order`)
- Pagination (`page` & `limit`)
- Natural Language Query (`/api/profiles/search?q=young males from nigeria`)
- Proper error responses and validation
- CORS enabled
- UUID v7 IDs and UTC timestamps
- Idempotent database seeding (2026 records)

## API Endpoints

### 1. Advanced Query
```bash
GET /api/profiles?gender=male&country_id=NG&min_age=25&sort_by=age&order=desc&page=1&limit=15

### 2. Natural Language Search (Core Feature)
GET /api/profiles/search?q=young males from nigeria
GET /api/profiles/search?q=females above 30
GET /api/profiles/search?q=adult males from kenya


