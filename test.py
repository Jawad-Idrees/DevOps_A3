from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pytest
from email.mime.application import MIMEApplication




def create_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)
@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")  # Comment out if you want to see the browser
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    yield driver
    driver.quit()

# ========== TEST CASES ==========

# TC 1: Homepage loads successfully
def test_homepage_loads():
    driver = create_driver()
    driver.get("http://localhost:8000")
    assert "Bank" in driver.page_source
    driver.quit()


# TC 2: Successful login with correct credentials (Positive)
def test_login_success():
    driver = create_driver()
    driver.get("http://localhost:8000")
    time.sleep(2)

    driver.find_element(By.XPATH, "//input[@type='email']").send_keys("jawadidrees822@gmail.com")
    driver.find_element(By.XPATH, "//input[@type='password']").send_keys("jujujuju")
    driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]").click()
    time.sleep(2)

    assert "EasTransfer" in driver.page_source or "Home" in driver.page_source
    driver.quit()


# TC 3: Login fails with incorrect password (Negative)
def test_login_fail_wrong_password():
    driver = create_driver()
    driver.get("http://localhost:8000")
    time.sleep(2)

    driver.find_element(By.XPATH, "//input[@type='email']").send_keys("jawadidrees822@gmail.com")
    driver.find_element(By.XPATH, "//input[@type='password']").send_keys("wrongpass")
    driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]").click()
    time.sleep(2)

    assert "Invalid Credential!" in driver.page_source or "Sign into your account" in driver.page_source
    driver.quit()


# TC 4: Login fails with empty username (Negative)
def test_login_empty_username():
    driver = create_driver()
    driver.get("http://localhost:8000")
    time.sleep(2)

    driver.find_element(By.XPATH, "//input[@type='password']").send_keys("pass123")
    driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]").click()
    time.sleep(2)

    assert "Please enter both email and password." in driver.page_source or "Bank" in driver.page_source
    driver.quit()



# TC 5: Sign up fails short password (Negative)
def test_signup_short_password():
    driver = create_driver()
    driver.get("http://localhost:8000/signup?")
    time.sleep(2)

    driver.find_element(By.ID, "username").send_keys("validuser")
    driver.find_element(By.ID, "email").send_keys("valid@example.com")
    driver.find_element(By.ID, "password").send_keys("123")
    driver.find_element(By.ID, "confirmPassword").send_keys("123")
    driver.find_element(By.XPATH, "//button[text()='Sign Up']").click()

    time.sleep(1)
    assert "Password must be at least 6 characters long" in driver.page_source
    driver.quit()


# TC 6: Sign up fails duplicate email (Negative)
def test_signup_with_duplicate_email_and_login_failure():
    driver = create_driver()

    # 1. Sign up with an email that already exists (should appear successful but silently fail)
    driver.get("http://localhost:8000/signup?")
    time.sleep(2)
    driver.find_element(By.ID, "username").clear()
    driver.find_element(By.ID, "email").clear()
    driver.find_element(By.ID, "password").clear()
    driver.find_element(By.ID, "confirmPassword").clear()

    driver.find_element(By.ID, "username").send_keys("duplicate_user")
    driver.find_element(By.ID, "email").send_keys("jawadidrees822@gmail.com")  # Already in DB
    driver.find_element(By.ID, "password").send_keys("securepass")
    driver.find_element(By.ID, "confirmPassword").send_keys("securepass")
    driver.find_element(By.XPATH, "//button[text()='Sign Up']").click()
    time.sleep(3)  # Wait for navigation or form submission to complete

    # 2. Try to login with the duplicate credentials (should fail)
    driver.get("http://localhost:8000")
    time.sleep(2)
    driver.find_element(By.XPATH, "//input[@type='email']").send_keys("jawadidrees822@gmail.com")
    driver.find_element(By.XPATH, "//input[@type='password']").send_keys("securepass")
    driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]").click()
    time.sleep(3)

    # 3. Verify login failed due to invalid credentials
    assert "Invalid Credential!" in driver.page_source

    driver.quit()




# TC 7: Sign up fails invalid email (Negative)
def test_signup_invalid_email():
    driver = create_driver()
    driver.get("http://localhost:8000/signup?")

    driver.find_element(By.ID, "username").send_keys("validuser")
    driver.find_element(By.ID, "email").send_keys("invalid-email")
    driver.find_element(By.ID, "password").send_keys("securepass")
    driver.find_element(By.ID, "confirmPassword").send_keys("securepass")
    driver.find_element(By.XPATH, "//button[text()='Sign Up']").click()

    time.sleep(1)
    assert "Please enter a valid email address" in driver.page_source
    driver.quit()

# TC 8 Balance is Zero for first time sign in
def login(driver, email, password):
    #driver = create_driver()
    driver.get("http://localhost:8000/signin")
    time.sleep(1)
    driver.find_element(By.XPATH, "//input[@type='email']").send_keys(email)
    driver.find_element(By.XPATH, "//input[@type='password']").send_keys(password)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]").click()
    time.sleep(5)

def test_homepage_initial_balance_is_zero(driver):
    
    login(driver, "jawadidrees822@gmail.com", "jujujuju")
    assert "$0" in driver.page_source or "$0.00" in driver.page_source


# TC 9 Logout Successful
# def test_logout_redirect(driver):
#     login(driver, "jawadidrees822@gmail.com", "jujujuju")
#     driver.find_element(By.XPATH, "//a[@href='/logout' and contains(text(), 'Logout')]").click()
#     time.sleep(2)
#     assert "Bank" in driver.page_source or "Email" in driver.page_source


def test_logout_redirect(driver):
    login(driver, "jawadidrees822@gmail.com", "jujujuju")

    # Wait for and click the navbar toggle button
    toggle = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "navbar-toggler"))
    )
    toggle.click()

    # Wait for logout link to be clickable
    logout_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Logout"))
    )
    logout_link.click()

    # Wait for redirected page content
    # WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Bank') or contains(text(), 'Email')]"))
    # )

    assert "Bank" in driver.page_source or "Email" in driver.page_source


# TC 10 Username set at sign up appears in home screen
def test_username_appears_on_homepage_after_signup(driver):
    # --- Test Data ---
    username = "uniqueuser123"
    email = "uniqueuser123@example.com"
    password = "StrongPass123"

    # --- Sign Up ---
    driver.get("http://localhost:8000/signup?")
    time.sleep(1)
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "confirmPassword").send_keys(password)
    driver.find_element(By.XPATH, "//button[text()='Sign Up']").click()
    time.sleep(2)

    # --- Sign In ---
    driver.get("http://localhost:8000")
    time.sleep(1)
    driver.find_element(By.XPATH, "//input[@type='email']").send_keys(email)
    driver.find_element(By.XPATH, "//input[@type='password']").send_keys(password)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]").click()
    time.sleep(2)

    # --- Verify username appears on home page ---
    page_text = driver.page_source
    assert username in page_text, f"Expected username '{username}' to appear on homepage"


