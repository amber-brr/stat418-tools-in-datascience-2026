# Web Scraping Basics

This example demonstrates web scraping fundamentals using Beautiful Soup and requests, including HTML parsing, CSS selectors, and handling common challenges.

## Overview

Learn how to:
- Fetch and parse HTML
- Use CSS selectors
- Extract text and attributes
- Handle pagination
- Implement rate limiting
- Save scraped data

## Prerequisites

```bash
# Install required packages
uv pip install requests beautifulsoup4 lxml
```

## Setup

Always check `robots.txt` before scraping:
```
https://example.com/robots.txt
```

## Examples

### Example 1: Basic HTML Parsing

```python
import requests
from bs4 import BeautifulSoup

url = 'https://example.com'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find elements
title = soup.find('h1')
print(f"Title: {title.get_text()}")

# Find all paragraphs
paragraphs = soup.find_all('p')
for p in paragraphs:
    print(p.get_text())
```

### Example 2: CSS Selectors

```python
import requests
from bs4 import BeautifulSoup

url = 'https://news.ycombinator.com/'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Select by class
headlines = soup.select('.titleline > a')

print("Top Headlines:")
for i, headline in enumerate(headlines[:10], 1):
    title = headline.get_text()
    link = headline.get('href', '')
    print(f"{i}. {title}")
    if link:
        print(f"   {link}")
```

### Example 3: Extracting Structured Data

```python
import requests
from bs4 import BeautifulSoup

def scrape_article(url):
    """Extract article information"""
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract data (adjust selectors for your target site)
    article = {
        'title': soup.find('h1').get_text() if soup.find('h1') else None,
        'author': None,
        'date': None,
        'content': []
    }
    
    # Find author
    author_elem = soup.find('span', class_='author')
    if author_elem:
        article['author'] = author_elem.get_text()
    
    # Find date
    date_elem = soup.find('time')
    if date_elem:
        article['date'] = date_elem.get('datetime', date_elem.get_text())
    
    # Find content paragraphs
    content_div = soup.find('div', class_='article-content')
    if content_div:
        paragraphs = content_div.find_all('p')
        article['content'] = [p.get_text() for p in paragraphs]
    
    return article

# Usage
article = scrape_article('https://example.com/article')
print(f"Title: {article['title']}")
print(f"Author: {article['author']}")
print(f"Date: {article['date']}")
print(f"Paragraphs: {len(article['content'])}")
```

### Example 4: Handling Pagination

```python
import requests
from bs4 import BeautifulSoup
import time

def scrape_paginated_site(base_url, max_pages=5):
    """Scrape multiple pages"""
    all_items = []
    
    for page in range(1, max_pages + 1):
        url = f"{base_url}?page={page}"
        print(f"Scraping page {page}...")
        
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract items (adjust selector for your site)
        items = soup.find_all('div', class_='item')
        
        for item in items:
            title = item.find('h2')
            link = item.find('a')
            
            if title and link:
                all_items.append({
                    'title': title.get_text().strip(),
                    'url': link.get('href')
                })
        
        # Be polite - wait between requests
        time.sleep(1)
    
    return all_items

# Usage
items = scrape_paginated_site('https://example.com/articles', max_pages=3)
print(f"Scraped {len(items)} items")
```

### Example 5: Rate-Limited Scraper

```python
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

class RateLimitedScraper:
    def __init__(self, delay=1.0):
        self.delay = delay
        self.last_request = 0
    
    def fetch(self, url):
        """Fetch URL with rate limiting"""
        # Wait if necessary
        elapsed = time.time() - self.last_request
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        
        # Make request
        print(f"[{datetime.now():%H:%M:%S}] Fetching {url}")
        self.last_request = time.time()
        
        response = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Educational Scraper)'
        })
        return response
    
    def parse(self, response):
        """Parse HTML response"""
        return BeautifulSoup(response.content, 'html.parser')

# Usage
scraper = RateLimitedScraper(delay=2.0)

urls = [
    'https://example.com/page1',
    'https://example.com/page2',
    'https://example.com/page3'
]

for url in urls:
    response = scraper.fetch(url)
    soup = scraper.parse(response)
    # Process soup...
```

### Example 6: Saving Data

```python
import requests
from bs4 import BeautifulSoup
import json
import csv
from datetime import datetime

def scrape_and_save(url, output_format='json'):
    """Scrape data and save to file"""
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract data
    items = []
    for article in soup.find_all('article'):
        title_elem = article.find('h2')
        date_elem = article.find('time')
        
        if title_elem:
            items.append({
                'title': title_elem.get_text().strip(),
                'date': date_elem.get('datetime') if date_elem else None,
                'scraped_at': datetime.now().isoformat()
            })
    
    # Save based on format
    if output_format == 'json':
        with open('scraped_data.json', 'w') as f:
            json.dump(items, f, indent=2)
        print(f"Saved {len(items)} items to scraped_data.json")
    
    elif output_format == 'csv':
        with open('scraped_data.csv', 'w', newline='') as f:
            if items:
                writer = csv.DictWriter(f, fieldnames=items[0].keys())
                writer.writeheader()
                writer.writerows(items)
        print(f"Saved {len(items)} items to scraped_data.csv")
    
    return items

# Usage
items = scrape_and_save('https://example.com/articles', output_format='json')
```

## Complete Example: News Aggregator

```python
import requests
from bs4 import BeautifulSoup
import time
import json
from datetime import datetime
from typing import List, Dict

class NewsAggregator:
    def __init__(self, delay=2.0):
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Educational News Aggregator)'
        })
    
    def fetch_page(self, url: str) -> BeautifulSoup:
        """Fetch and parse a page"""
        time.sleep(self.delay)
        response = self.session.get(url, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    
    def scrape_hacker_news(self) -> List[Dict]:
        """Scrape Hacker News front page"""
        print("Scraping Hacker News...")
        soup = self.fetch_page('https://news.ycombinator.com/')
        
        articles = []
        for item in soup.select('.athing')[:10]:
            title_elem = item.select_one('.titleline > a')
            if title_elem:
                articles.append({
                    'source': 'Hacker News',
                    'title': title_elem.get_text(),
                    'url': title_elem.get('href', ''),
                    'scraped_at': datetime.now().isoformat()
                })
        
        return articles
    
    def scrape_multiple_sources(self) -> List[Dict]:
        """Scrape multiple news sources"""
        all_articles = []
        
        # Add more sources as needed
        sources = [
            ('Hacker News', self.scrape_hacker_news),
        ]
        
        for source_name, scraper_func in sources:
            try:
                articles = scraper_func()
                all_articles.extend(articles)
                print(f"  Scraped {len(articles)} articles from {source_name}")
            except Exception as e:
                print(f"  Error scraping {source_name}: {e}")
        
        return all_articles
    
    def save_results(self, articles: List[Dict], filename='news_aggregation.json'):
        """Save scraped articles"""
        data = {
            'scraped_at': datetime.now().isoformat(),
            'total_articles': len(articles),
            'articles': articles
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"\nSaved {len(articles)} articles to {filename}")

# Usage
if __name__ == '__main__':
    aggregator = NewsAggregator(delay=2.0)
    articles = aggregator.scrape_multiple_sources()
    aggregator.save_results(articles)
    
    # Display summary
    print("\nTop Headlines:")
    for i, article in enumerate(articles[:5], 1):
        print(f"{i}. {article['title']}")
        print(f"   Source: {article['source']}")
```

## Handling Common Challenges

### Missing Elements

```python
from bs4 import BeautifulSoup

def safe_extract(soup, selector, attribute=None):
    """Safely extract data with fallback"""
    element = soup.select_one(selector)
    if element:
        if attribute:
            return element.get(attribute, '')
        return element.get_text().strip()
    return None

# Usage
title = safe_extract(soup, 'h1.title')
link = safe_extract(soup, 'a.read-more', 'href')
```

### Cleaning Text

```python
import re

def clean_text(text):
    """Clean scraped text"""
    if not text:
        return ''
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Remove special characters if needed
    text = re.sub(r'[^\w\s\-.,!?]', '', text)
    
    return text.strip()

# Usage
raw_text = soup.find('p').get_text()
clean = clean_text(raw_text)
```

### Handling Relative URLs

```python
from urllib.parse import urljoin

base_url = 'https://example.com'
relative_url = '/articles/123'

# Convert to absolute URL
absolute_url = urljoin(base_url, relative_url)
print(absolute_url)  # https://example.com/articles/123
```

## Best Practices

1. **Check robots.txt**: Always respect site rules
2. **Rate limit**: Add delays between requests (1-2 seconds minimum)
3. **User-Agent**: Identify your scraper
4. **Error handling**: Expect and handle failures
5. **Save incrementally**: Don't lose data if scraper crashes
6. **Validate data**: Check for None/missing values
7. **Log activity**: Track what you've scraped

## Common Issues

**Issue**: `AttributeError: 'NoneType' object has no attribute 'get_text'`
- **Solution**: Check if element exists before accessing: `if elem: text = elem.get_text()`

**Issue**: Empty results
- **Solution**: Inspect HTML in browser, verify selectors are correct

**Issue**: `403 Forbidden` or `429 Too Many Requests`
- **Solution**: Add User-Agent header, increase delays, respect rate limits

**Issue**: Inconsistent data
- **Solution**: Add validation, handle missing fields gracefully

## Ethical Considerations

- ✅ **DO**: Check robots.txt
- ✅ **DO**: Rate limit your requests
- ✅ **DO**: Identify your scraper
- ✅ **DO**: Respect copyright
- ❌ **DON'T**: Overload servers
- ❌ **DON'T**: Scrape personal data
- ❌ **DON'T**: Ignore Terms of Service
- ❌ **DON'T**: Scrape behind logins without permission

## Resources

- [Beautiful Soup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [CSS Selectors Reference](https://www.w3schools.com/cssref/css_selectors.asp)
- [Requests Documentation](https://docs.python-requests.org/)
- [Web Scraping Best Practices](https://www.scrapehero.com/web-scraping-best-practices/)

## Next Steps

- Try scraping different websites
- Learn about Selenium for dynamic content
- Explore Scrapy framework
- Build a data collection pipeline
- Practice with the assignment