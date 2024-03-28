import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin, urlparse
import hashlib
import psycopg2
import io
import PyPDF2
import docx
import pptx
from datetime import datetime
from selenium import webdriver

# Function to retrieve and parse HTML content using requests
def fetch_html(url):
    try:
        print(url)
        options = webdriver.FirefoxOptions()
        options.headless = True
        firefox_options = webdriver.FirefoxOptions()
        driver = webdriver.Firefox(options=firefox_options)
        driver.get(url)
        html = driver.page_source
        status_code = driver.execute_script("return document.readyState")
        driver.quit()
        return (html, status_code)
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
    html, status_code = fetch_html(url)
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
            store_data(canonical_url, html, status_code)
        else:
            store_data(canonical_url, html, status_code)
            from_id = cur.execute("SELECT id FROM page WHERE url = (%s)", canonical_url)
            to_id = cur.execute("SELECT id FROM page WHERE url = (%s)", frontier[0])
            cur.execute("INSERT INTO link (from_page, to_page) VALUES (%s, %s)",
                        (from_id, to_id))
            conn.commit()


# Function to check for duplicate content
def is_duplicate(html):
    # Check if the hash of the HTML content already exists in the database
    html_hash = hashlib.sha256(html.encode()).hexdigest()
    cur.execute("SELECT * FROM page WHERE html_content_hash = %s", (html_hash,))
    return cur.fetchone() is not None


# Function to store data in the database
def store_data(canonical_url, html, status_code):
    page_types = {0: 'HTML', 1: 'BINARY', 2: 'DUPLICATE', 3: 'FRONTIER'}
    html_hash = hashlib.sha256(html.encode()).hexdigest()
    cur.execute("INSERT INTO page (page_type_code, url, html_content_hash, html_content, http_status_code, accessed_time) "
                    "VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
                    (page_types.get(0), canonical_url, html_hash, html, status_code, datetime.now()))
    page_id = cur.fetchone()[0]  # Get the inserted page ID
    conn.commit()

    # Check for specific file extensions in the URL and store them in a separate table
    file_extensions = {'.pdf': 0, '.doc': 1, '.docx': 2, '.ppt': 3, '.pptx': 4}
    for ext, data_type_code in file_extensions.items():
        if ext in canonical_url.lower():  # Check if the URL contains the file extension
            file_type = ext.upper()  # Extract file type
            file_content = None
            if file_type == '.pdf':
                file_content = extract_pdf_content(canonical_url)
            elif file_type in ['.doc', '.docx']:
                file_content = extract_doc_content(canonical_url)
            elif file_type in ['.ppt', '.pptx']:
                file_content = extract_ppt_content(canonical_url)

            # Insert the file content into the page_data table
            if file_content:
                cur.execute("INSERT INTO page_data (page_id, data_type_code, data) VALUES (%s, %s, %s)",
                            (page_id, data_type_code, file_content))
                conn.commit()


# Function to extract content from a PDF file
def extract_pdf_content(url):
    try:
        response = requests.get(url)
        pdf_file = PyPDF2.PdfFileReader(io.BytesIO(response.content))
        text = ""
        for page_num in range(pdf_file.numPages):
            text += pdf_file.getPage(page_num).extractText()
        return text
    except Exception as e:
        print(f"Error extracting PDF content from {url}: {e}")
        return None


# Function to extract content from a DOC or DOCX file
def extract_doc_content(url):
    try:
        response = requests.get(url)
        doc = docx.Document(io.BytesIO(response.content))
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text
        return text
    except Exception as e:
        print(f"Error extracting DOC/DOCX content from {url}: {e}")
        return None


# Function to extract content from a PPT or PPTX file
def extract_ppt_content(url):
    try:
        response = requests.get(url)
        ppt = pptx.Presentation(io.BytesIO(response.content))
        text = ""
        for slide in ppt.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    text += shape.text
        return text
    except Exception as e:
        print(f"Error extracting PPT/PPTX content from {url}: {e}")
        return None


# Function to fetch and parse the robots.txt file
def parse_robots_txt(domain):
    robots_txt_url = urljoin(domain, "/robots.txt")
    try:
        response = requests.get(robots_txt_url)
        if response.status_code == 200:
            return response.text
    except Exception as e:
        print(f"Error fetching {robots_txt_url}: {e}")
    return ""

# Function to parse robots.txt rules
def parse_robots_rules(robots_txt_content):
    rules = {}
    current_user_agent = None
    for line in robots_txt_content.splitlines():
        if line.strip():  # Ignore empty lines
            if line.lower().startswith("user-agent"):
                current_user_agent = line.split(":")[1].strip()
            elif current_user_agent:
                key, value = line.split(":", 1)
                rules.setdefault(current_user_agent, []).append((key.strip(), value.strip()))
    return rules

# Function to check if a URL is allowed to be crawled
def is_allowed_by_robots(url, robots_rules):
    parsed_url = urlparse(url)
    user_agent = "*"
    if "User-agent" in robots_rules:
        user_agent = robots_rules["User-agent"]
    elif "*" in robots_rules:
        user_agent = "*"
    if user_agent in robots_rules:
        for rule_key, rule_value in robots_rules[user_agent]:
            if rule_key.lower() == "allow" and rule_value != "/" and parsed_url.path.startswith(rule_value):
                return True
            elif rule_key.lower() == "disallow" and parsed_url.path.startswith(rule_value):
                return False
    return True


# Function to fetch and parse the sitemap.xml file
def parse_sitemap_xml(domain):
    sitemap_url = urljoin(domain, "/sitemap.xml")
    try:
        response = requests.get(sitemap_url)
        if response.status_code == 200:
            return response.text
    except Exception as e:
        print(f"Error fetching {sitemap_url}: {e}")
    return ""


# Function to save data into the "site" table
def save_site_data(domain, robots_content, sitemap_content):
    try:
        cur.execute("INSERT INTO site (domain, robots_content, sitemap_content) VALUES (%s, %s, %s)",
                   (domain, robots_content, sitemap_content))
        conn.commit()
        print(f"Data for {domain} saved successfully.")
    except Exception as e:
        print(f"Error saving data for {domain}: {e}")



# Worker function for each thread
def crawl():
    while True:
        url = None
        # Ensure thread safety while accessing shared frontier
        if frontier:
            url = frontier[0]
            print("crawling: " + url)
        if url:
            domain = urlparse(url).netloc
            respect_crawl_delay(domain)
            robots = parse_robots_txt(url)
            rules = parse_robots_rules(robots)
            if is_allowed_by_robots(url, rules):
                sitemap = parse_sitemap_xml(url)
                save_site_data(domain, robots, sitemap)
                crawl_url(url)
                frontier.pop(0)
            else:
                frontier.pop(0)
        else:
            break


# Initialize database connection
conn = psycopg2.connect(database="postgres", user="postgres.guoimnempzxzidvwjnem", password="IepsCrawler12!!",
                        host="aws-0-eu-west-2.pooler.supabase.com", port="5432")

cur = conn.cursor()

global frontier
frontier = [
    'https://gov.si',
    'https://evem.gov.si',
    'https://e-uprava.gov.si',
    'https://e-prostor.gov.si'
]

# Global variable to store last access times for domains
global last_access_times
last_access_times = {}

# Start crawling with multi-threading
while len(frontier) != 0:
    crawl()