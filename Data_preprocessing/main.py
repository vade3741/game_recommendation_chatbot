import pandas as pd
from google_play_scraper import search, app

# Initialize an empty list to store the game details
game_details = []

# List of different search terms to diversify results
search_terms = ["top games", "popular games", "trending games", "new games", "best games"]

# Set to store seen app IDs to avoid duplicates
seen_app_ids = set()

# Fetch games using different search terms
for term in search_terms:
    if len(game_details) >= 100:
        break
    
    top_games = search(
        term,
        lang="en",
        country="in",
        n_hits=30
    )
    
    # Fetch details for each game
    for game in top_games:
        if game['appId'] not in seen_app_ids:
            game_info = app(
                game['appId'],
                lang='en',
                country='in'
            )
            game_details.append([
                game_info['title'],
                game_info['appId'],
                game_info['descriptionHTML'],
                game_info['icon'],
                game_info['score'],
                game_info['genre'],
                game_info['price'],
                game_info['installs']
            ])
            seen_app_ids.add(game['appId'])
        
        if len(game_details) >= 100:
            break

# Create a DataFrame from the game details
df = pd.DataFrame(game_details, columns=[
    "Game Name", "Package Name", "Description", "Icon URL", "Rating", "Genre", "Price", "Downloads"
])

# Save the DataFrame to a CSV file
df.to_csv("top_100_games.csv", index=False)
