import time
import csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

# -----------------------
# Webscraping by Sabine
# -----------------------

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

print(f"✅ Data successfully saved to {csv_filename}")

# Close Selenium
driver.quit()


# -------------------------------
# Cleaning & Analysis by Minjoo
# -------------------------------

# Now, let's load the scraped data into a Pandas Dataframe!
df = pd.read_csv("imdb_movies.csv")

# Let's take a peek at the first few rows of the dataframe
print("Initial dataframe:")
print(df.head())

# Then drop rows with any missing values
df = df.replace("N/A", pd.NA) 
df = df.dropna()

# Let's get rid of the numbering in the Title column
df["Title"] = df["Title"].str.replace(r"^\d+\.\s*", "", regex=True)     
            # "^\d+\.\s*" means : 
                                    # ^ makes sure we're looking at the start of the string
                                    # \d+ matches to any number of digits (1, 12, 123, etc.)
                                    # \. matches to a literal dot or period
                                    # \s* matches any number of spaces
                                    # this in all works to replace strings like "12. " or "145. " with ""
            # regex=True means :
                                    # regex: regular expression
                                    # A regular expression (aka regex) is a pattern language 
                                    # that lets you match a wide variety of similar text patterns, 
                                    # using special symbols (like we just did).
print("Removed numbering in Title")
print(df.head())

# Right now the Runtime of the movies is in hour and minute format as a String. Let's represent it as a float value!
# (note to Sabine: you can have them fill in the blanks to the code below so it's not so hard)
def runtime_to_minutes(runtime_str):
    if pd.isna(runtime_str):
        return None
    
    parts = runtime_str.split()
    total_minutes = 0
    
    for part in parts:
        if 'h' in part:
            total_minutes += int(part.replace('h', '')) * 60
        elif 'm' in part:
            total_minutes += int(part.replace('m', ''))
    
    return float(total_minutes)

df["Runtime"] = df["Runtime"].apply(runtime_to_minutes)

print("Converted Runtime to minutes")
print(df.head())



# Cleaning is done! Note that usually data cleaning can be a very long process for more complicated datasets, 
# especially if model training is involved! 


# Let's print some analysis!


# Top 5 highest-rated movies
print("\n🎖 Top 5 Movies by Star Rating:")
print(df.sort_values("Star Rating", ascending=False)[["Title", "Star Rating", "Year"]].head(5))

# Group by year – average star rating
print("\n📊 Average Star Rating by Year:")
print(df.groupby("Year")["Star Rating"].mean().dropna().sort_index())

# Most frequent directors
print("\n🎬 Most Frequent Directors:")
print(df["Director"].value_counts().head(5))

# Longest movie
print("\n🕒 Longest Movie:")
longest = df.sort_values("Runtime", ascending=False).iloc[0]
print(longest[["Title", "Runtime", "Year", "Star Rating"]])
