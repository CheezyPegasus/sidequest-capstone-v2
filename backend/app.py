import math
import os
import random
from urllib.parse import quote_plus

import requests
from flask import Flask, jsonify, redirect, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


API_KEY = os.environ.get("GOOGLE_PLACES_API_KEY", "").strip()

GEOAPIFY_PLACES_URL = "https://api.geoapify.com/v2/places"

GEOAPIFY_CATEGORIES = {
    "food": (
        "catering.restaurant,"
        "catering.fast_food,"
        "catering.food_court"
    ),

    "coffee": (
        "catering.cafe"
    ),

    "outdoors": (
        "leisure.park,"
        "tourism"
    ),

    "culture": (
        "entertainment.museum,"
        "entertainment.culture"
    ),

    "nightlife": (
        "catering.bar,"
        "catering.pub,"
        "adult.nightclub"
    ),

    "activities": (
        "entertainment"
    ),

    "surprise": (
        "entertainment,"
        "catering,"
        "leisure.park,"
        "tourism"
    ),
}

CITY_CONFIG = {
    "pittsburgh": {
        "label": "Pittsburgh",
        "query": "Pittsburgh, PA",
        "lat": 40.4406,
        "lng": -79.9959,
    },
    "san_francisco": {
        "label": "San Francisco",
        "query": "San Francisco, CA",
        "lat": 37.7749,
        "lng": -122.4194,
    },
    "palo_alto": {
        "label": "Palo Alto",
        "query": "Palo Alto, CA",
        "lat": 37.4419,
        "lng": -122.1430,
    },
    "san_jose": {
        "label": "San Jose",
        "query": "San Jose, CA",
        "lat": 37.3382,
        "lng": -121.8863,
    },
    "santa_clara": {
        "label": "Santa Clara",
        "query": "Santa Clara, CA",
        "lat": 37.3541,
        "lng": -121.9552,
    },
    "cupertino": {
        "label": "Cupertino",
        "query": "Cupertino, CA",
        "lat": 37.3230,
        "lng": -122.0322,
    },
    "berkeley": {
        "label": "Berkeley",
        "query": "Berkeley, CA",
        "lat": 37.8715,
        "lng": -122.2730,
    },
    "new_york": {
        "label": "New York City",
        "query": "New York, NY",
        "lat": 40.7128,
        "lng": -74.0060,
    },
    "los_angeles": {
        "label": "Los Angeles",
        "query": "Los Angeles, CA",
        "lat": 34.0522,
        "lng": -118.2437,
    },
    "boston": {
        "label": "Boston",
        "query": "Boston, MA",
        "lat": 42.3601,
        "lng": -71.0589,
    },
    "seattle": {
        "label": "Seattle",
        "query": "Seattle, WA",
        "lat": 47.6062,
        "lng": -122.3321,
    },
    "atlanta": {
        "label": "Atlanta",
        "query": "Atlanta, GA",
        "lat": 33.7490,
        "lng": -84.3880,
    },
}


SEARCH_TERMS = {
    "food": [
        "restaurants",
        "local food",
        "dessert",
    ],
    "coffee": [
        "coffee shops",
        "cafes",
    ],
    "outdoors": [
        "parks",
        "scenic viewpoints",
        "hiking trails",
    ],
    "culture": [
        "museums",
        "art galleries",
        "historic attractions",
    ],
    "nightlife": [
        "nightlife",
        "live music",
        "arcades",
    ],
    "activities": [
        "fun activities",
        "entertainment",
        "unique attractions",
    ],
}


SURPRISE_TERMS = [
    "unique things to do",
    "hidden gems",
    "museums",
    "parks",
    "cafes",
    "fun activities",
    "local attractions",
]


TIME_BY_TYPE = {
    "cafe": 60,
    "coffee_shop": 60,
    "restaurant": 90,
    "bakery": 45,
    "bar": 120,
    "night_club": 150,
    "museum": 150,
    "art_gallery": 90,
    "park": 120,
    "hiking_area": 180,
    "tourist_attraction": 120,
    "amusement_park": 240,
    "zoo": 240,
    "aquarium": 180,
    "movie_theater": 180,
    "bowling_alley": 120,
    "shopping_mall": 120,
    "book_store": 60,
}


ADVENTURE_BY_TYPE = {
    "hiking_area": 5,
    "amusement_park": 5,
    "park": 4,
    "tourist_attraction": 4,
    "zoo": 4,
    "aquarium": 3,
    "night_club": 4,
    "bar": 3,
    "museum": 2,
    "art_gallery": 2,
    "cafe": 1,
    "coffee_shop": 1,
    "restaurant": 2,
    "book_store": 1,
}


DEMO_PHOTOS = [
    "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1400&q=80",
    "https://images.unsplash.com/photo-1444723121867-7a241cacace9?auto=format&fit=crop&w=1400&q=80",
    "https://images.unsplash.com/photo-1494526585095-c41746248156?auto=format&fit=crop&w=1400&q=80",
    "https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?auto=format&fit=crop&w=1400&q=80",
    "https://images.unsplash.com/photo-1496568816309-51d7c20e3b21?auto=format&fit=crop&w=1400&q=80",
    "https://images.unsplash.com/photo-1519501025264-65ba15a82390?auto=format&fit=crop&w=1400&q=80",
    "https://images.unsplash.com/photo-1518005020951-eccb494ad742?auto=format&fit=crop&w=1400&q=80",
    "https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?auto=format&fit=crop&w=1400&q=80",
]


DEMO_PLACES = [
    {
        "id": "demo-phipps",
        "name": "Phipps Conservatory and Botanical Gardens",
        "address": "1 Schenley Dr, Pittsburgh, PA",
        "lat": 40.4392,
        "lng": -79.9489,
        "rating": 4.8,
        "user_rating_count": 6200,
        "price_level": "PRICE_LEVEL_MODERATE",
        "primary_type": "tourist_attraction",
        "primary_type_label": "Botanical Garden",
    },
    {
        "id": "demo-randyland",
        "name": "Randyland",
        "address": "1501 Arch St, Pittsburgh, PA",
        "lat": 40.4570,
        "lng": -80.0104,
        "rating": 4.7,
        "user_rating_count": 2500,
        "price_level": "PRICE_LEVEL_FREE",
        "primary_type": "tourist_attraction",
        "primary_type_label": "Art Attraction",
    },
    {
        "id": "demo-mt-washington",
        "name": "Mount Washington Overlook",
        "address": "Grandview Ave, Pittsburgh, PA",
        "lat": 40.4390,
        "lng": -80.0185,
        "rating": 4.8,
        "user_rating_count": 4200,
        "price_level": "PRICE_LEVEL_FREE",
        "primary_type": "tourist_attraction",
        "primary_type_label": "Scenic View",
    },
]


def clamp(value, low, high):
    return max(low, min(high, value))


def haversine_miles(lat1, lng1, lat2, lng2):
    earth_radius_miles = 3958.8

    p1 = math.radians(lat1)
    p2 = math.radians(lat2)

    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(p1)
        * math.cos(p2)
        * math.sin(dlng / 2) ** 2
    )

    return (
        earth_radius_miles
        * 2
        * math.atan2(
            math.sqrt(a),
            math.sqrt(1 - a),
        )
    )


def estimate_time(primary_type):
    return TIME_BY_TYPE.get(primary_type, 120)


def time_label(minutes):
    if minutes <= 45:
        return "30–45 min"

    if minutes <= 60:
        return "45–60 min"

    if minutes <= 90:
        return "1–1.5 hr"

    if minutes <= 120:
        return "1–2 hr"

    if minutes <= 180:
        return "2–3 hr"

    return "3–4+ hr"


def price_score(price_level):
    mapping = {
        "PRICE_LEVEL_FREE": 0,
        "PRICE_LEVEL_INEXPENSIVE": 1,
        "PRICE_LEVEL_MODERATE": 2,
        "PRICE_LEVEL_EXPENSIVE": 3,
        "PRICE_LEVEL_VERY_EXPENSIVE": 4,
    }

    return mapping.get(price_level)


def price_label(price_level):
    labels = {
        "PRICE_LEVEL_FREE": "Free",
        "PRICE_LEVEL_INEXPENSIVE": "$",
        "PRICE_LEVEL_MODERATE": "$$",
        "PRICE_LEVEL_EXPENSIVE": "$$$",
        "PRICE_LEVEL_VERY_EXPENSIVE": "$$$$",
    }

    return labels.get(
        price_level,
        "Price unknown",
    )


def accessibility_score(options):
    if not options:
        return None

    keys = [
        "wheelchairAccessibleEntrance",
        "wheelchairAccessibleParking",
        "wheelchairAccessibleRestroom",
        "wheelchairAccessibleSeating",
    ]

    known = [
        options.get(key)
        for key in keys
        if key in options
    ]

    if not known:
        return None

    positives = sum(
        value is True
        for value in known
    )

    if not positives:
        return 1

    return clamp(
        round(5 * positives / len(known)),
        1,
        5,
    )


def group_fit(primary_type, party):
    solo_friendly = {
        "cafe",
        "coffee_shop",
        "museum",
        "art_gallery",
        "book_store",
        "park",
    }

    group_friendly = {
        "restaurant",
        "bar",
        "night_club",
        "bowling_alley",
        "amusement_park",
        "tourist_attraction",
        "park",
        "movie_theater",
        "zoo",
        "aquarium",
    }

    if party == "solo":
        return (
            5
            if primary_type in solo_friendly
            else 4
        )

    if party == "friends":
        return (
            5
            if primary_type in group_friendly
            else 4
        )

    return (
        5
        if primary_type in group_friendly
        else 3
    )


def quest_objectives(primary_type, name):
    if primary_type in {
        "restaurant",
        "cafe",
        "coffee_shop",
        "bakery",
    }:
        return [
            "Try the item that seems most specific to this place.",
            "Pick one thing you normally would not order.",
            "Take one photo worth remembering.",
            "Figure out what regulars seem to come here for.",
            "Decide whether you would bring a friend back.",
        ]

    if primary_type in {
        "museum",
        "art_gallery",
    }:
        return [
            "Find one exhibit you would genuinely recommend.",
            "Read one description all the way through.",
            "Find the strangest or most niche object in the collection.",
            "Take one photo where photography is allowed.",
            "Leave with one fact you did not know before.",
        ]

    if primary_type in {
        "park",
        "hiking_area",
    }:
        return [
            "Reach one viewpoint, landmark, or memorable stopping point.",
            "Explore at least one full section of the route or park.",
            "Notice one thing unique to the local landscape.",
            "Take one photo that captures the place well.",
            "Leave the space as clean as you found it.",
        ]

    if primary_type in {
        "bar",
        "night_club",
    }:
        return [
            "Check out the atmosphere before settling in.",
            "Find the most distinctive thing on the menu or event list.",
            "Talk to at least one person if the vibe feels right.",
            "Capture one memorable detail without disrupting anyone.",
            "Decide what kind of night this place is best for.",
        ]

    return [
        f"Explore enough of {name} to find its most memorable feature.",
        "Find one detail most visitors might miss.",
        "Take one photo worth keeping.",
        "Try one part of the experience you did not plan in advance.",
        "Give the quest a personal 1–5 rating when you leave.",
    ]


def normalize_place(
    place,
    city,
    max_distance,
    party,
):
    location = place.get("location") or {}

    lat = location.get("latitude")
    lng = location.get("longitude")

    if lat is None or lng is None:
        return None

    distance = haversine_miles(
        city["lat"],
        city["lng"],
        lat,
        lng,
    )

    # Respect the actual selected distance.
    if distance > max_distance:
        return None

    display_name = (
        place.get("displayName")
        or {}
    )

    type_display = (
        place.get("primaryTypeDisplayName")
        or {}
    )

    primary_type = (
        place.get("primaryType")
        or (
            place.get("types")
            or ["point_of_interest"]
        )[0]
    )

    estimated_minutes = estimate_time(
        primary_type
    )

    photos = place.get("photos") or []

    photo_names = [
        photo.get("name")
        for photo in photos
        if photo.get("name")
    ][:8]

    address = place.get(
        "formattedAddress",
        "",
    )

    maps_url = (
        "https://www.google.com/maps/search/?api=1&query="
        + quote_plus(
            f"{display_name.get('text', '')} {address}"
        )
    )

    return {
        "id": place.get("id"),
        "name": (
            display_name.get("text")
            or "Unnamed place"
        ),
        "address": address,
        "lat": lat,
        "lng": lng,
        "rating": place.get("rating"),
        "user_rating_count": place.get(
            "userRatingCount",
            0,
        ),
        "price_level": place.get(
            "priceLevel"
        ),
        "price_label": price_label(
            place.get("priceLevel")
        ),
        "primary_type": primary_type,
        "primary_type_label": (
            type_display.get("text")
            or primary_type
            .replace("_", " ")
            .title()
        ),
        "photo_names": photo_names,
        "distance_miles": distance,
        "estimated_minutes": (
            estimated_minutes
        ),
        "estimated_time_label": (
            time_label(
                estimated_minutes
            )
        ),
        "maps_url": maps_url,
        "accessibility_options": (
            place.get(
                "accessibilityOptions"
            )
        ),
        "city_label": city["label"],
        "metrics": {
            "accessibility": (
                accessibility_score(
                    place.get(
                        "accessibilityOptions"
                    )
                )
            ),
            "adventure": (
                ADVENTURE_BY_TYPE.get(
                    primary_type,
                    3,
                )
            ),
            "group_fit": group_fit(
                primary_type,
                party,
            ),
        },
    }


def add_relative_scores(
    places,
    max_distance,
):
    counts = sorted(
        place.get(
            "user_rating_count",
            0,
        )
        for place in places
    )

    for place in places:
        count = place.get(
            "user_rating_count",
            0,
        )

        if len(counts) <= 1:
            percentile = 0.5
        else:
            lower_or_equal = sum(
                value <= count
                for value in counts
            )

            percentile = (
                lower_or_equal - 1
            ) / (
                len(counts) - 1
            )

        popularity = clamp(
            round(
                1
                + 4 * percentile
            ),
            1,
            5,
        )

        nicheness = 6 - popularity

        distance_score = clamp(
            round(
                5
                - 4
                * min(
                    place[
                        "distance_miles"
                    ]
                    / max(
                        max_distance,
                        1,
                    ),
                    1,
                )
            ),
            1,
            5,
        )

        place["metrics"][
            "popularity"
        ] = popularity

        place["metrics"][
            "nicheness"
        ] = nicheness

        place["metrics"][
            "distance"
        ] = distance_score


def add_intro_and_objectives(place):
    rating_phrase = (
        f"{place['rating']}-star "
        if place.get("rating")
        else ""
    )

    place["intro"] = (
        f"A {rating_phrase}"
        f"{place['primary_type_label'].lower()} "
        f"in {place['city_label']}, "
        f"about {place['distance_miles']:.1f} miles "
        f"from the city center. "
        f"Plan on roughly "
        f"{place['estimated_time_label']} "
        f"for a comfortable first visit."
    )

    place["quest_objectives"] = (
        quest_objectives(
            place["primary_type"],
            place["name"],
        )
    )


def demo_places(
    city,
    max_distance,
    party,
):
    output = []

    for index, raw in enumerate(
        DEMO_PLACES
    ):
        distance = haversine_miles(
            city["lat"],
            city["lng"],
            raw["lat"],
            raw["lng"],
        )

        if distance > max_distance:
            continue

        place = {
            **raw,
            "city_label": city["label"],
            "distance_miles": distance,
            "estimated_minutes": (
                estimate_time(
                    raw[
                        "primary_type"
                    ]
                )
            ),
            "estimated_time_label": (
                time_label(
                    estimate_time(
                        raw[
                            "primary_type"
                        ]
                    )
                )
            ),
            "price_label": (
                price_label(
                    raw[
                        "price_level"
                    ]
                )
            ),
            "photo_names": [],
            "demo_photo_urls": (
                DEMO_PHOTOS[index:]
                + DEMO_PHOTOS[:index]
            ),
            "maps_url": (
                "https://www.google.com/maps/search/?api=1&query="
                + quote_plus(
                    raw["name"]
                    + " "
                    + raw["address"]
                )
            ),
            "metrics": {
                "accessibility": None,
                "adventure": (
                    ADVENTURE_BY_TYPE.get(
                        raw[
                            "primary_type"
                        ],
                        3,
                    )
                ),
                "group_fit": (
                    group_fit(
                        raw[
                            "primary_type"
                        ],
                        party,
                    )
                ),
            },
        }

        output.append(place)

    add_relative_scores(
        output,
        max_distance,
    )

    for place in output:
        add_intro_and_objectives(
            place
        )

    return output

def geoapify_primary_type(categories):
    joined = " ".join(categories or [])

    if "catering.cafe" in joined:
        return "cafe"
    if "catering.restaurant" in joined:
        return "restaurant"
    if "entertainment.museum" in joined:
        return "museum"
    if "entertainment.culture.gallery" in joined:
        return "art_gallery"
    if "entertainment.culture.theatre" in joined:
        return "performing_arts_theater"
    if "leisure.park" in joined:
        return "park"
    if "adult.nightclub" in joined:
        return "night_club"
    if "catering.bar" in joined or "catering.pub" in joined:
        return "bar"

    return "tourist_attraction"

@app.get("/")
def root():
    return jsonify({
        "ok": True,
        "service": "Sidequest API",
    })


@app.get("/health")
def health():
    return jsonify({
        "ok": True,
        "provider": "geoapify",
        "geoapify_configured": bool(API_KEY),
    })


@app.get("/places")
def places():
    city_key = request.args.get(
        "city",
        "pittsburgh",
    )

    city = CITY_CONFIG.get(
        city_key,
        CITY_CONFIG["pittsburgh"],
    )

    category = request.args.get(
        "category",
        "surprise",
    )

    party = request.args.get(
        "party",
        "solo",
    )

    try:
        max_minutes = clamp(
            int(
                request.args.get(
                    "max_minutes",
                    120,
                )
            ),
            30,
            360,
        )

        max_distance = clamp(
            float(
                request.args.get(
                    "max_distance",
                    25,
                )
            ),
            1,
            125,
        )

        limit = clamp(
            int(
                request.args.get(
                    "limit",
                    200,
                )
            ),
            1,
            200,
        )

    except ValueError:
        return jsonify({
            "error": (
                "One or more filter "
                "values were invalid."
            )
        }), 400
    
    # Multi-select budget values:
    # 0 = Free
    # 1 = $
    # 2 = $$
    # 3 = $$$
    # 4 = $$$$
    raw_prices = request.args.get(
        "prices",
        "0,1,2",
    )

    try:
        selected_prices = {
            int(value)
            for value
            in raw_prices.split(",")
            if value.strip() != ""
        }

    except ValueError:
        selected_prices = {
            0,
            1,
            2,
        }

    selected_prices = {
        value
        for value in selected_prices
        if 0 <= value <= 4
    }

    # If every box is unchecked,
    # treat that as all prices rather
    # than returning an empty deck.
    if not selected_prices:
        selected_prices = {
            0,
            1,
            2,
            3,
            4,
        }

    if not API_KEY:
        demo = demo_places(
            city,
            max_distance,
            party,
        )
    
        return jsonify({
            "places": demo,
            "source": "demo",
            "warning": (
                "Geoapify API key "
                "is not configured."
            ),
        })
    
    
    categories = GEOAPIFY_CATEGORIES.get(
        category,
        GEOAPIFY_CATEGORIES["surprise"],
    )
    
    categories = geo_categories.get(
        category,
        geo_categories["surprise"],
    )
    
    radius_meters = int(
        max_distance * 1609.344
    )
    
    # Fetch more than the desired final
    # deck size so local filtering has
    # enough candidates to work with.
    fetch_limit = min(
        max(limit * 2, 200),
        500,
    )
    
    params = {
        "categories": categories,
    
        "filter": (
            f"circle:"
            f"{city['lng']},"
            f"{city['lat']},"
            f"{radius_meters}"
        ),
    
        "bias": (
            f"proximity:"
            f"{city['lng']},"
            f"{city['lat']}"
        ),
    
        "limit": fetch_limit,
        "apiKey": API_KEY,
    }
    
    try:
        response = requests.get(
            GEOAPIFY_PLACES_URL,
            params=params,
            timeout=20,
        )
    
    except requests.RequestException as exc:
        return jsonify({
            "error": (
                "Could not reach "
                f"Geoapify: {exc}"
            )
        }), 502
    
    
    if not response.ok:
        try:
            detail = response.json()
        except ValueError:
            detail = response.text
    
        print(
            "GEOAPIFY ERROR:",
            response.status_code,
            detail,
            flush=True,
        )
    
        return jsonify({
            "error": (
                f"Geoapify HTTP "
                f"{response.status_code}: "
                f"{detail}"
            )
        }), response.status_code
    
    
    features = response.json().get(
        "features",
        [],
    )
    
    raw_places = []
    
    
    for feature in features:
        props = feature.get(
            "properties",
            {},
        )
    
        categories_for_place = props.get(
            "categories",
            [],
        )
    
        name = (
            props.get("name")
            or props.get("address_line1")
            or "Unnamed Sidequest"
        )
    
        primary_type = (
            geoapify_primary_type(
                categories_for_place
            )
        )
    
        lat = props.get("lat")
        lng = props.get("lon")
    
        # Some Geoapify responses also
        # carry coordinates in geometry.
        if lat is None or lng is None:
            geometry = feature.get(
                "geometry",
                {},
            )
    
            coordinates = geometry.get(
                "coordinates",
                [],
            )
    
            if len(coordinates) >= 2:
                lng = coordinates[0]
                lat = coordinates[1]
    
        if lat is None or lng is None:
            continue
    
        raw_places.append({
            "id": (
                props.get("place_id")
                or props.get("osm_id")
                or f"{name}-{lat}-{lng}"
            ),
    
            "displayName": {
                "text": name,
            },
    
            "formattedAddress": (
                props.get("formatted")
                or props.get("address_line2")
                or ""
            ),
    
            "location": {
                "latitude": lat,
                "longitude": lng,
            },
    
            # Geoapify does not provide
            # Google-style ratings/prices.
            "rating": None,
            "userRatingCount": 0,
            "priceLevel": None,
    
            "primaryType": primary_type,
    
            "primaryTypeDisplayName": {
                "text": (
                    primary_type
                    .replace("_", " ")
                    .title()
                )
            },
    
            "types": categories_for_place,
    
            # We'll handle real images
            # separately after the deck works.
            "photos": [],
    
            "accessibilityOptions": {},
        })

    normalized = []

    for raw in raw_places:
        place = normalize_place(
            raw,
            city,
            max_distance,
            party,
        )

        if not place:
            continue

        known_price = price_score(
            place.get(
                "price_level"
            )
        )

        # Filter prices locally.
        #
        # This is intentional:
        # PRICE_LEVEL_FREE cannot be
        # sent as a Google Text Search
        # priceLevels request value,
        # and Google price filtering
        # can also exclude place types
        # such as parks/attractions.
        if (
            known_price is not None
            and known_price
            not in selected_prices
        ):
            continue

        # Time is an estimate based
        # on the place's primary type.
        if (
            place[
                "estimated_minutes"
            ]
            > max_minutes * 1.6
        ):
            continue

        normalized.append(
            place
        )

    add_relative_scores(
        normalized,
        max_distance,
    )

    for place in normalized:
        add_intro_and_objectives(
            place
        )

    def rank_score(place):
        rating = (
            place.get("rating")
            or 3.5
        )

        metrics = place["metrics"]

        return (
            rating * 1.3
            + metrics["distance"]
            * 0.65
            + metrics["group_fit"]
            * 0.35
            + random.random()
            * 1.2
        )

    normalized.sort(
        key=rank_score,
        reverse=True,
    )

    return jsonify({
        "places": normalized[:limit],
        "source": "geoapify",
    })


@app.get("/photo")
def photo():
    photo_name = request.args.get(
        "name",
        "",
    ).strip()

    if not photo_name:
        return jsonify({
            "error": (
                "Missing photo name."
            )
        }), 400

    if (
        photo_name.startswith(
            "http://"
        )
        or photo_name.startswith(
            "https://"
        )
    ):
        return redirect(
            photo_name,
            code=302,
        )

    if not GOOGLE_API_KEY:
        return jsonify({
            "error": (
                "Google Places API key "
                "is not configured."
            )
        }), 503

    if not photo_name.startswith(
        "places/"
    ):
        return jsonify({
            "error": (
                "Invalid photo "
                "resource name."
            )
        }), 400

    url = (
        f"{GOOGLE_PHOTO_BASE}/"
        f"{photo_name}/media"
    )

    try:
        response = requests.get(
            url,
            headers={
                "X-Goog-Api-Key": (
                    GOOGLE_API_KEY
                )
            },
            params={
                "maxWidthPx": 1400,
                "maxHeightPx": 1000,
                "skipHttpRedirect": (
                    "true"
                ),
            },
            timeout=10,
        )

    except requests.RequestException as exc:
        return jsonify({
            "error": (
                "Could not fetch "
                f"photo: {exc}"
            )
        }), 502

    if not response.ok:
        return jsonify({
            "error": (
                "Google Places photo "
                "request failed."
            )
        }), response.status_code

    photo_uri = (
        response.json().get(
            "photoUri"
        )
    )

    if not photo_uri:
        return jsonify({
            "error": (
                "Photo URI was "
                "not returned."
            )
        }), 502

    return redirect(
        photo_uri,
        code=302,
    )


if __name__ == "__main__":
    app.run(
        debug=True,
        port=int(
            os.environ.get(
                "PORT",
                5000,
            )
        ),
    )
