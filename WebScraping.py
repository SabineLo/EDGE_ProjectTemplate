#Our Imports 
#CSV stands for Comma Separated Values a file format 
import time
import csv
#Pandas is a powerful data analysis and manipulation library for Python.
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

#python WebScraping.py

# -----------------------
# Webscraping by Sabine
# -----------------------

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--log-level=3")  # Suppress warnings
#Shows us Chrome :D
driver = webdriver.Chrome(options=options)

# Open IMDb page
url = "https://www.imdb.com/list/ls009487211/?sort=list_order,asc"
#It is opening the URL in the Chrome browser
driver.get(url)

# Wait for the page to load
time.sleep(10)  # Adjust if needed

#Lets find this data !
#Goal is to find the class names for the movie title, meta score, star rating, director, and metadata (year, runtime, rating).
# Extract movie elements
#CSS Selectors are used to select elements from the HTML document based on their class names, IDs, or other attributes.
movies = driver.find_elements(By.CSS_SELECTOR, "h3.______")
meta_scores = driver.find_elements(By.CSS_SELECTOR, "span._______")
star_ratings = driver.find_elements(By.CSS_SELECTOR, "span.__________")
directors = driver.find_elements(By.CSS_SELECTOR, "a._________")

# Metadata (Year, Runtime, Rating)
#Might be a bit complicated
metadata_containers = driver.find_elements(By.CSS_SELECTOR, "div._____")

# Prepare data storage
movies_data = []

# Loop through movies
#It's creating a loop that goes through each movie found on the page — one by one — by index.
for i in range(len(movies)):
    #[2,3,2,3,9] = len(movies) = 5
    #This checks if i is a valid index in the movies list (i.e., it ensures i is less than the length of the list
    #We need to make sure i is less then len movies otherwise out of bounds
    if i < len(movies):
        #text.strip() is a method that removes any leading or trailing whitespace from the text.
        movie_title = movies[i].text.strip()
    else:
        movie_title = "N/A"

# For meta score
#This is a check to see if the index i is within the bounds of the meta_scores list.
    if i < len(meta_scores):
        meta_score = _______
    else:
        meta_score = "N/A"

    # For star rating
    if i < len(star_ratings):
        star_rating = _________
    else:
        star_rating = "N/A"

    # For director
    if i < len(directors):
        director = directors[i].text.strip()
    else:
        director = "N/A"

    # Extract metadata (Year, Runtime, Rating)
    if i < len(metadata_containers):
        metadata_items = metadata_containers[i].find_elements(By.CSS_SELECTOR, "___________")

        #It checks if the metadata_items list has any elements.
        #[year, runtime,rating]
        year = metadata_items['_'].text.strip() if len(metadata_items) > 0 else "N/A"
        runtime = metadata_items['_'].text.strip() if len(metadata_items) > 1 else "N/A"
        rating = metadata_items['_'].text.strip() if len(metadata_items) > 2 else "N/A"
    else:
        year, runtime, rating = "N/A", "N/A", "N/A"

    # Store movie data
    #append is a method that adds an element to the end of a list.
    movies_data.append(['____', '_____', '____', '___', '___', '____', '___'])

    #Print format print(f"Movie: {movie}") 
    #The f allows you to input the variables directly into the string using curly braces {}.
    print(f"Movie: {movie_title}")
    print(f"Meta Score: {'_______'}")
    print(f"Star Rating: {'_______'}")
    print(f"Director: {'_______'}")
    print(f"Year: {'_______'}")
    print(f"Runtime: {'_______'}")
    print(f"Rating: {'_______'}")
    print("-" * 40)

# Save to CSV
csv_filename = "imdb_movies.csv"
#What this does is it creates a CSV file called imdb_movies.csv
#The mode "w" means that we are opening the file in write mode, which means that if the file already exists, it will be overwritten.
#The newline="" argument is used to prevent extra blank lines from being added between rows in the CSV file.
with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    # Write header row
    writer.writerow(["Title", "Meta Score", "Star Rating", "Director", "Year", "Runtime", "Rating"])
    writer.writerows(movies_data)

print(f"Data successfully saved to {csv_filename}")

# Close Selenium
#Because we want to close the browser window and end the WebDriver session.
driver.quit()


# -------------------------------
# Cleaning & Analysis by Minjoo
# -------------------------------

# Now, let's load the scraped data into a Pandas Dataframe!
#What is Pandas?
#Pandas is a powerful data analysis and manipulation library for Python.
#Uncomment out !
"""
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
#What is float value?
#A float value is a number that has a decimal point.
def runtime_to_minutes(runtime_str):
#If empty return none
    if pd.isna(runtime_str):
        return None
    
    #For example, "2h 30m" will be split into ["2h", "30m"].
    parts = runtime_str.split()
    total_minutes = 0
    
    for part in parts:
        if '_' in part:
            total_minutes += int(part.replace('h', '')) * 60
        elif '_' in part:
            total_minutes += int(part.replace('m', ''))
    
    return float(total_minutes)

#We are applying the runtime_to_minutes function to the "Runtime" column of the DataFrame.
df["Runtime"] = df["Runtime"].apply(runtime_to_minutes)

print("Converted Runtime to minutes")
print(df.head())



# Cleaning is done! Note that usually data cleaning can be a very long process for more complicated datasets, 
# especially if model training is involved! (making predictions)



# Let's print some analysis!


# Top 5 highest-rated movies
print("\n🎖 Top 5 Movies by Star Rating:")
#Ascending=False means we want the highest ratings first.
print(df.sort_values("column_name", ascending=False)[["Title", "Star Rating", "Year"]].head())


# Group by year – average star rating
print("\n📊 Average Star Rating by Year:")
print(df.groupby("Year")["Star Rating"].mean().dropna().sort_index())

# Most frequent directors
print("\n🎬 Most Frequent Directors:")
print(df["Director"].value_counts().head(5))

# Longest movie
print("\n🕒 Longest Movie:")
#ilove[0] means we want the first row of the sorted DataFrame.
longest = df.sort_values("Runtime", ascending=False).iloc[0]
print(longest[["Title", "Runtime", "Year", "Star Rating"]])
"""