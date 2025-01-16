# --------------------------------------- #
#     Filename: get_daily_quote.py
#       Author: Steven Wasserman 
#      Created: Thu Jan 16 2025
# Last Updated: Thu Jan 16 2025
#      Contact: steven.wasserman@datarobot.com
#  Description: Module that grabs a daily quote from a website
#               and updates the README.md file in the repository.
# --------------------------------------- #
# Import packages
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import subprocess
from datetime import datetime
# Function to extract daily quote
def get_daily_quote():
    # Set up ChromeDriver
    options = webdriver.ChromeOptions()
    # Run headless (without opening a window)
    options.add_argument('--headless')  
    driver = webdriver.Chrome(options=options)
    # Open the website
    url = 'https://www.minimizemymess.com/random-quote-generator'
    driver.get(url)
    # Wait for the page to load
    time.sleep(2)
    # Extract the quote and author using XPath
    try:
        quote = driver.find_element(By.XPATH, '/html/body/div[1]/main/article/section[1]/div[2]/div/div/div/div/div[2]/div/main/section/div/div/div/p/span[1]')
        author = driver.find_element(By.XPATH, '/html/body/div[1]/main/article/section[1]/div[2]/div/div/div/div/div[2]/div/main/section/div/div/div/p/span[2]/i')
    except Exception as e:
        print(f"Error: {e}")
        driver.quit()
        return None
    # Format the quote
    formatted_quote = f'"{quote.text}" - {author.text}'
    # Quit the driver
    driver.quit()
    # Return out
    return formatted_quote

# Function to update the README.md with the new quote
def update_readme(quote):
    readme_path = "README.md"
    # Read the existing README.md content
    with open(readme_path, "r") as file:
        readme_content = file.readlines()
    # Insert the quote at a specific place in README.md
    today = datetime.today().strftime('%Y-%m-%d')
    quote_section_start = "## Today's Quote"
    quote_section_end = "<!-- END OF QUOTE -->"
    # Find the location of the quote section
    try:
        start_index = readme_content.index(quote_section_start + "\n") + 1
        end_index = readme_content.index(quote_section_end + "\n")
    except ValueError:
        print("Error: Couldn't find quote section in README.md")
        return
    # Replace the existing quote (if any) with the new one
    new_readme_content = readme_content[:start_index] + [f"{quote}\n"] + readme_content[end_index:]
    # Write the updated content back to README.md
    with open(readme_path, "w") as file:
        file.writelines(new_readme_content)
    print(f"README.md updated with quote: {quote}")

# Function to commit and push changes to GitHub
def commit_and_push():
    # Commit the changes to the repository
    subprocess.run(["git", "add", "README.md"], check=True)
    subprocess.run(["git", "commit", "-m", "Updated daily quote"], check=True)
    # Push to GitHub (ensure you have configured git with your credentials)
    subprocess.run(["git", "push"], check=True)

if __name__ == "__main__":
    quote = get_daily_quote()
    if quote:
        update_readme(quote)
        commit_and_push()
