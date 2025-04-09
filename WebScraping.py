import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--log-level=3")  # Suppress warnings
driver = webdriver.Chrome(options=options)

# Open IMDb page
url = "https://www.imdb.com/list/ls009487211/?sort=list_order,asc"
driver.get(url)

# Wait for the page to load
time.sleep(3)  # Adjust if needed

# Extract movie elements
movies = driver.find_elements(By.CSS_SELECTOR, "h3.ipc-title__text")
meta_scores = driver.find_elements(By.CSS_SELECTOR, "span.sc-b0901df4-0.bXIOoL.metacritic-score-box")
star_ratings = driver.find_elements(By.CSS_SELECTOR, "span.ipc-rating-star--rating")
directors = driver.find_elements(By.CSS_SELECTOR, "a.ipc-link.ipc-link--base.sttd-director-item")
metadata_containers = driver.find_elements(By.CSS_SELECTOR, "div.sc-2bbfc9e9-6.cZkKPy.dli-title-metadata")

# Prepare data storage
movies_data = []

# Loop through movies
for i in range(len(movies)):
    movie_title = movies[i].text.strip() if i < len(movies) else "N/A"
    meta_score = meta_scores[i].text.strip() if i < len(meta_scores) else "N/A"
    star_rating = star_ratings[i].text.strip() if i < len(star_ratings) else "N/A"
    director = directors[i].text.strip() if i < len(directors) else "N/A"

    # Extract metadata (Year, Runtime, Rating)
    if i < len(metadata_containers):
        metadata_items = metadata_containers[i].find_elements(By.CSS_SELECTOR, "span.sc-2bbfc9e9-7.jttFlJ.dli-title-metadata-item")
        year = metadata_items[0].text.strip() if len(metadata_items) > 0 else "N/A"
        runtime = metadata_items[1].text.strip() if len(metadata_items) > 1 else "N/A"
        rating = metadata_items[2].text.strip() if len(metadata_items) > 2 else "N/A"
    else:
        year, runtime, rating = "N/A", "N/A", "N/A"

    # Store movie data
    movies_data.append([movie_title, meta_score, star_rating, director, year, runtime, rating])

    print(f"Movie: {movie_title}")
    print(f"Meta Score: {meta_score}")
    print(f"Star Rating: {star_rating}")
    print(f"Director: {director}")
    print(f"Year: {year}")
    print(f"Runtime: {runtime}")
    print(f"Rating: {rating}")
    print("-" * 40)

# Save to CSV
csv_filename = "imdb_movies.csv"
with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Meta Score", "Star Rating", "Director", "Year", "Runtime", "Rating"])
    writer.writerows(movies_data)

print(f"Data successfully saved to {csv_filename}")

# Close Selenium
driver.quit()

#now we need to clean the data and analyze it?
"""Oranize by alphabetical order, by year, by star rating?? Check how many times a direector has been nominated if any
only show the highest rated movie?"""