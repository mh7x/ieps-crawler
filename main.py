import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin, urlparse
import hashlib
import psycopg2
import threading

# Function to retrieve and parse HTML content using requests
def fetch_html(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    return None

# Function to extract links from HTML content
def extract_links(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    links = set()
    for link in soup.find_all('a', href=True):
        href = link.get('href')
        if href.startswith('http') or href.startswith('https'):
            links.add(href)
        else:
            links.add(urljoin(base_url, href))
    return links

# Function to respect crawl delay
def respect_crawl_delay(domain, delay=5):
    current_time = time.time()
    last_access_time = last_access_times.get(domain, 0)
    if current_time - last_access_time < delay:
        time.sleep(delay - (current_time - last_access_time))
    last_access_times[domain] = time.time()

# Function to canonicalize URLs
def canonicalize_url(url):
    return hashlib.sha256(url.encode()).hexdigest()

# Function to crawl a single URL
def crawl_url(url):
    html = fetch_html(url)
    if html:
        # Store canonicalized URL
        canonical_url = canonicalize_url(url)
        # Check for duplicate content
        if not is_duplicate(html):
            # Extract links
            links = extract_links(html, url)
            for link in links:
                frontier.append(link)
            # Store data in the database
            store_data(canonical_url, html)

# Function to check for duplicate content
def is_duplicate(html):
    # Check if the hash of the HTML content already exists in the database
    html_hash = hashlib.sha256(html.encode()).hexdigest()
    cur.execute("SELECT * FROM crawldb.page WHERE html_content_hash = %s", (html_hash,))
    return cur.fetchone() is not None

# Function to store data in the database
def store_data(canonical_url, html):
    html_hash = hashlib.sha256(html.encode()).hexdigest()
    cur.execute("INSERT INTO crawldb.page (site_id, page_type_code, url, html_content_hash, html_content) VALUES (%s, %s, %s, %s, %s) RETURNING id",
                (1, 'HTML', canonical_url, html_hash, html))
    page_id = cur.fetchone()[0]  # Get the inserted page ID
    conn.commit()

    # Store HTML content in page_data table
    cur.execute("INSERT INTO crawldb.page_data (page_id, data_type_code, data) VALUES (%s, %s, %s)",
                (page_id, 'HTML', html.encode()))
    conn.commit()

# Function to perform crawling with multi-threading
def crawl_with_threads(seed_urls, num_workers):
    global frontier
    frontier = seed_urls.copy()
    threads = []
    for _ in range(num_workers):
        t = threading.Thread(target=worker)
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

# Worker function for each thread
def worker():
    while True:
        url = None
        # Ensure thread safety while accessing shared frontier
        with lock:
            if frontier:
                url = frontier.pop(0)
        if url:
            domain = urlparse(url).netloc
            respect_crawl_delay(domain)
            crawl_url(url)
        else:
            break

# Initialize database connection
conn = psycopg2.connect(database="postgres", user="postgres.guoimnempzxzidvwjnem", password="IepsCrawler12!!",
                        host="aws-0-eu-west-2.pooler.supabase.com", port="5432")

cur = conn.cursor()

# Seed URLs
seed_urls = [
    'https://gov.si',
    'https://evem.gov.si',
    'https://e-uprava.gov.si',
    'https://e-prostor.gov.si'
]

# Number of workers (threads)
num_workers = 4

# Global variable to store last access times for domains
last_access_times = {}
# Lock for thread safety
lock = threading.Lock()

# Start crawling with multi-threading
crawl_with_threads(seed_urls, num_workers)