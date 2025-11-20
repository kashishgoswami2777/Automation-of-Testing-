from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time, traceback

EMAIL = "gkashish152@gmail.com"
PASSWORD = "Kashyiselegant@123"
PROFILE_NAME = "gkashish152"
SEARCH_TITLE = "Delhi Crime"

# Setup Chrome
options = webdriver.ChromeOptions()
options.add_argument("--disable-gpu")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    print("\n Starting login...")
    driver.get("https://www.netflix.com/in/login")

    # Email
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "userLoginId"))
    ).send_keys(EMAIL)

    # Password
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "password"))
    ).send_keys(PASSWORD)

    # Click Login
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-uia='sign-in-button']"))
    ).click()
    print(" Login submitted.")

    # Wait Profiles
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, "profile-name"))
    )
    print(" Profiles loaded.")

    # Select Profile
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//span[text()='{PROFILE_NAME}']"))
    ).click()
    print(f" Profile selected: {PROFILE_NAME}")

    # Wait Home Page
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "mainView"))
    )
    print(" Home loaded!")

    # Close Popups
    time.sleep(2)
    popup_selectors = [
        ".nf-modal",
        ".previewModal-close",
        "role=dialog button.close",
        "button[data-uia='modal-close']",
        "button[data-uia='close-button']",
        ".btn-secondary",
        ".close"
    ]

    for selector in popup_selectors:
        try:
            pop = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
            )
            driver.execute_script("arguments[0].click();", pop)
            print(f" Closed popup: {selector}")
            time.sleep(1)
        except:
            pass

    try:
        modals = driver.find_elements(By.CSS_SELECTOR, ".nf-modal")
        for m in modals:
            driver.execute_script("arguments[0].remove();", m)
            print(" Removed leftover modal element.")
    except:
        pass

    #  OPEN SEARCH BOX
    for i in range(3):
        try:
            search_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-uia='search-box-launcher']"))
            )
            driver.execute_script("arguments[0].click();", search_btn)
            time.sleep(1.5)
            break
        except:
            print(f" Retry search button... {i+1}")
            time.sleep(1)

    #  TYPE WITHOUT CLICKING
    search_input = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-uia='search-box-input']"))
    )
    time.sleep(1)
    search_input.send_keys(SEARCH_TITLE)
    time.sleep(2)
    print(f" Searching for: {SEARCH_TITLE}")

    #  CLICK SEARCH RESULT
    movie = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, f"//*[@data-uia='search-gallery-video-card' and @aria-label='{SEARCH_TITLE}']")
        )
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", movie)
    time.sleep(1)
    driver.execute_script("arguments[0].click();", movie)
    print(f" Opened: {SEARCH_TITLE}")

    #   AUTO SKIP + AUTOPLAY
    #   AUTO SKIP + NEXT EPISODE 
    print(" Watching & Auto-Skipping for 5 seconds...")

    start_time = time.time()

    while time.time() - start_time < 5:  # run for 5 seconds only
      try:
        driver.execute_script("document.dispatchEvent(new MouseEvent('mousemove', {clientX:10, clientY:10}));")
      except:
        pass

      try:
        skip_intro = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-uia='player-skip-intro']"))
        )
        driver.execute_script("arguments[0].click();", skip_intro)
        print(" Skipped Intro.")
      except:
        pass

      try:
        skip_recap = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-uia='player-skip-recap']"))
        )
        driver.execute_script("arguments[0].click();", skip_recap)
        print("⏭ Skipped Recap.")
      except:
        pass

      try:
        next_ep = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-uia='player-next-episode']"))
        )
        driver.execute_script("arguments[0].click();", next_ep)
        print(" Auto-playing Next Episode.")
      except:
        pass

    time.sleep(1)

    print(" Stopping Auto-Skip...")
  
except Exception as e:
    print("\n Error:", e)
    traceback.print_exc()

finally:
    driver.quit()
