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


def login_and_scrape_all_hcs(login_url, hc_categories, username, password):
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

        # Prepare data dictionary to hold all HCs
        all_data = {}

        # Loop through each category and HC
        for category, hc_list in hc_categories.items():
            all_data[category] = []
            for hc in hc_list:
                target_url = (
                    f"https://my.minerva.edu/academics/hc-resources/hc-handbook/{hc}/"
                )
                print(f"Navigating to {target_url}...")
                driver.get(target_url)
                time.sleep(5)  # Allow time for the page to load

                # Parse the page content
                page_source = driver.page_source
                soup = BeautifulSoup(page_source, "html.parser")

                # Prepare data dictionary for current HC
                data = {"hc_name": hc}

                # General Example and Footnote
                general_example_section = soup.find("p", id="hc_general_example")
                if general_example_section:
                    # Extract Footnote from the same section
                    footnote = general_example_section.find_next("em")
                    if footnote:
                        # Clean the footnote content
                        footnote_content = (
                            footnote.get_text(strip=True)
                            .replace("Footnote:", "")
                            .strip()
                        )
                        data["footnote"] = footnote_content
                        # Remove the footnote content from the general example
                        footnote.extract()
                    else:
                        data["footnote"] = "Not found"

                    # Extract the cleaned general example content
                    general_example_content = general_example_section.get_text(
                        strip=True
                    )
                    data["general_example"] = general_example_content
                else:
                    data["general_example"] = "Not found"
                    data["footnote"] = "Not found"

                # Extract Cornerstone Introduction
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

                # Extract Guided Reflection Questions
                guided_reflection_section = soup.find("h4", string="Guided Reflection")
                if guided_reflection_section:
                    guided_reflection_questions = [
                        li.get_text(strip=True)
                        for li in guided_reflection_section.find_next("ul").find_all(
                            "li"
                        )
                    ]
                    data["guided_reflection"] = guided_reflection_questions
                else:
                    data["guided_reflection"] = []

                # Extract Common Pitfalls
                common_pitfalls_section = soup.find("h4", string="Common Pitfalls")
                if common_pitfalls_section:
                    common_pitfalls = [
                        li.get_text(strip=True)
                        for li in common_pitfalls_section.find_next("ul").find_all("li")
                    ]
                    data["common_pitfalls"] = common_pitfalls
                else:
                    data["common_pitfalls"] = []

                # Append HC data to the respective category
                all_data[category].append(data)

        # Save all data to a JSON file
        with open("all_hc_data.json", "w", encoding="utf-8") as f:
            json.dump(all_data, f, indent=4, ensure_ascii=False)
        print("All HCs data saved to all_hc_data.json")

    except NoSuchWindowException:
        print("Browser window closed unexpectedly. Restarting the WebDriver...")
    except WebDriverException as e:
        print(f"WebDriver error occurred: {e}")
    finally:
        if "driver" in locals():
            driver.quit()


# Example usage
login_url = "https://my.minerva.edu/application/login/"
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
username = "your_email"
password = "your_password"

login_and_scrape_all_hcs(login_url, HC_CATEGORIES, username, password)
