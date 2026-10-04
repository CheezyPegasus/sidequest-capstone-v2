# Sidequest

Sidequest is a swipe-based web app for discovering things to do when you do not already have a destination in mind. The basic idea is similar to a dating-app card deck, except the cards are places and activities instead of people.

Users choose a city and preferences such as category, available time, maximum distance, budget, and group size. Sidequest then builds a live deck of places that users can swipe through, save, or mark as completed.

## Live App

Frontend:  
https://cheezypegasus.github.io/sidequest-capstone-v2/

Backend:  
https://sidequest-capstone-v2.onrender.com/

Repository:  
https://github.com/CheezyPegasus/sidequest-capstone-v2

## What Sidequest Does

Sidequest lets users discover places through a set of practical filters:

- city
- category
- available time
- maximum distance
- budget
- party size

The current app supports a maximum trip radius of 125 miles.

The budget control is a multi-select menu with:

- Free
- $
- $$
- $$$
- $$$$

A broad search can return up to 200 live Sidequests.

## Main Features

### Swipe-based discovery

Places appear as cards that users can move through with swipe-style controls.

The interface is designed to make choosing an activity feel less like searching a directory and more like discovering options one at a time.

### Live place discovery with Geoapify

The Flask backend uses the Geoapify Places API to retrieve real points of interest around the selected city.

The backend converts Geoapify results into the data format used by the Sidequest frontend.

### 2-3 preview images per Sidequest

The app loads preview images lazily for the current card using Wikimedia Commons / MediaWiki.

The backend first searches geographically using the Sidequest coordinates and then falls back to a place-name search when needed.

Images are not fetched for all 200 places at startup. They are loaded only when a card is actually viewed, which keeps the initial deck request much lighter.

### Saved, Completed, and History

Users can save interesting Sidequests and mark them as completed.

The MVP stores saved, completed, and history state with browser `localStorage`, so it does not require accounts or a database.

### Sidequest metrics

The backend calculates or estimates Sidequest-specific values such as:

- distance fit
- popularity
- nicheness
- accessibility
- adventure level
- group fit
- estimated visit time

### Quest objectives

Each destination receives a small set of objectives based on its type.

These are intended to make the app feel more like a real-world quest system rather than a normal places directory.

## Features I Am Most Proud Of

One feature I am especially proud of is the frontend/backend separation.

The frontend is deployed on GitHub Pages while the Flask API is deployed independently on Render. The frontend sends requests to the backend, and the backend handles external API communication and transforms the returned data into Sidequest cards.

I am also proud of the final result-pool size. The earliest deployed version only showed three demo Sidequests, while the final version can load up to 200 real locations in a broad search.

Another feature I am proud of is the image pipeline. Geoapify solved the place-discovery problem but did not provide the same photo resources I originally expected from Google Places. Instead of rebuilding the frontend, I added a second lightweight endpoint that retrieves up to three Wikimedia Commons preview images for the current place.

## Architecture

### Frontend

Technologies:

- HTML
- CSS
- JavaScript
- GitHub Pages

The frontend handles:

- filters
- swipe cards
- image display
- saved Sidequests
- completed Sidequests
- history
- localStorage persistence
- frontend error states

### Backend

Technologies:

- Python
- Flask
- `requests`
- `flask-cors`
- Gunicorn
- Render

The backend handles:

- Geoapify Places requests
- category translation
- distance calculation
- data normalization
- Sidequest metrics
- quest objectives
- Wikimedia Commons image lookup
- API-key security
- JSON error responses

### Data flow

Main place discovery:

```text
Browser
  -> GitHub Pages frontend
  -> Flask backend on Render
  -> Geoapify Places API
```

Image loading:

```text
Current Sidequest card
  -> Flask /place-images endpoint
  -> Wikimedia Commons / MediaWiki API
  -> 2-3 image URLs
  -> existing frontend photo viewer
```

## Main Backend Endpoints

### `/health`

Returns backend status and whether the external API key is configured.

### `/places`

Accepts the current Sidequest filters and returns a normalized list of places.

Important request parameters include:

- `city`
- `category`
- `max_minutes`
- `max_distance`
- `prices`
- `party`
- `limit`

### `/place-images`

Accepts information about the current place, including coordinates, and returns up to three Wikimedia Commons image URLs when available.

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
export GOOGLE_PLACES_API_KEY="YOUR_GEOAPIFY_KEY_HERE"
PORT=5055 python app.py
```

Then open:

```text
http://127.0.0.1:5055/health
```

Note: the current deployment still reads the Geoapify key from the environment-variable name `GOOGLE_PLACES_API_KEY` because that name was retained during the provider migration. The value itself is a Geoapify API key.

### Frontend

From the repository root:

```bash
python3 -m http.server 8080 --bind 127.0.0.1 --directory frontend
```

Then open:

```text
http://127.0.0.1:8080
```

For local development, `frontend/config.js` must point to the local Flask backend rather than the deployed Render URL.

## Secrets and API Keys

The live Geoapify key is not stored in frontend JavaScript.

The deployed backend reads the key from a Render environment variable.

The repository should not contain the real API key.

The frontend communicates only with the Flask backend.

## Error Handling

The backend returns JSON error responses for external API failures.

During development I also added more explicit error output so backend exceptions could be diagnosed without the frontend failing on an HTML 500 page.

The frontend has visible failure states for cases where places cannot be loaded or the backend cannot be reached.

## What Changed From My Earlier Sidequest Work

This project builds on an earlier Sidequest idea, but Project 2 changes the interaction and technical architecture substantially.

Major changes include:

- swipe-based interaction instead of a simple randomizer
- saved/completed/history state
- deployed Flask backend
- live Geoapify integration
- up to 200 live Sidequests
- expanded city support
- distance filtering up to 125 miles
- multi-select price controls
- Sidequest-specific scoring
- dynamically generated quest objectives
- lazy Wikimedia image loading
- frontend/backend deployment and CORS handling

## AI Usage

I used ChatGPT during development for brainstorming, starter code, debugging, reviewing changes, and documentation support.

I did not treat generated code as automatically correct. I tested locally and in deployment, inspected actual API and Render errors, changed requirements and design decisions myself, and corrected suggestions that did not match the real APIs.

Examples of decisions and modifications I made include:

- changing the project into a swipe-based discovery app
- choosing the supported cities and filters
- changing the trip radius to 125 miles
- increasing the live result goal to 200
- replacing the original budget control with a multi-select interface
- switching from Google Places to Geoapify
- keeping the frontend response structure stable during the provider migration
- using localStorage instead of adding user accounts
- adding lazy Wikimedia image loading instead of requesting images for all 200 cards at startup

A detailed record of the AI workflow, debugging process, important prompts, and examples where AI suggestions were incorrect is included separately in `prompt_log.md`.

## AI-Generated Documentation Note

An AI-generated draft was used as a starting point for portions of this README. I reviewed and edited the project implementation and documentation to reflect the actual deployed system, my own product decisions, and the debugging work I completed.
