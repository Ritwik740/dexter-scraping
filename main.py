# import requests
# import json
# import time
# from datetime import datetime
# SEEN_TOKENS_FILE = "seen_token_profiles.json"
# CHECK_INTERVAL = 10  # seconds

# # Load seen tokens
# try:
#     with open(SEEN_TOKENS_FILE, "r") as f:
#         seen_token_ids = set(json.load(f))
# except FileNotFoundError:
#     seen_token_ids = set()

# # def check_new_tokens():
# #     global seen_token_ids
# #     url = "https://api.dexscreener.com/token-profiles/latest/v1"
# #     headers = {
# #         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
# #     }

# #     try:
# #         response = requests.get(url, headers=headers)
# #         print(f"\n[+] Status Code: {response.status_code}")
# #         current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# #         print(f"Last checked at: {current_time}")

# #         if response.status_code != 200:
# #             print("❌ Failed to fetch data. Response:")
# #             print(response.text[:300])
# #             return

# #         data = response.json()  # This is a list, not a dict
# #         new_detected = False

# #         for token in data:
# #             token_id = token.get("tokenAddress")
# #             token_name = token.get("name") or token.get("symbol") or "Unknown Token"

# #             chain = token.get("chainId", "unknown")
# #             token_url = f"https://dexscreener.com/{chain}/{token_id}"

# #             if token_id and token_id not in seen_token_ids:
# #                 print("🆕 New Token Detected!")
# #                 print(f"Name : {token_name}")
# #                 print(f"URL  : {token_url}")
# #                 print(f"Chain: {chain}")
# #                 print(f"Token ID: {token_id}")
# #                 print(f"Token Address: {token.get('tokenAddress')}")
# #                 print("-" * 40)
# #                 seen_token_ids.add(token_id)
# #                 new_detected = True

# #         if new_detected:
# #             with open(SEEN_TOKENS_FILE, "w") as f:
# #                 json.dump(list(seen_token_ids), f)

# #     except requests.exceptions.RequestException as e:
# #         print("❌ Request failed:", e)
# #     except Exception as e:
# #         print("❌ Unexpected error:", e)


# def check_new_tokens():
#     global seen_token_ids
#     url = "https://api.dexscreener.com/token-profiles/latest/v1"
#     headers = {
#         "User-Agent": "Mozilla/5.0"
#     }

#     try:
#         response = requests.get(url, headers=headers)
#         print(f"\n[+] Status Code: {response.status_code}")

#         if response.status_code != 200:
#             print("❌ Failed to fetch data. Response:")
#             print(response.text[:300])
#             return

#         data = response.json()
#         new_detected = False

#         for token in data:
#             token_id = token.get("tokenAddress")
#             if token_id and token_id not in seen_token_ids:
#                 token_name = token.get("name") or token.get("symbol") or "Unknown Token"
#                 chain = token.get("chainId", "unknown")
#                 profile_url = token.get("url", f"https://dexscreener.com/{chain}/{token_id}")
#                 icon_url = token.get("icon", "N/A")
#                 header_url = token.get("header", "N/A")
#                 description = token.get("description", "No description provided")
#                 links = token.get("links", [])

#                 print("🆕 New Token Detected!")
#                 print(f"Name        : {token_name}")
#                 print(f"Chain ID    : {chain}")
#                 print(f"Address     : {token_id}")
#                 print(f"Profile URL : {profile_url}")
#                 print(f"Icon URL    : {icon_url}")
#                 print(f"Header URL  : {header_url}")
#                 print(f"Description : {description}")
#                 print("Links       :")
#                 for link in links:
#                     print(f"  - [{link.get('type', 'N/A')}] {link.get('label', 'N/A')} → {link.get('url', 'N/A')}")
#                 print("-" * 50)

#                 seen_token_ids.add(token_id)
#                 new_detected = True

#         if new_detected:
#             with open(SEEN_TOKENS_FILE, "w") as f:
#                 json.dump(list(seen_token_ids), f)

#     except requests.exceptions.RequestException as e:
#         print("❌ Request failed:", e)
#     except Exception as e:
#         print("❌ Unexpected error:", e)

# # Run in loop
# if __name__ == "__main__":
#     print("🚀 Starting Dexscreener Token Profile Monitor...")
#     while True:
#         check_new_tokens()
#         time.sleep(CHECK_INTERVAL)


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# Setup headless Chrome
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = "https://dexscreener.com/token-profiles"
driver.get(url)
time.sleep(5)  # Wait for JS to render

tokens = driver.find_elements(By.CSS_SELECTOR, "div[class^='TokenProfileCard_card__']")
print(f"Found {len(tokens)} token profiles.\n")

for token in tokens:
    try:
        name = token.find_element(By.CSS_SELECTOR, "div[class*='TokenProfileCard_name__']").text
        description = token.find_element(By.CSS_SELECTOR, "div[class*='TokenProfileCard_description__']").text
        link = token.find_element(By.TAG_NAME, "a").get_attribute("href")
        age = token.find_element(By.CSS_SELECTOR, "div[class*='TokenProfileCard_badge__']").text

        print("🆕 Token:")
        print(f"Name       : {name}")
        print(f"Description: {description}")
        print(f"Age        : {age}")
        print(f"URL        : {link}")
        print("-" * 60)

    except Exception as e:
        print("⚠️ Failed to parse a token:", e)

driver.quit()
