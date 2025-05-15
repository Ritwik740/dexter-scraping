from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta

def parse_age(age_str):
    """Parse age string into minutes"""
    if not age_str:
        return float('inf')
    
    # Strictly match only minutes format (Xm)
    match = re.search(r'^(\d+)\s*m$', age_str.lower())
    if not match:
        return float('inf')
    
    number = int(match.group(1))
    return number

def scrape_dexscreener():
    # Read the HTML file
    with open('test.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Parse HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all anchor tags
    items = []
    for a in soup.find_all('a', href=True):
        # Find age element
        age_elem = a.find(class_=lambda x: x and 'pair-age' in x)
        if not age_elem:
            continue
            
        age_str = age_elem.get_text().strip()
        age_minutes = parse_age(age_str)
        
        # Skip if not in minutes format
        if age_minutes == float('inf'):
            continue
        
        # Get other details
        token_elem = a.find(class_=lambda x: x and 'token' in x)
        price_elem = a.find(class_=lambda x: x and 'price' in x)
        
        token = token_elem.get_text().strip() if token_elem else 'N/A'
        price = price_elem.get_text().strip() if price_elem else 'N/A'
        
        items.append({
            'token': token,
            'price': price,
            'age': age_str,
            'age_minutes': age_minutes,
            'url': a['href']
        })
    
    # Sort by age
    items.sort(key=lambda x: x['age_minutes'])
    
    # Filter and print items less than 50 minutes old
    print("\nItems less than 50 minutes old:")
    print("-" * 80)
    for item in items:
        if item['age_minutes'] < 50:
            print(f"Token: {item['token']}")
            print(f"Price: {item['price']}")
            print(f"Age: {item['age']}")
            print(f"URL: {item['url']}")
            print("-" * 80)

if __name__ == "__main__":
    scrape_dexscreener() 