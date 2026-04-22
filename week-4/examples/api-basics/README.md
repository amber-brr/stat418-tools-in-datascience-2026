# API Basics

This example demonstrates fundamental API usage with the `requests` library, including authentication, error handling, and data processing.

## Overview

Learn how to:
- Make GET and POST requests
- Handle API authentication
- Process JSON responses
- Implement error handling
- Respect rate limits

## Prerequisites

```bash
# Install required packages
uv pip install requests python-dotenv
```

## Setup

1. Create a `.env` file with your API keys:
```bash
GITHUB_TOKEN=your_github_token_here
OPENWEATHER_API_KEY=your_openweather_key_here
```

2. Never commit `.env` files to Git!

## Examples

### Example 1: Simple GET Request

```python
import requests

# Public API - no authentication needed
url = 'https://api.github.com/repos/python/cpython'
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print(f"Repository: {data['name']}")
    print(f"Stars: {data['stargazers_count']}")
    print(f"Forks: {data['forks_count']}")
else:
    print(f"Error: {response.status_code}")
```

### Example 2: Authenticated Request

```python
import requests
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('GITHUB_TOKEN')
headers = {'Authorization': f'token {token}'}

url = 'https://api.github.com/user/repos'
response = requests.get(url, headers=headers)

if response.status_code == 200:
    repos = response.json()
    for repo in repos[:5]:
        print(f"- {repo['name']}")
```

### Example 3: Query Parameters

```python
import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('OPENWEATHER_API_KEY')
base_url = 'http://api.openweathermap.org/data/2.5/weather'

params = {
    'q': 'Los Angeles',
    'appid': api_key,
    'units': 'imperial'
}

response = requests.get(base_url, params=params)
data = response.json()

print(f"Temperature: {data['main']['temp']}°F")
print(f"Conditions: {data['weather'][0]['description']}")
print(f"Humidity: {data['main']['humidity']}%")
```

### Example 4: Error Handling

```python
import requests
from requests.exceptions import RequestException
import time

def fetch_with_retry(url, max_retries=3):
    """Fetch URL with exponential backoff retry"""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            if attempt == max_retries - 1:
                print(f"Failed after {max_retries} attempts: {e}")
                raise
            wait_time = 2 ** attempt
            print(f"Attempt {attempt + 1} failed, retrying in {wait_time}s...")
            time.sleep(wait_time)
    return None

# Usage
try:
    data = fetch_with_retry('https://api.github.com/repos/python/cpython')
    print(f"Success! Stars: {data['stargazers_count']}")
except RequestException:
    print("Failed to fetch data")
```

### Example 5: Rate Limiting

```python
import requests
import time
from datetime import datetime

class RateLimitedAPI:
    def __init__(self, calls_per_minute=10):
        self.calls_per_minute = calls_per_minute
        self.min_interval = 60.0 / calls_per_minute
        self.last_call = 0
    
    def get(self, url, **kwargs):
        """Make rate-limited GET request"""
        # Wait if necessary
        elapsed = time.time() - self.last_call
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        
        # Make request
        self.last_call = time.time()
        print(f"[{datetime.now():%H:%M:%S}] Fetching {url}")
        return requests.get(url, **kwargs)

# Usage
api = RateLimitedAPI(calls_per_minute=10)

urls = [
    'https://api.github.com/repos/python/cpython',
    'https://api.github.com/repos/python/mypy',
    'https://api.github.com/repos/python/typing',
]

for url in urls:
    response = api.get(url)
    data = response.json()
    print(f"  {data['name']}: {data['stargazers_count']} stars")
```

### Example 6: POST Request

```python
import requests
import json

# Example using JSONPlaceholder test API
url = 'https://jsonplaceholder.typicode.com/posts'

data = {
    'title': 'My Data Science Project',
    'body': 'Analysis of API usage patterns',
    'userId': 1
}

response = requests.post(url, json=data)

if response.status_code == 201:
    created = response.json()
    print(f"Created post with ID: {created['id']}")
    print(json.dumps(created, indent=2))
```

## Complete Example: GitHub Repository Analyzer

```python
import requests
import os
from dotenv import load_dotenv
from datetime import datetime
import json

load_dotenv()

class GitHubAnalyzer:
    def __init__(self):
        self.token = os.getenv('GITHUB_TOKEN')
        self.headers = {'Authorization': f'token {self.token}'}
        self.base_url = 'https://api.github.com'
    
    def get_repo_info(self, owner, repo):
        """Get repository information"""
        url = f"{self.base_url}/repos/{owner}/{repo}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_recent_commits(self, owner, repo, count=5):
        """Get recent commits"""
        url = f"{self.base_url}/repos/{owner}/{repo}/commits"
        params = {'per_page': count}
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def analyze_repository(self, owner, repo):
        """Complete repository analysis"""
        print(f"\nAnalyzing {owner}/{repo}...")
        
        # Get repo info
        repo_data = self.get_repo_info(owner, repo)
        
        # Get recent commits
        commits = self.get_recent_commits(owner, repo)
        
        # Compile analysis
        analysis = {
            'name': repo_data['name'],
            'description': repo_data['description'],
            'stars': repo_data['stargazers_count'],
            'forks': repo_data['forks_count'],
            'language': repo_data['language'],
            'created': repo_data['created_at'],
            'updated': repo_data['updated_at'],
            'recent_commits': len(commits),
            'last_commit': commits[0]['commit']['author']['date'] if commits else None
        }
        
        return analysis

# Usage
if __name__ == '__main__':
    analyzer = GitHubAnalyzer()
    
    repos = [
        ('python', 'cpython'),
        ('pandas-dev', 'pandas'),
        ('scikit-learn', 'scikit-learn')
    ]
    
    results = []
    for owner, repo in repos:
        try:
            analysis = analyzer.analyze_repository(owner, repo)
            results.append(analysis)
            
            print(f"  Stars: {analysis['stars']:,}")
            print(f"  Language: {analysis['language']}")
            print(f"  Last commit: {analysis['last_commit']}")
        except Exception as e:
            print(f"  Error: {e}")
    
    # Save results
    with open('github_analysis.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nAnalysis saved to github_analysis.json")
```

## Free APIs for Practice

- **GitHub API**: https://api.github.com (no key needed for basic use)
- **JSONPlaceholder**: https://jsonplaceholder.typicode.com (test API)
- **REST Countries**: https://restcountries.com/v3.1/all
- **OpenWeatherMap**: https://openweathermap.org/api (free tier)
- **NASA APIs**: https://api.nasa.gov (free with API key)
- **The Movie Database**: https://www.themoviedb.org/settings/api

## Best Practices

1. **Always handle errors**: Use try/except blocks
2. **Respect rate limits**: Add delays between requests
3. **Use environment variables**: Never hardcode API keys
4. **Check status codes**: Don't assume success
5. **Log requests**: Help with debugging
6. **Cache responses**: Avoid unnecessary API calls
7. **Read the docs**: Each API is different

## Common Issues

**Issue**: `401 Unauthorized`
- **Solution**: Check your API key/token is correct and not expired

**Issue**: `429 Too Many Requests`
- **Solution**: You're hitting rate limits. Add delays between requests

**Issue**: `timeout` errors
- **Solution**: Increase timeout value or check your internet connection

**Issue**: `KeyError` when accessing response data
- **Solution**: Check the response structure first with `print(response.json())`

## Resources

- [Requests Documentation](https://docs.python-requests.org/)
- [HTTP Status Codes](https://httpstatuses.com/)
- [Public APIs List](https://github.com/public-apis/public-apis)
- [REST API Tutorial](https://restfulapi.net/)

## Next Steps

- Try the web scraping examples
- Build your own API client
- Explore async requests with `httpx`
- Learn about GraphQL APIs