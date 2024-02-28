from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def setup_driver():
    """Set up Selenium WebDriver for Chrome."""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode
    options.add_argument('--no-sandbox')  # Bypass OS security model, necessary in some environments
    options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def get_acreage(parcel_number):
    """Scrape the acreage information for a given parcel number from Clayton County's public access site."""
    driver = setup_driver()
    try:
        driver.get("https://publicaccess.claytoncountyga.gov/search/commonsearch.aspx?mode=realprop")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "inpParid")))
        search_input = driver.find_element(By.ID, "inpParid")
        search_input.send_keys(parcel_number)

        search_button = driver.find_element(By.ID, "btSearch")
        search_button.click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "searchResults")))
        # Navigate to the first result; adjust if necessary based on the actual page structure
        first_result = driver.find_elements(By.CSS_SELECTOR, "#searchResults tbody tr")[0]
        first_result.click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "Parcel")))
        parcel_info = driver.find_element(By.ID, "Parcel").text

        # Example of extracting acreage; adjust based on actual content and structure
        acreage = "Not Found"
        for line in parcel_info.split('\n'):
            if "Acreage" in line:
                acreage = line.split(":")[-1].strip()
                break

        return {"ParcelNumber": parcel_number, "Acreage": acreage}
    except Exception as e:
        print(f"Error scraping parcel number {parcel_number}: {e}")
        return {"ParcelNumber": parcel_number, "Acreage": "Error"}
    finally:
        driver.quit()

# Example usage (commented out for safety):
# print(get_acreage("123456789"))
