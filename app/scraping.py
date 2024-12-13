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

HC_CATEGORIES = {
    "COMPLEX_SYSTEMS": [
        "levelsofanalysis",
        "shapingbehavior",
        "systemmapping",
        "emergentproperties",
        "complexcausality",
        "networks",
        "systemdynamics",
        "negotiate",
        "ethicalconsiderations",
        "ethicalcourage",
        "ethicaljudgment",
        "conformity",
        "differences",
        "emotionaliq",
        "leadprinciples",
        "powerdynamics",
        "responsibility",
        "selfawareness",
        "strategize",
        "psychologicalexplanation",
        "purpose",
    ],
    "FORMAL_ANALYSES": [
        "algorithms",
        "optimization",
        "confidenceintervals",
        "correlation",
        "descriptivestats",
        "distributions",
        "probability",
        "regression",
        "significance",
        "decisiontrees",
        "utility",
        "gametheory",
        "variables",
        "estimation",
        "deduction",
        "fallacies",
        "induction",
    ],
    "MULTIMODAL_COMMUNICATIONS": [
        "audience",
        "composition",
        "connotation",
        "organization",
        "professionalism",
        "thesis",
        "communicationdesign",
        "expression",
        "medium",
        "multimedia",
        "persuasion",
        "designthinking",
        "context",
        "critique",
        "interpretivelens",
        "evidencebased",
        "sourcequality",
    ],
    "EMPIRICAL_ANALYSES": [
        "dataviz",
        "casestudy",
        "comparisongroups",
        "interventionalstudy",
        "interviewsurvey",
        "observationalstudy",
        "sampling",
        "studyreplication",
        "hypothesisdevelopment",
        "modeling",
        "analogies",
        "constraints",
        "heuristics",
        "scienceoflearning",
        "biasidentification",
        "biasmitigation",
        "breakitdown",
        "gapanalysis",
        "rightproblem",
        "plausibility",
        "testability",
    ],
}


def scrape_all_hcs(login_url, base_url, username, password):
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

        # Step 1: Log in
        print("Logging in...")
        driver.get(login_url)
        username_input = wait.until(EC.presence_of_element_located((By.NAME, "email")))
        password_input = driver.find_element(By.NAME, "password")
        username_input.send_keys(username)
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)

        # Wait for redirection after login
        time.sleep(5)

        # Initialize results dictionary
        results = {category: [] for category in HC_CATEGORIES}

        # Step 2: Scrape each HC
        for category, hcs in HC_CATEGORIES.items():
            print(f"Scraping category: {category}")
            for hc in hcs:
                target_url = f"{base_url}/{hc}/"
                print(f"Scraping HC: {hc} at {target_url}")

                # Navigate to the HC page
                driver.get(target_url)
                time.sleep(5)  # Allow time for the page to load

                # Parse the page
                page_source = driver.page_source
                soup = BeautifulSoup(page_source, "html.parser")

                # Extract HC details
                data = {"hc_name": hc, "cornerstone": category}

                # General Example and Footnote
                general_example_section = soup.find("p", id="hc_general_example")
                if general_example_section:
                    general_example_content = general_example_section.get_text(
                        strip=True
                    )
                    data["general_example"] = general_example_content

                    # Extract Footnote
                    footnote = general_example_section.find_next("em")
                    if footnote:
                        footnote_content = footnote.get_text(strip=True)
                        data["footnote"] = footnote_content
                    else:
                        data["footnote"] = "Not found"
                else:
                    data["general_example"] = "Not found"

                # Cornerstone Introduction
                cornerstone_section = soup.find("h4", string="Cornerstone Introduction")
                if cornerstone_section:
                    cornerstone_content = cornerstone_section.find_next("div").get_text(
                        strip=True
                    )
                    cornerstone_content = (
                        cornerstone_content.replace("Class:", "").split("|")[0].strip()
                    )
                    data["cornerstone"] = cornerstone_content
                else:
                    data["cornerstone"] = "Not found"

                # Append to results
                results[category].append(data)

        # Save results to JSON file
        with open("all_hcs_data.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4, ensure_ascii=False)
        print("All HC data saved to all_hcs_data.json")

    except NoSuchWindowException:
        print("Browser window closed unexpectedly. Restarting the WebDriver...")
    except WebDriverException as e:
        print(f"WebDriver error occurred: {e}")
    finally:
        if "driver" in locals():
            driver.quit()


# Replace with your login URL and base URL
login_url = "https://my.minerva.edu/application/login/"
base_url = "https://my.minerva.edu/academics/hc-resources/hc-handbook"
username = "your_email"
password = "your_password"

scrape_all_hcs(login_url, base_url, username, password)
