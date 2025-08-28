from playwright.sync_api import sync_playwright
import mysql.connector
import time
import db_config  # Import database configuration from another file

# ---------- Initialize users list ----------
users = []

# ---------- Connect to the database ----------
try:
    conn = mysql.connector.connect(
        host=db_config.host,
        port=db_config.port,
        user=db_config.user,
        password=db_config.password,
        database=db_config.database
    )
    cursor = conn.cursor(dictionary=True)
    # Fetch users from the table
    #cursor.execute("SELECT name, last_name, password FROM users;")

    # Alternatively, fetch a single user by ID
    user_id = 2
    cursor.execute("SELECT name, last_name, password FROM users WHERE id = %s;", (user_id,))

    users = cursor.fetchall()
    print(f"{len(users)} records obtained from the database")

except mysql.connector.Error as err:
    print(f"Database connection error: {err}")

finally:
    # Close the connection if open
    if 'conn' in locals() and conn.is_connected():
        conn.close()

# ---------- Automate browser using Playwright ----------
playwright = sync_playwright().start()  # Start Playwright manually
browser = playwright.chromium.launch(headless=False)  # Launch Chromium (visible)
page = browser.new_page()

# Navigate to test page
page.goto(
    "https://www.w3schools.com/html/html_forms.asp",
    timeout=60000,
    wait_until="domcontentloaded"
)

# Fill the form with data from the database
for u in users:
    page.fill("input[name='firstname']", u["name"])
    page.fill("input[name='lastname']", u["last_name"])
    # If your form has a password field, you can add:
    # page.fill("input[name='password']", u["password"])
    time.sleep(2)  # Pause to see the actions

# Keep the browser open until Enter is pressed
input("Form filled. Press Enter to close the browser...")

# Close the browser and stop Playwright
browser.close()
playwright.stop()

# ---------- End of script ----------