# Sidequest Project 2 Prompt Log

## AI Tools Used

I primarily used ChatGPT during this project for brainstorming, planning the frontend/backend architecture, generating and modifying starter code, debugging Flask/Render/GitHub Pages/CORS/API problems, reviewing implementation choices, and organizing documentation.

I used GitHub's web interface and local terminal tools to edit, commit, deploy, and test the project. I also relied on browser error messages, Render deployment logs, direct endpoint tests, and the deployed application itself to verify whether AI suggestions actually worked.

The final deployed project uses:
- GitHub Pages for the frontend
- Render for the Flask backend
- Geoapify Places API for live place discovery
- Wikimedia Commons / MediaWiki API for place preview images
- browser localStorage for saved, completed, and history state

## Which Tool I Used for Which Job

I used ChatGPT most heavily for:
- brainstorming the Sidequest product concept
- planning the frontend/backend boundary
- generating starter HTML/CSS/JavaScript/Python code
- debugging deployment, CORS, API, and data-shape problems
- suggesting concrete patches after I supplied error messages
- reviewing which changes were most important before the deadline
- helping organize the README and prompt log

I used browser developer tools, direct endpoint tests, terminal output, GitHub, and Render logs to verify the actual behavior of the system. This was especially important during deployment and API debugging because several AI suggestions were plausible but wrong for the real API.

For product decisions, I used AI as a brainstorming/debugging partner rather than allowing it to define the project. I personally chose the Sidequest concept, supported cities, the 125-mile range, the swipe-style interaction, the Free/$/$$/$$$/$$$$ multi-select price control, the result target, the decision to keep localStorage instead of adding accounts, and the final decision to prioritize a working MVP over additional large features.

## Development Process

### 1. Starting from the Sidequest concept

Sidequest began as an earlier project for recommending things to do.

For Project 2, I wanted a substantial change rather than a small extension of the earlier randomizer. The concept became essentially "Tinder/Hinge for things to do": the user chooses filters, receives a deck of possible places, swipes through them, saves interesting choices, and can later mark them complete.

### 2. Frontend and backend architecture

I split the application into:
- a plain HTML/CSS/JavaScript frontend
- a Flask backend

The frontend is deployed to GitHub Pages.

The Flask backend is deployed to Render.

The frontend sends filter choices to the backend through HTTP requests. The backend handles third-party API communication and converts external place data into the structure expected by the Sidequest cards.

This separation also keeps API credentials off the public frontend.

### 3. Deployment debugging

A large part of the project was making the deployed frontend and backend communicate correctly.

Port 8000 conflicted with another local tool.

Port 5000 on my Mac was being used by an AirTunes/AirPlay-related service, so I moved the local Flask development server to port 5055.

I configured CORS so the GitHub Pages frontend could call the Render backend.

At one point the frontend configuration URL was malformed, so the frontend reported that the backend was offline even though the backend `/health` route worked.

I fixed the frontend configuration, redeployed GitHub Pages and Render, and verified the public connection.

### 4. Initial Google Places implementation

The earlier backend implementation used Google Places.

The goal was to retrieve real locations, addresses, coordinates, ratings, place types, photos, and accessibility information.

The API key was kept on the backend as an environment variable rather than committed to GitHub.

However, I was not able to continue using a Google Places key for the final deployment, so this became a major late-stage architectural change.

### 5. Expanding the result pool

The first working deployment only returned three demo Sidequests.

I expanded the backend so the app could work with a much larger live result pool.

During development the target changed several times, including 50-60, 80, 100, and finally a maximum of 200 Sidequests.

The final Geoapify version can return a large set of real POIs and the backend normalizes those results into the format expected by the frontend.

The deployed app successfully reached 200 Sidequests in a broad Pittsburgh search.

### 6. Distance changes

The original maximum distance was too small for the type of app I wanted.

I changed the maximum distance to 125 miles.

The backend calculates actual Haversine distance from the selected city center and uses the result in Sidequest filtering/scoring.

### 7. Budget filter redesign

The earlier budget filter behaved like a simple maximum.

I changed it to a multi-select dropdown with:
- Free
- $
- $$
- $$$
- $$$$

This required changes across the HTML, CSS, frontend JavaScript, query parameters, and backend filtering logic.

### 8. Persistence

For the MVP, I deliberately did not add accounts or a database.

Saved, completed, and history information are stored in browser localStorage.

This kept the scope manageable while still giving the app persistent interactive state.

### 9. Switching the live place provider to Geoapify

Late in development, the live Google Places path was blocked by the lack of a usable Google Places key.

I obtained a Geoapify key and switched the backend provider.

This required replacing Google-specific Text Search requests with Geoapify's Places endpoint and translating Sidequest categories into Geoapify categories.

I intentionally kept the frontend response shape largely unchanged so I would not need to rebuild the UI.

Important debugging steps during this migration included:
- removing leftover Google-only request logic
- changing the provider reported by `/health`
- fixing duplicate category dictionaries
- removing stale variables such as `queries_used`
- replacing references to a deleted local `geo_categories` variable with the top-level `GEOAPIFY_CATEGORIES`
- using real API error text instead of guessing why requests failed

The migration was successful and the final deployed backend returned 200 Sidequests.

### 10. Fixing API/category mistakes

One Geoapify request failed with:

`Invalid parameters. Category "commercial.cafe" is not supported.`

The error came from a stale duplicate category dictionary in `/places`.

I removed that duplicate block and used the single top-level `GEOAPIFY_CATEGORIES` dictionary.

A later backend crash returned HTML instead of JSON, which caused the frontend error:

`Unexpected token '<', "<!doctype "... is not valid JSON`

To diagnose that, I temporarily added an exception handler that returned the Python exception as JSON. This exposed:

`NameError: name 'geo_categories' is not defined`

I then replaced the stale reference with `GEOAPIFY_CATEGORIES`.

After redeployment, the app successfully loaded the full live deck.

### 11. Adding preview images

Geoapify solved the live place-discovery problem, but it did not provide the same Google Places photo resources that the frontend had originally expected.

Instead of making `/places` load images for all 200 cards at once, I added a separate lazy image path.

The backend now exposes a place-image endpoint using Wikimedia Commons / MediaWiki.

The frontend requests images only for the currently displayed Sidequest.

The first image approach searched Commons by place name, but it often returned no results.

I then changed the image lookup to use the Sidequest's latitude/longitude with Wikimedia geographic search first, followed by a place-name search as a fallback.

The frontend attaches up to 2-3 returned image URLs to the current card and re-renders the existing photo preview area.

This worked in the deployed application and avoided making hundreds of image requests during the initial 200-place deck load.

### 12. Current MVP

The deployed MVP currently has:
- public GitHub Pages frontend
- public Render Flask backend
- frontend/backend communication
- Geoapify live place discovery
- up to 200 Sidequests in a broad search
- city/category/time/distance/budget/party-size filters
- distance filtering up to 125 miles
- multi-select price controls
- swipe-style discovery
- saved places
- completed places
- history
- localStorage persistence
- Sidequest-specific metrics and quest objectives
- lazy-loaded 2-3 image previews through Wikimedia Commons
- error handling for backend/API failures

## Meaningful Changes I Made Myself

Examples of product and implementation decisions I made or substantially changed include:
- changing the project from a randomizer into a swipe-style discovery app
- choosing the supported cities
- changing the maximum trip distance to 125 miles
- increasing the result target until the final 200-place goal
- choosing the Free/$/$$/$$$/$$$$ budget categories
- redesigning the budget interaction as a multi-select dropdown
- deciding to keep saved/completed/history state in localStorage
- configuring and redeploying the Render backend
- configuring GitHub Pages deployment
- testing `/health`, `/places`, and the image endpoint
- verifying frontend/backend connectivity
- switching the live provider from Google Places to Geoapify when Google was no longer practical
- choosing to preserve the frontend data shape during that migration
- using real request/response errors to find broken variables and duplicate category definitions
- adding lazy image loading instead of fetching images for all 200 results at startup
- prioritizing a stable MVP over adding accounts, a database, or an ML recommendation model before the deadline

## One Place AI Got It Wrong

There were several useful examples.

One early suggestion tried to use Google Places price categories in a way that did not match the actual API behavior. I had to change the implementation and perform price handling locally instead.

A more important late-stage example happened during the Geoapify migration. AI suggested `commercial.cafe` as a valid Geoapify category. The deployed API explicitly rejected it with a 400 error: `Category "commercial.cafe" is not supported.` I used the actual API error to correct the implementation and remove a stale duplicate category dictionary.

AI also initially assumed that changing the API key was enough to move from Google Places to Geoapify. In reality, the API key and the API provider are not interchangeable: the backend still had Google-specific URLs, request fields, pagination logic, and variables. I had to replace the provider-specific code and then remove leftover Google-era variables one by one.

Another example was the first Wikimedia image approach. Searching only by exact place name often returned no images. The working version instead uses geographic image search based on each Sidequest's coordinates and then falls back to name search.

These were good reminders that AI-generated code still needed to be tested against real APIs and real deployed behavior.

# Important Prompts

Below are important prompts copied verbatim from my development conversation.

## Prompt 1
> YES, now everything works, but only 3 sidequests loaded; we need 50-60 more soon without breaking anything

## Prompt 2
> change destination max to 125 miles as well, too close

## Prompt 3
> make a list of changes I can make to the github from the earlier 2 messages

## Prompt 4
> oh, one last thing, just make the toggle for free/paid to like a dropdown with checkmarks, you can choose "Free," "$" "$$" $$$" "$$$$"

## Prompt 5
> ok we are going to summarize and package it up into one commit ASAP, can you tell me where to change on github website?

## Prompt 6
> CSS now

## Prompt 7
> where do I add the CSS segment?

## Prompt 8
> fix this (change the 100 to 80)

## Prompt 9
> no fix everything you told me to, I fixed 3

## Prompt 10
> just fix it yourself and let me copy paste, I cannot ctrl f in github

## Prompt 11
> just deployed render, waiting for success

## Prompt 12
> now it's a MVP that works, what should I 1. say during OH today in terms of my progress? and 2. what should I do next according to the specs?

## Prompt 13
> can you pack a README and a Prompt log for me right now, and I can push them onto Git?

## Prompt 14
> done, now go check in case I screwed up anything

## Prompt 15
> 0 sidequests loaded. Demo mode is active — add GOOGLE_PLACES_API_KEY for live results.
> I think this might be the issue, nothing is really happening here

## Prompt 16
> I can't get a free GOOGLE_PLACES_API_KEY, can I use an nvidia free key instead?

## Prompt 17
> Could not reach the Sidequest backend.
>
> Could not load Sidequests.
> Google Places returned an error.
>
> Check the deployed backend or try again.

## Prompt 18
> where is the places I need to modify?

## Prompt 19
> bro, this need to be fixed before 3:30PM, else I will be cooked by 15-150 (not 113)

## Prompt 20
> Could not load Sidequests.
> Geoapify HTTP 400: {'statusCode': 400, 'error': 'Bad Request', 'message': 'Invalid parameters. Category "commercial.cafe" is not supported.'}
>
> Check the deployed backend or try again.
> still, after the fresh deploy

## Prompt 21
> Could not load Sidequests.
> Unexpected token '<', "<!doctype "... is not valid JSON
>
> Check the deployed backend or try again.
> even after

## Prompt 22
> **Could not load Sidequests.**
> NameError: name 'geo_categories' is not defined
> Check the deployed backend or try again.

## Prompt 23
> YES, it worked
> the next step and final step is to literally add images, 200 sidequests found, holy shit
> time to go to the TA work session/OH

## Prompt 24
> now I need to fix the image issue, pull 2-3 images per sidequest in the top as preview

## Prompt 25
> bad news: no photos yet

## Prompt 26
> YES, now it works omg
> what is left for me?
> also make an updated prompt_log.md and let me push it to Git via Desktop

# Testing and Debugging Notes

Testing was done both locally and against deployed services.

Examples included:
- testing Flask `/health`
- testing `/places`
- testing the image endpoint
- checking whether the backend API key was detected
- testing GitHub Pages
- checking Render deployment logs
- testing frontend/backend CORS
- testing card loading
- checking whether saved/completed state persisted
- changing local ports when existing services caused conflicts
- reading exact third-party API error responses
- changing the backend error path so a Python exception was returned as JSON instead of an HTML 500 page
- verifying that deployment changes actually reached the public versions
- verifying a broad Pittsburgh search could load 200 Sidequests
- verifying that 2-3 preview images could appear on a live Sidequest card

One of the most important lessons from the project was that deployment and third-party API problems required inspecting actual request/response behavior rather than continuing to modify code from guesses.

# Remaining Work at Final Polish Stage

At the time of this update, the core application was functioning.

Remaining work was primarily submission/polish:
- perform one final end-to-end test of the deployed app
- test a few categories/cities and a small-screen layout
- update the README so it reflects Geoapify, Wikimedia Commons, and the 200-place result target instead of the earlier Google/80-place implementation
- make sure no API key is committed to the repository
- link Sidequest from the deployed portfolio Projects section
- record the required short demo video using the deployed app
- explain the frontend/backend architecture and the changes I personally made
- test the video link in an incognito/private window
- submit the deployed URL, repository URL, and video link through the required Google form

I deliberately chose not to add accounts, a database, social features, or an ML recommendation model before submission because those features were not necessary for the core Sidequest experience.
