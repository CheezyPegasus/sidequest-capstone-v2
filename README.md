# Sidequest

Sidequest is a web app for discovering things to do when you do not already have a specific destination in mind. The basic idea is similar to a swipe-based dating app, except the cards are places and activities instead of people.

Users choose a city and a few preferences, then Sidequest builds a deck of possible destinations. Users can swipe through the deck, save places that look interesting, and mark places as completed later.

## Live App

Frontend:
https://cheezypegasus.github.io/sidequest-capstone-v2/

Backend:
https://sidequest-capstone-v2.onrender.com/

## What Sidequest Does

Sidequest lets users filter possible activities based on city, activity category, available time, maximum distance, budget, and group size.

The distance filter supports trips up to 125 miles from the selected city.

The budget filter is a multi-select menu with:
- Free
- $
- $$
- $$$
- $$$$

Instead of returning only a few hard-coded locations, the deployed version uses Google Places to build a larger pool of real locations.

The backend can combine multiple searches, remove duplicate Google Place IDs, normalize the results into a consistent format, and return up to 80 places.

## Main Features

### Swipe-based discovery
Places appear as cards that users can move through like a swipe deck.

### Filters
The app supports filters for location, category, time, distance, budget, and party size.

### Saved, Completed, and History
Users can save interesting destinations and mark destinations as completed. The MVP uses browser localStorage for this information, so it does not require user accounts or a database.

### Google Places integration
The Flask backend communicates with the Google Places API and retrieves place names, addresses, coordinates, ratings, rating counts, price levels, place types, photos, and accessibility information.

The frontend never receives the Google API key.

### Place scoring
The backend calculates or estimates Sidequest-specific values including distance, popularity, nicheness, accessibility, adventure level, group fit, and estimated visit time.

### Quest objectives
Each destination receives a short list of objectives based on its type.

## Features I Am Most Proud Of

One feature I am especially proud of is the frontend/backend separation.

The frontend is deployed with GitHub Pages while the Flask API is deployed independently on Render. The frontend sends requests to the backend, and the backend handles Google Places requests and API-key security.

I am also proud of the way the app turns raw Google Places data into a more game-like discovery experience. The swipe deck, saved/completed state, custom metrics, and quest objectives are meant to make deciding what to do feel more playful.

Another improvement I made during development was expanding the discovery radius to 125 miles and increasing the possible result pool. The backend now combines multiple searches and deduplicates places instead of relying on one small result set.

## Architecture

### Frontend
- HTML
- CSS
- JavaScript
- GitHub Pages

The frontend handles filters, place cards, swiping, photo display, saved places, completed places, history, and localStorage.

### Backend
- Python
- Flask
- requests
- flask-cors
- Gunicorn
- Render

The backend handles Google Places API requests, filtering, distance calculation, price filtering, deduplication, ranking, Sidequest metrics, quest objectives, and photo requests.

Data flow:

Browser → GitHub Pages frontend → Flask API on Render → Google Places API

## Running Locally

Clone the repository:

```bash
git clone https://github.com/CheezyPegasus/sidequest-capstone-v2.git
cd sidequest-capstone-v2
```

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export GOOGLE_PLACES_API_KEY="YOUR_KEY_HERE"
PORT=5055 python app.py
```

Backend:
`http://127.0.0.1:5055`

Health endpoint:
`http://127.0.0.1:5055/health`

### Frontend

From the repository root:

```bash
python3 -m http.server 8080 --bind 127.0.0.1 --directory frontend
```

Then open:
`http://127.0.0.1:8080`

For local development, `frontend/config.js` needs to point to the local Flask backend instead of the deployed Render backend.

## Secrets and API Keys

The Google Places API key is never committed to GitHub.

Locally, the backend reads the key from the `GOOGLE_PLACES_API_KEY` environment variable.

On Render, the same value is stored using Render's environment-variable management.

The frontend only communicates with my backend and does not contain the Google API key.

The repository's `.gitignore` excludes environment files such as `.env`.

## Error Handling

The backend returns JSON error responses when Google Places cannot be reached or returns an error.

The frontend also has an error state for cases where the backend cannot be reached.

During development I tested the deployed frontend and deployed backend together instead of relying only on local testing.

## What Changed From My Earlier Sidequest Work

This project builds on an earlier Sidequest idea, but Project 2 substantially changes the application.

The new version includes:
- a swipe-based interaction model
- saved/completed/history state
- a deployed Flask backend
- live Google Places integration
- Google Places photos
- a larger dynamically generated result pool
- expanded city support
- distance filtering up to 125 miles
- multi-select price filters
- Sidequest-specific scoring
- dynamically generated quest objectives
- frontend/backend deployment and CORS handling

## AI Usage

I used ChatGPT during development for brainstorming, code generation, debugging, and reviewing changes.

I did not treat generated code as automatically correct. I tested the application locally and in deployment, inspected errors, changed requirements and design decisions myself, and corrected several suggestions that did not work with the actual APIs.

Examples of decisions and modifications I made include:
- changing the maximum trip distance to 125 miles
- changing the result target to 80
- replacing the original budget control with a multi-select Free/$/$$/$$$/$$$$ control
- deciding to use Google Places
- deciding which cities and filters the application should support
- deploying the frontend and backend separately
- testing and fixing the connection between GitHub Pages and Render

A detailed record of my AI workflow and important prompts is included separately in `prompt_log.md`.

## AI-Generated Documentation Note

An AI-generated draft was used as a starting point for portions of this README. I reviewed and edited the final README to reflect my own implementation, decisions, and understanding of the project.
