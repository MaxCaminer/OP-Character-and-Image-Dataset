import requests
from bs4 import BeautifulSoup
from json import dumps

# List to store character names and image URLs
character_data = []

# URL of the One Piece Wiki "List of Canon Characters" page
wiki_url = "https://onepiece.fandom.com/wiki/List_of_Canon_Characters"

# Make a GET request to the URL
wiki_page = requests.get(wiki_url)

# Parse the HTML of the page
wiki_soup = BeautifulSoup(wiki_page.content, "html.parser")

# Find the first two tables on the page
tables = wiki_soup.find_all('table', limit=2)

# Iterate over the tables
for table in tables:
    # Check if the table has more than one row
    if len(table) > 1:
        # Find all the rows in the table
        rows = table.find_all('tr')
        # Iterate over the rows (excluding the first row)
        for row in rows[1:]:
            # Find all the cells in the row
            cells = row.find_all('td')
            # Extract the character name from the second cell
            character_name = cells[1].text.strip()
            # Replace spaces in the character name with underscores for the URL
            url_name = character_name.replace(" ", "_")
            # Construct the URL for the character's page
            character_url = f"https://onepiece.fandom.com/wiki/{url_name}"
            # Make a GET request to the character's page
            character_page = requests.get(character_url)
            # Parse the HTML of the page
            character_soup = BeautifulSoup(character_page.content, "html.parser")
            # Find the image on the page
            character_image = character_soup.find("img", class_="pi-image-thumbnail")
            # Check if the image exists
            if character_image is not None:
                # Extract the image URL and remove everything after ".png"
                image_url = character_image.get('src').rsplit(".png", 1)[0] + ".png"
                # Add the character name and image URL to the list
                character_data.append([character_name, image_url])

# Convert the list to JSON
json_data = dumps(character_data)
print(json_data)
