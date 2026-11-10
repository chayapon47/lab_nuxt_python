# Nuxt 4 API Intern Training — 12 Labs

## Requirements
Node.js compatible with your Nuxt version; npm.

## Start
```bash
npm install
cp .env.example .env
npm run dev
```
Open http://localhost:3000

All 149 records are copied from the original Python training dataset.
`public/data/*.json` are intentionally public, fake training records.

## Lab map
1 GET JSON; 2 POST Student; 3 404 error; 4 GET provider; 5 CRUD; 6 Courses + enrollment counts;
7 Graph node/edge; 8 Meta Graph API (optional credentials); 9 Pagination;
10 OpenAI Responses; 11 Structured Output; 12 Course-to-AI.

Lab 5: to test PUT/DELETE use curl or browser developer tools:
```bash
curl -i http://localhost:3000/api/students/1001
curl -i -X DELETE http://localhost:3000/api/students/1001
```
Lab 9: change page=2 or page=3 to explore pagination.
Lab 8: requires META_ACCESS_TOKEN, META_PAGE_ID, META_API_VERSION.
Labs 10-12: require OPENAI_API_KEY and access to OPENAI_MODEL.
Never commit `.env`. AI endpoints have only a localhost guard, not production authentication;
do not deploy this demo publicly. For production implement authentication, per-user quotas,
rate limits, request logging without secrets, spending controls and error classification.
The student store is in memory and resets on restart. SQLite is supplied in the Python
training pack but Nuxt examples use JSON and Nitro server endpoints.
