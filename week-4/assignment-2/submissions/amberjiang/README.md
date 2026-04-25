# Assignment 2: Movie Data Collection & Analysis Pipeline

## Overview

Build a data collection pipeline that combines API integration and web scraping to gather movie and TV show data. Data is collected from The Movie Database (TMDB) API and additional information from IMDb is scraped to analyze trends in the entertainment industry.

## Description

Collected data for **at least 50 movies or TV shows** including:

**From TMDB API:**
- Title, release date, runtime
- Genres
- Budget and revenue (for movies)
- TMDB rating and vote count
- Cast and crew (top 5)
- Production companies
- Original language

**From IMDb (via scraping):**
- IMDb rating
- Number of user reviews
- Metascore (if available)

### Part 1: API Integration

`api_collector.py` that:
1. Authenticates with TMDB API
2. Fetches popular movies/shows
3. Gets detailed information for each item
4. Retrieves cast and crew data
5. Implements rate limiting (40 requests per 10 seconds for TMDB)
6. Handles API errors with retry logic
7. Saves raw API responses to JSON files
8. Logs all API calls with timestamps

**Key Functions:**
```python
def get_popular_movies(page: int = 1) -> List[Dict]
def get_movie_details(movie_id: int) -> Dict
def get_movie_credits(movie_id: int) -> Dict
def collect_all_data(num_items: int = 50) -> List[Dict]
```

### Part 2: Web Scraping

`web_scraper.py` that:
1. Checks IMDb's robots.txt
2. Scrapes movie pages for ratings and review counts
3. Implements rate limiting (minimum 2 seconds between requests)
4. Uses appropriate User-Agent header
5. Handles missing data gracefully
6. Saves scraped data to JSON files
7. Logs all scraping activity

**Key Functions:**
```python
def check_robots_txt() -> bool
def scrape_movie_page(imdb_id: str) -> Dict
def scrape_multiple_movies(imdb_ids: List[str]) -> List[Dict]
```

**Note:** Focus on getting basic ratings and counts. Don't worry about extracting review text for this assignment.

### Part 3: Data Processing

`data_processor.py`:
1. Loads data from both sources
2. Merges data on common identifiers (IMDb ID)
3. Cleans and validates data
4. Handles missing values appropriately
5. Standardizes formats (dates, ratings)
6. Removes duplicates
7. Saves processed data as CSV and JSON

**Key Functions:**
```python
def load_raw_data() -> Tuple[List[Dict], List[Dict]]
def merge_data(tmdb_data: List[Dict], imdb_data: List[Dict]) -> pd.DataFrame
def clean_data(df: pd.DataFrame) -> pd.DataFrame
def save_processed_data(df: pd.DataFrame, output_dir: str)
```

### Part 4: Analysis

`analyze_data.py` that:

Answers: 
1. **Rating Analysis:**
   - What's the correlation between TMDB and IMDb ratings?
   - Distribution of ratings on each platform

2. **Genre Analysis:**
   - Most common genres
   - Average ratings by genre

3. **Temporal Analysis:**
   - Rating trends over time
   - Most productive years

Generates:
1. **4 Visualizations:** 
    - TMDB and IMDb distributions side by side
    - TMDB vs IMDb rating scatter plot
    - Most common genres bar plot
    - Average TMDB and IMDb ratings by year line plot
2: **Summary report of rating, genre, and temporal analysis**

### Part 5: Documentation

#### **Setup Instructions**

1. Get TMDB API Key:
    1. Create account at https://www.themoviedb.org/
    2. Go to Settings → API
    3. Request API key (free)
    4. Copy your API key

2. Create .env File:
```bash
# .env
TMDB_API_KEY=your_api_key_here
```

3. Create .env.example:
**Never commit .env to Git!**
```bash
# .env.example
TMDB_API_KEY=your_tmdb_api_key_here
```

#### **How to run the pipeline:**

1. Collect TMDB data -> data/raw/tmdb/tmdb_movie_data
```bash
python api_collector.py  
```

2. Scrape IMDb ratings -> data/raw/imdb/imdb_scraped_data.json
```bash
python web_scraper.py        
```

3. Merge and clean data -> data/processed/
```bash
python data_processor.py
```

4. Analyze and generate visualizations/summary report -> data/analysis/
```bash
python analyze_data.py    
```

#### **Dependencies and requirements:**
`requirements.txt`:
```
requests>=2.31.0
beautifulsoup4>=4.12.0
lxml>=4.9.0
pandas>=2.0.0
python-dotenv>=1.0.0
matplotlib>=3.7.0
seaborn>=0.12.0
```

Install with uv:
```bash
uv pip install -r requirements.txt
```
#### **Data sources and collection methods:**

**TMDB API (`api_collector.py`):**
- Authenticates via API key loaded from `.env`
- Fetches popular movies from `/movie/popular` (paginated) and collects 50 by default
- For each movie, retrieves full details from `/movie/{id}` (title, release date, runtime, genres, budget, revenue, ratings) and cast/crew from `/movie/{id}/credits`
- Rate-limited to 4 requests/second (well within TMDB's 40 requests/10 seconds limit)
- Saves raw responses to `data/raw/tmdb/tmdb_movie_data.json`

**IMDb web scraping (`web_scraper.py`):**
- Checks `robots.txt` before any scraping
- Resolves IMDb IDs from `tmdb_movie_data.json` (TMDB movie details include `imdb_id`)
- Scrapes each movie's IMDb title page (`https://www.imdb.com/title/{imdb_id}/`)
- Extracts IMDb rating and review count from `application/ld+json` structured data; metascore from the embedded `__NEXT_DATA__` JSON
- Rate-limited to a minimum of 2 seconds between requests
- Saves scraped records to `data/raw/imdb/imdb_scraped_data.json`

#### **Ethical considerations:**
**Did:**
- ✅ Check robots.txt before scraping IMDb
- ✅ Implement rate limiting (2+ seconds between requests)
- ✅ Use descriptive User-Agent: "UCLA STAT418 Student - amberjiang@g.ucla.edu"
- ✅ Respect TMDB API rate limits (40 requests per 10 seconds)
- ✅ Handle errors gracefully
- ✅ Document all data sources

**Did Not Do:**
- ❌ Overload servers with rapid requests
- ❌ Scrape personal user data
- ❌ Ignore robots.txt directives
- ❌ Use data for commercial purposes
- ❌ Share or sell collected data

#### **Known limitations:**

- **IMDb scraping fragility:** IMDb rating and metascore extraction depends on the structure of embedded JSON (`ld+json` and `__NEXT_DATA__`). If IMDb changes their page layout, the parser will silently return `None` for those fields.
- **robots.txt blocking:** IMDb's `robots.txt` may disallow scraping for the User-Agent used. If so, all IMDb records will be skipped and the merged dataset will have no IMDb ratings.
- **Missing budget/revenue:** TMDB reports budget and revenue as `0` for movies where this data is not public; these are treated as missing values during processing.
- **Metascore availability:** Metascore is only present for a subset of movies on IMDb; expect a high proportion of `None` values in that column.
- **Popularity bias:** Data is sourced from TMDB's "popular" endpoint, so the dataset reflects currently trending movies rather than a broad or historical sample.
- **No TV show support:** The pipeline is scoped to movies only; extending to TV shows would require separate TMDB endpoints and different IMDb page structures.

#### **REPORT.md**
1. Data collection summary (how much data, from where)
2. Analysis findings with visualizations
3. Interesting insights or patterns
4. Challenges encountered and solutions
5. Limitations and future improvements

## Technical Elements

### Directory Structure
```
week-4/assignment-2/submissions/yourname/
├── README.md
├── REPORT.md
├── requirements.txt
├── .env.example
├── api_collector.py
├── web_scraper.py
├── data_processor.py
├── analyze_data.py
├── run_pipeline.py
├── data/
│   ├── raw/
│   │   ├── tmdb/
│   │   └── imdb/
│   ├── processed/
│   └── analysis/
└── logs/
    └── pipeline.log
```

### Code Quality
- Type hints for function signatures
- Docstrings for all functions and classes
- PEP 8 style guidelines
- Meaningful variable names
- Proper error handling with try/except
- Logging throughout the pipeline
