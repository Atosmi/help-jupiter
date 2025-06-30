from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import json

# Setup Selenium
options = Options()
options.add_argument("--headless")  # Run in headless mode
options.add_argument("--disable-gpu")
driver = webdriver.Chrome(options=options)

BASE_URL = "https://community.jupiter.money"
CATEGORY_URL = f"{BASE_URL}/c/help/27"
output = []

# Step 1: Visit the category page and get topic links
driver.get(CATEGORY_URL)
time.sleep(3)  # Wait for JS to load

topic_elements = driver.find_elements(By.CSS_SELECTOR, "a.title")
topic_links = [e.get_attribute("href") for e in topic_elements if e.get_attribute("href")]

print(f"Found {len(topic_links)} topics.")

# Step 2: Visit each topic and extract Q&A
for link in topic_links:
    try:
        driver.get(link)
        time.sleep(2)

        # Get all posts in the thread
        posts = driver.find_elements(By.CSS_SELECTOR, "div.topic-body .cooked")
        if len(posts) < 2:
            continue

        question = posts[0].text.strip()
        answers = [p.text.strip() for p in posts[1:] if p.text.strip()]
        
        for answer in answers:
            output.append({
                "question": question,
                "answer": answer
            })

        print(f"✅ Scraped topic: {link}")

    except Exception as e:
        print(f"❌ Error scraping {link}: {e}")

# Step 3: Save to JSON
with open("jupiter_help_qas.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"\n✅ Saved {len(output)} Q&A pairs to jupiter_help_qas.json")

# Cleanup
driver.quit()
