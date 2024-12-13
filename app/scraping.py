from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchWindowException, WebDriverException
from bs4 import BeautifulSoup
import time
import json


def login_and_scrape_selenium(login_url, target_url, username, password):
    try:
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--window-size=1920,1080")

        # Initialize the WebDriver
        driver = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(driver, 10)

        # Step 1: Open the login page
        print("Opening login page...")
        driver.get(login_url)

        # Step 2: Log in
        print("Logging in...")
        username_input = wait.until(EC.presence_of_element_located((By.NAME, "email")))
        password_input = driver.find_element(By.NAME, "password")
        username_input.send_keys(username)
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)

        # Wait for redirection after login
        time.sleep(5)

        # Step 3: Navigate to the target page
        print("Navigating to the target page...")
        driver.get(target_url)
        time.sleep(5)  # Allow time for the page to load

        # Step 4: Parse the loaded page content
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")

        # Debug: Save the HTML for inspection
        with open("debug_output_selenium.html", "w", encoding="utf-8") as f:
            f.write(soup.prettify())
        print("HTML written to debug_output_selenium.html for inspection.")

        # Prepare data dictionary
        data = {}

        # Step 5: Extract HC Name from the URL
        hc_name = target_url.rstrip("/").split("/")[-1]
        data["hc_name"] = hc_name

        # General Example and Footnote
        general_example_section = soup.find("p", id="hc_general_example")
        if general_example_section:
            general_example_content = general_example_section.get_text(strip=True)
            data["general_example"] = general_example_content

            # Extract Footnote from the same section
            footnote = general_example_section.find_next("em")
            if footnote:
                footnote_content = footnote.get_text(strip=True)
                data["footnote"] = footnote_content
            else:
                data["footnote"] = "Not found"
        else:
            data["general_example"] = "Not found"

        # Step 7: Extract Cornerstone Introduction
        cornerstone_section = soup.find("h4", string="Cornerstone Introduction")
        if cornerstone_section:
            cornerstone_content = cornerstone_section.find_next("div").get_text(
                strip=True
            )
            cornerstone_content = (
                cornerstone_content.replace("Class:", "").split("|")[0].strip()
            )  # Keep only the first part
            data["cornerstone"] = cornerstone_content
        else:
            data["cornerstone"] = "Not found"

        # Step 8: Extract Guided Reflection Questions
        guided_reflection_section = soup.find("h4", string="Guided Reflection")
        if guided_reflection_section:
            guided_reflection_questions = [
                li.get_text(strip=True)
                for li in guided_reflection_section.find_next("ul").find_all("li")
            ]
            data["guided_reflection"] = guided_reflection_questions
        else:
            data["guided_reflection"] = []

        # Step 9: Extract Common Pitfalls
        common_pitfalls_section = soup.find("h4", string="Common Pitfalls")
        if common_pitfalls_section:
            common_pitfalls = [
                li.get_text(strip=True)
                for li in common_pitfalls_section.find_next("ul").find_all("li")
            ]
            data["common_pitfalls"] = common_pitfalls
        else:
            data["common_pitfalls"] = []

        # Save data to a JSON file
        with open("scraped_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print("Scraped data saved to scraped_data.json")

    except NoSuchWindowException:
        print("Browser window closed unexpectedly. Restarting the WebDriver...")
    except WebDriverException as e:
        print(f"WebDriver error occurred: {e}")
    finally:
        if "driver" in locals():
            driver.quit()


# Replace with your login and target URLs
login_url = "https://my.minerva.edu/application/login/"
target_url = "https://my.minerva.edu/academics/hc-resources/hc-handbook/audience/"
username = "your_email"
password = "your_pasword"

login_and_scrape_selenium(login_url, target_url, username, password)
