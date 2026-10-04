# Sidequest Project 2 Prompt Log

## AI Tools Used

I primarily used ChatGPT during this project for brainstorming, planning the frontend/backend architecture, generating starter code, debugging Flask/Render/GitHub Pages/CORS/API problems, modifying filters and backend behavior, reviewing implementation choices, and organizing documentation.

I used GitHub's web interface and local terminal tools to actually edit, commit, deploy, and test the project.

Google Places was the external data source, Render hosted the Flask backend, and GitHub Pages hosted the frontend.

## Which Tool I Used for Which Job

I used ChatGPT most heavily for coding and debugging because it was useful for quickly generating possible fixes and explaining where a problem might be.

I used browser developer tools, curl, terminal output, GitHub Actions logs, and Render deployment logs to verify whether those suggestions actually worked.

For deployment problems, I relied more heavily on actual logs than on AI explanations because errors involving ports, CORS, hosting configuration, and API responses needed to be checked against the running application.

For product decisions, I used AI mostly as a brainstorming partner. I personally chose the Sidequest concept, cities, 125-mile range, 80-place result target, filters, swipe behavior, and the Free/$/$$/$$$/$$$$ multi-select price interface.

## Development Process

### 1. Starting from the Sidequest concept

Sidequest began as an earlier project based around recommending things to do.

For Project 2, I wanted to make the idea substantially more interactive rather than only making a slightly improved randomizer.

The new concept became essentially "Tinder/Hinge for things to do."

### 2. Frontend and backend architecture

The project was split into a plain HTML/CSS/JavaScript frontend and a Flask backend.

The frontend was deployed to GitHub Pages.

The Flask backend was deployed to Render.

The backend was responsible for third-party API communication so the Google API key would not be exposed in frontend JavaScript.

### 3. Deployment debugging

One of the more time-consuming parts of the project was making the deployed frontend and backend actually communicate correctly.

Port 8000 conflicted with another local tool.

Port 5000 on my Mac was being used by an AirTunes/AirPlay-related service, so I moved the Flask development server to port 5055.

I also had to configure CORS correctly so the GitHub Pages origin could call the Render backend.

At one point the frontend configuration URL was malformed, which caused the deployed frontend to report that the backend was offline even though the backend `/health` route worked.

I fixed the frontend configuration, redeployed GitHub Pages, redeployed Render, and verified the connection.

### 4. Google Places integration

The backend was changed to use Google Places for real location data, ratings, addresses, coordinates, categories, price levels, photos, and accessibility information.

The API key is stored only on the backend through an environment variable.

### 5. Expanding the result pool

The first working version only showed three demo Sidequests.

Once the deployment pipeline was working, I expanded the backend so the application could retrieve a much larger result pool.

The target was eventually changed to a maximum of 80 places.

The backend now performs multiple relevant searches, collects results, removes duplicate Place IDs, normalizes the data, applies Sidequest filters, and ranks the remaining results.

### 6. Distance changes

The initial maximum distance was too small for the type of app I wanted.

I changed the maximum distance to 125 miles and changed the backend so the actual Haversine distance calculation enforces the selected distance.

### 7. Budget filter redesign

The earlier budget filter behaved like a simple maximum.

I changed the interface to a multi-select dropdown with:
- Free
- $
- $$
- $$$
- $$$$

This required changes to the HTML, CSS, frontend JavaScript, query parameters, and backend filtering.

### 8. Persistence

For the MVP, I deliberately did not add accounts or a database.

Saved, completed, and history information are stored using localStorage.

### 9. Current MVP

The deployed MVP has:
- public frontend
- public backend
- frontend/backend communication
- Google Places integration
- secret API-key handling
- city/category/time/distance/budget/party-size filters
- distance filtering up to 125 miles
- multi-select price filtering
- place cards with multiple photos
- swipe controls
- saved places
- completed places
- history
- custom metrics
- quest objectives
- localStorage persistence

## Meaningful Changes I Made Myself

Examples include:
- changing the desired maximum distance to 125 miles
- changing the maximum result pool from 100 to 80
- choosing the exact budget categories and changing the interaction to a multi-select dropdown
- choosing Google Places as the data source
- deciding which cities the interface should support
- editing and committing files directly through GitHub
- configuring and redeploying the Render backend
- configuring GitHub Pages deployment
- testing `/health` and `/places`
- verifying frontend/backend connectivity
- keeping localStorage instead of adding accounts or a database
- prioritizing a working MVP over adding more large features before the deadline

## One Place AI Got It Wrong

One useful example happened while implementing the new price filter.

AI originally suggested passing all five price categories, including `PRICE_LEVEL_FREE`, directly through the Google Places `priceLevels` request field.

That suggestion was wrong for the API behavior I needed.

The implementation was corrected so Sidequest retrieves places and applies the selected price categories locally instead.

A related issue happened when increasing the result target. An early approach treated pagination as if one search could simply provide enough results for an 80-place pool. The final implementation instead combines multiple relevant searches and deduplicates the resulting Google Place IDs.

These were good examples of why I still needed to understand, test, and modify AI-generated code rather than assuming a confident answer was correct.

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

# Testing and Debugging Notes

Testing was done both locally and against deployed services.

Examples included:
- testing Flask `/health`
- testing `/places`
- checking whether the Google Places key was detected
- testing GitHub Pages
- checking Render deployment logs
- testing frontend/backend CORS
- testing card loading
- checking whether saved/completed state persisted
- changing local ports when existing services caused conflicts
- verifying that deployment changes actually reached the public versions

The most important lesson from this part of the project was that deployment problems often required looking at actual request/response behavior rather than only changing code.

# Remaining Work

At the time this prompt log was drafted, the MVP was functioning.

Remaining work was mostly:
- testing edge cases
- testing mobile/small-screen layout
- improving loading/error states
- polishing UI details
- finishing documentation
- linking the project from the portfolio
- recording the demo video
- submitting the required Google form

I deliberately chose not to add a database, account system, or recommendation ML model before finishing the required project because those features were not necessary for the core Sidequest experience.
