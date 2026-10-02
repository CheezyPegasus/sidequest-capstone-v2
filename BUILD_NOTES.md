# Sidequest v2 build notes

## Why v2 changes the API

The UI now expects 6–8 photos per place plus accessibility data. Google Places (New) fits that data model better than Yelp for this project:
- Text Search / Place Details can return up to 10 photo resources.
- Structured accessibility options can be requested.
- Ratings, rating counts, price level, type and coordinates are all available.
- The API key stays on the Flask backend.

## Features in this scaffold

- Pittsburgh-first city dropdown plus:
  - San Francisco
  - Palo Alto
  - San Jose
  - Santa Clara
  - Cupertino
  - Berkeley
  - New York City
  - Los Angeles
  - Boston
  - Seattle
  - Atlanta
- "Surprise me" + six categories
- Time-at-destination slider
- Distance slider
- Budget slider
- Party-size segmented control
- Google Places Text Search through Flask
- Up to 8 photos per card
- Photo carousel with arrows and dots
- Google Maps address link
- Ratings + review count + price + estimated visit time + distance
- Nicheness / distance / popularity / accessibility / adventure / group-fit scores
- Short deterministic intro
- Up to 5 quest objectives
- Swipe left/right
- Bookmark quest
- Mark quest complete
- Saved / Completed / History views
- localStorage persistence
- Helpful backend-offline error message

## Important scoring notes

Some Sidequest fields are *derived*, not provided directly by Google:

- Distance: calculated from the selected city's center.
- Time at destination: estimated from place type.
- Nicheness: inverse of popularity within the current returned deck.
- Popularity: relative to user rating counts in the current deck.
- Adventure: heuristic based on place type.
- Group fit: heuristic based on place type + selected party size.
- Accessibility: based only on known Google accessibility flags. If Google does not provide them, the UI says "Unknown."

These should be explained in the final README so the app does not imply that Google directly supplies every score.

## Local run

### Terminal 1 — backend

```bash
cd ~/Downloads/sidequest-capstone-v2/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Before you have a Google key, the backend returns demo cards.

Verify:

```text
http://127.0.0.1:5000/health
```

You should see JSON with `"ok": true`.

### Terminal 2 — frontend

```bash
cd ~/Downloads/sidequest-capstone-v2/frontend
python3 -m http.server 8000
```

Open:

```text
http://localhost:8000
```

## Google Places setup

Enable Places API (New) in a Google Cloud project and create an API key.
For local development:

```bash
export GOOGLE_PLACES_API_KEY="YOUR_KEY"
python app.py
```

For Render, set `GOOGLE_PLACES_API_KEY` as an environment secret.

Do not put the key in `config.js`, HTML, JavaScript, GitHub, or the final prompt log.

## Deployment later

Backend:
- Root directory: `backend`
- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app`
- Secret: `GOOGLE_PLACES_API_KEY`

Frontend:
- Replace the localhost backend URL in `frontend/config.js` with the Render backend URL.
- Deploy to GitHub Pages.

## Course note

Do not use this file as your final README. The assignment explicitly asks you to write the README yourself in your own words.
