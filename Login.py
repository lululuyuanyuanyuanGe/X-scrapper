from playwright.sync_api import sync_playwright
import json
import time

def login_to_twitter():
    with sync_playwright() as p:
        # Launch the browser (set headless=False to see the browser)
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Go to the Twitter login page
        page.goto("https://twitter.com/login")

        # Fill in the email field
        page.fill("input[name='text']", "Enter your X account email here")
        page.click("button:has-text('Next')")

        # Fill in the username field
        page.fill("input[name='text']", "Enter your X account username here")
        page.click("button:has-text('Next')")

        # Wait for the password field to appear
        page.wait_for_selector("input[name='password']")

        # Fill in the password
        page.fill("input[name='password']", "   Enter your X account password here")  
        page.click("button:has-text('Log in')")

        # Wait for the home page to load as an indication of a successful login
        page.wait_for_selector("a[data-testid='AppTabBar_Home_Link']", timeout=10000)
        time.sleep(5)  # Adjust timeout if needed
        print("Login successful")

        # Save cookies for later use
        cookies = context.cookies()
        with open("cookies.json", "w") as f:
            json.dump(cookies, f)
        print("Cookies saved to cookies.json")

        # Close the browser
        time.sleep(5) 
        browser.close()