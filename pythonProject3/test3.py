import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_driver():
    service = Service("D:\\QA\\driver.exe")  # Adjust the path as needed
    options = webdriver.ChromeOptions()
    options.add_argument("--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/85.0.4183.109 Mobile/15E148 Safari/604.1")
    return webdriver.Chrome(service=service, options=options)

def login_to_openinapp(driver):
    driver.get("https://app.openinapp.com/")
    logging.info(f"Accessing URL: {driver.current_url}")

    try:
        # Login Button
        login_button = WebDriverWait(driver, 120).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[1]/div/div[2]/div[1]/div[2]/div/button/div/p"))
        )
        login_button.click()

        # Contact Input
        contact_input = WebDriverWait(driver, 120).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div[2]/button[2]"))
        )
        contact_input.send_keys("Your Phone Number or Email Here")

        # Send OTP Button
        send_otp_button = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div/div/div[3]/div/form/button")
        send_otp_button.click()

        # OTP Input
        otp_input = WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[2]/div/div/div[3]/div/form/div/div[1]/div[4]/input"))
        )

        otp = input("Please enter the OTP you received: ")
        otp_input.send_keys(otp)

        # Verify Button
        verify_button = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div/div/div[3]/div/form/button/div/p")
        verify_button.click()

        # Wait for the Dashboard to Load
        WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[1]/div/div[2]/div[1]"))
        )
        logging.info("Successfully logged in")
    except (TimeoutException, NoSuchElementException) as e:
        logging.error(f"Login failed: {str(e)}")
        raise

def create_topsecret_links(driver):
    links = []
    for i in range(4):
        try:
            # Create TopSecret Link Button
            create_link_button = WebDriverWait(driver, 120).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[1]/div/div[2]/div[3]/div/div[1]/div/button/div/p"))
            )
            create_link_button.click()

            # Resource URL Input Field
            resource_url_input = WebDriverWait(driver, 120).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/div[2]/div[2]/input"))
            )
            resource_url_input.send_keys(f"https://Ash.topsecret.link/dutyd{i+1}")

            # Resource Title Input Field
            driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div[2]/div[1]/div[2]/div/input").send_keys(f"Special_LInk {i+1}")

            # Generate Link Button
            generate_button = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/div/div[2]/div[3]/div[1]/div[2]/button")
            generate_button.click()

            # Copy Generated Link
            generated_link = WebDriverWait(driver, 120).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div"))
            ).get_attribute("value")

            links.append(generated_link)
            logging.info(f"Created TopSecret Link {i+1}: {generated_link}")

        except (TimeoutException, NoSuchElementException) as e:
            logging.error(f"Failed to create TopSecret Link {i+1}: {str(e)}")

    return links

def update_instagram_bio(links):
    print("Please update your Instagram bio with the following links:")  # NOT TO VIOLATE INSTAGRAM POLICIES THIS CAN BE DONE MANUALLY #
    for i, link in enumerate(links, 1):
        print(f"Link {i}: {link}")
    print("\nInstructions:")
    print("1. Open Instagram on your mobile device")
    print("2. Go to your profile")
    print("3. Tap 'Edit Profile'")
    print("4. Update the website field with these links")
    input("Press Enter when you have updated your Instagram bio...")
    logging.info("Instagram bio update confirmed by user")

def access_resources(driver, links):
    for i, link in enumerate(links, 1):
        try:
            driver.get(link)

            WebDriverWait(driver, 120).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            if "expected_text" in driver.page_source:
                logging.info(f"Successfully accessed resource {i}: {driver.title}")
            else:
                logging.warning(f"Resource {i} may not have loaded correctly: {driver.title}")
            time.sleep(2)  # Add a small delay between accesses
        except TimeoutException:
            logging.error(f"Failed to access resource {i}: {link}")

def main():
    driver = setup_driver()
    try:
        login_to_openinapp(driver)
        links = create_topsecret_links(driver)
        update_instagram_bio(links)
        access_resources(driver, links)
        logging.info("Test completed successfully")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        logging.error(f"Current URL: {driver.current_url}")
        logging.error(f"Page source: {driver.page_source}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
