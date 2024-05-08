import re
from lxml import etree
from bs4 import BeautifulSoup
from difflib import SequenceMatcher

# Regex extractions
def extract_rtv_regex(html_file):
    html_content = html_file.read()

    title_match = re.search(re.compile(r'(?<=<h1>)(.*?)(?=<\/h1>)'), html_content)
    title = title_match.group(0).strip()

    author_match = re.search(re.compile(r'(?<=\<div class="author-name"\>).*?(?=\<\/div\>)', re.DOTALL), html_content)
    author = author_match.group(0).strip()
    
    published_time_match = re.search(re.compile(r'(?<=\<div class="publish-meta"\>).*?(?=\<\/div\>)', re.DOTALL), html_content)
    published_time = published_time_match.group(0).strip()
    published_time = " ".join(published_time.split())

    subtitle_match = re.search(re.compile(r'(?<=\<div class="subtitle"\>).*?(?=\<\/div\>)', re.DOTALL), html_content)
    subtitle = subtitle_match.group(0).strip()

    lead_match = re.search(re.compile(r'(?<=\<p class="lead"\>).*?(?=\<\/p\>)', re.DOTALL), html_content)    
    lead = lead_match.group(0).strip()

    body_paragraphs = re.findall(r'<p class="Body">(.*?)</p>', html_content, re.DOTALL)
    content = ""
    for paragraph in body_paragraphs:
        content += paragraph.strip()
    content = re.sub(r'<.*?>', '', content)

    data = {
        "Title": title,
        "Author": author,
        "Published time": published_time,
        "Subtitle": subtitle,
        "Lead": lead,
        "Content": content,
    }

    print(data)


def extract_overstock_regex(html_file):
    html_content = html_file.read()

    title_matches = re.findall(r'<td valign="top">\s*<a href=".*?"><b>(.*?)</b></a><br>', html_content, re.DOTALL)
    listPrice_matches = re.findall(r'<td align="right" nowrap="nowrap"><b>List Price:</b></td>\s*<td align="left" nowrap="nowrap"><s>(.*?)</s></td>', html_content, re.DOTALL)
    price_matches = re.findall(r'<td align="right" nowrap="nowrap"><b>Price:</b></td>\s*<td align="left" nowrap="nowrap"><span class="bigred"><b>(.*?)</b></span></td>', html_content, re.DOTALL)
    savings_matches = re.findall(r'<td align="right" nowrap="nowrap"><b>You Save:</b></td>\s*<td align="left" nowrap="nowrap"><span class="littleorange">(\$[\d,.]+)', html_content, re.DOTALL)
    savingPercent_matches = re.findall(r'\((\d+%)\)', html_content, re.DOTALL)
    content_matches = re.findall(r'<span class="normal">(.*?)<br>', html_content, re.DOTALL)

    data = {
        "Titles": title_matches,
        "List prices": listPrice_matches,
        "Prices": price_matches,
        "Savings": savings_matches,
        "Saving percents": savingPercent_matches,
        "Contents": content_matches,
    }

    print(data)


def extract_24ur_regex(html_file):
    html_content = html_file.read()

    title_match = re.search(re.compile(r'<h1 class=".*?">(.*?)</h1>'), html_content)
    title = title_match.group(1).strip()

    author_match = re.search(re.compile(r'<div class="text-14 font-semibold text-black/80 dark:text-white/80">(.*?)</div>', re.DOTALL), html_content)
    author = author_match.group(1).strip()
    
    published_time_match = re.search(re.compile(r'<p class="text-black/60 dark:text-white/60 mb-16 leading-caption">(.*?) \|', re.DOTALL), html_content)
    published_time = published_time_match.group(1).strip()

    subtitle_match = re.search(re.compile(r'<div class="summary mb-16 px-0 md:px-article-summary pb-16 md:pb-24 border-b border-black/10 dark:border-white/10">(.*?)</div>', re.DOTALL), html_content)
    subtitle = subtitle_match.group(1).strip()
    subtitle = re.sub(r'<p.*?>(.*?)', '', subtitle, flags=re.DOTALL)
    subtitle = " ".join(subtitle.split())

    body_paragraphs = re.findall(r'<p>(.*?)<p>', html_content, re.DOTALL)
    content = ""
    for paragraph in body_paragraphs:
        content += paragraph.strip()
    content = " ".join(content.split())
    content = re.sub(r'<.*?>', '', content)

    data = {
        "Title": title,
        "Author": author,
        "Published time": published_time,
        "Subtitle": subtitle,
        "Content": content,
    }

    print(data)


def extract_kosarka_regex(html_file):
    html_content = html_file.read()

    title_match = re.search(r'<h1[^>]*>(.*?)<\/h1>', html_content)
    title = title_match.group(1).strip()

    author_match = re.search(re.compile(r'<span class="author-name">(.*?)<\/span>', re.DOTALL), html_content)
    author = author_match.group(1).strip()
    
    published_time_match = re.search(re.compile(r'Objavljeno: (\d{2}\.\d{2}\.\d{4} ob \d{2}:\d{2})', re.DOTALL), html_content)
    published_time = published_time_match.group(1)

    category_match = re.search(re.compile(r'<span><a href=".*?">(.*?)<\/a><\/span>', re.DOTALL), html_content)
    category = category_match.group(1).strip()
    category = re.sub(r'<p.*?>(.*?)', '', category, flags=re.DOTALL)

    body_paragraphs = re.findall(r'<p>(.*?)<p>', html_content, re.DOTALL)
    content = ""
    for paragraph in body_paragraphs:
        content += paragraph.strip()
    content = " ".join(content.split())
    content = re.sub(r'<.*?>', '', content)

    data = {
        "Title": title,
        "Author": author,
        "Published time": published_time,
        "Category": category,
        "Content": content,
    }

    print(data)


# extract_rtv_regex(open("./webpages/rtvslo.si/rtvslo-2.html", "r", encoding="utf-8"))
# extract_overstock_regex(open("./webpages/overstock.com/jewelry02.html", "r", encoding="latin-1"))
# extract_24ur_regex(open("./webpages/24ur.com/novica2.html", "r", encoding="utf-8"))
# extract_kosarka_regex(open("./webpages/kosarka.si/novica2.html", "r", encoding="utf-8"))


# xPath extarctions
def extract_rtv_xpath(html_file):
    html_content = html_file.read()
    root = etree.HTML(html_content)

    title = root.xpath('//h1/text()')
    author = root.xpath('//div[@class="author"]/div[@class="author-name"]/text()')
    published_time = root.xpath('//div[@class="publish-meta"]/text()')
    subtitle = root.xpath('//div[@class="subtitle"]/text()')
    lead = root.xpath('//p[@class="lead"]/text()')
    lead = ''.join(lead)
    content = root.xpath('//p[@class="Body"]/text()')
    content = ''.join(content)

    data = {
        "Title": title[0].strip(),
        "Author": author[0].strip(),
        "Published time": published_time[0].strip(),
        "Subtitle": subtitle[0].strip(),
        "Lead": " ".join(lead.split()),
        "Content": " ".join(content.split()),
    }

    print(data)


def extract_overstock_xpath(html_file):
    html_content = html_file.read()
    root = etree.HTML(html_content)

    title_matches = root.xpath('//td[@valign="top"]/a/b/text()')
    listPrice_matches = root.xpath("//td[.//b[contains(text(), 'List Price:')]]/following-sibling::td[1]/s/text()")
    price_matches = root.xpath("//td[.//b[contains(text(), 'Price:')]]/following-sibling::td[1]/span/b/text()")
    savings_matches = root.xpath('//td/span[@class="littleorange"]/text()')
    content_matches = root.xpath('//td/span[@class="normal"]/text()')

    savings = []
    percents = []
    for temp in savings_matches:
        savings.append(temp.split(" ")[0]) 
        percents.append(temp.split(" ")[1]) 

    data = {
        "Titles": title_matches,
        "List prices": listPrice_matches,
        "Prices": price_matches,
        "Savings": savings,
        "Saving percents": percents,
        "Contents": content_matches,
    }

    print(data)


def extract_24ur_xpath(html_file):
    html_content = html_file.read()
    root = etree.HTML(html_content)

    title = root.xpath('//h1/text()')
    author = root.xpath('//div[@class="text-14 font-semibold text-black/80 dark:text-white/80"]/text()')
    published_time = root.xpath('//p[@class="text-black/60 dark:text-white/60 mb-16 leading-caption"]/text()')
    subtitle = root.xpath('normalize-space(//p[@class="text-article-summary font-semibold leading-tight text-black dark:text-white"])')
    content = root.xpath('normalize-space(string(//div[@class="contextual"]))')

    data = {
        "Title": title[0].strip(),
        "Author": author[0].strip(),
        "Published time": published_time[0].strip(),
        "Subtitle": subtitle,
        "Content": content
    }

    print(data)


def extract_kosarka_xpath(html_file):
    html_content = html_file.read()
    root = etree.HTML(html_content)

    title = root.xpath('//h1/text()')
    author = root.xpath('//span[@class="author-name"]/text()')
    published_time = root.xpath('//time[@class="entry-date"]/text()')
    date = published_time[0].split(" ")[1]
    category = root.xpath('//div[@class="entry-sections"]/span/a/text()')
    content = root.xpath('//div[@class="body-content post-content-wrap"]/p/text()')

    content = ''.join(content).replace('\t', '')

    data = {
        "Title": title[0],
        "Author": author[0],
        "Published time": date,
        "Category": category[0],
        "Content": " ".join(content.split())
    }

    print(data)


# extract_rtv_xpath(open("./webpages/rtvslo.si/rtvslo-1.html", "r", encoding="utf-8"))
# extract_overstock_xpath(open("./webpages/overstock.com/jewelry01.html", "r", encoding="latin-1"))
# extract_24ur_xpath(open("./webpages/24ur.com/novica2.html", "r", encoding="utf-8"))
# extract_kosarka_xpath(open("./webpages/kosarka.si/novica2.html", "r", encoding="utf-8"))


# PART 3
def parse_html(file_name, encoding):
    # Extract text from HTML file by removing tags
    with open(file_name, 'r', encoding=encoding) as file:
        html_content = file.read()
        return html_content


def extract_layout_blocks(html_content):
    # Extract layout blocks from HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    # Consider relevant elements such as div, p, title, etc.
    relevant_tags = ['div', 'p', 'title', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
    layout_blocks = []
    for tag in relevant_tags:
        elements = soup.find_all(tag)
        layout_blocks.extend([(tag, element.get_text()) for element in elements])
    return layout_blocks



def compute_similarity(block1, block2):
    # Compute similarity between two layout blocks using edit distance
    # Here, we use difflib's SequenceMatcher to compute similarity ratio
    return SequenceMatcher(None, block1, block2).ratio()

def cluster_pages(pages):
    clusters = []
    for page in pages:
        found_cluster = False
        for cluster in clusters:
            # Compute similarity with pages in the cluster
            similarities = [compute_similarity(page, p) for p in cluster]
            avg_similarity = sum(similarities) / len(similarities)
            if avg_similarity > 0.7:  # Adjust threshold as needed
                cluster.append(page)
                found_cluster = True
                break
        if not found_cluster:
            clusters.append([page])
    return clusters


def generate_wrapper(cluster):
    # Generate a human-readable wrapper based on a cluster of layout blocks
    wrapper = {}
    for i, (tag, block) in enumerate(cluster, start=1):
        wrapper[f'{tag}'] = {
            'Text': block,
        }
    return wrapper


def webstemmer(file1, encoding1, file2, encoding2):
    # Parse HTML files and extract layout blocks
    text_page1 = parse_html(file1, encoding1)
    text_page2 = parse_html(file2, encoding2)
    blocks_page1 = extract_layout_blocks(text_page1)
    blocks_page2 = extract_layout_blocks(text_page2)

    # Combine text and layout blocks for clustering
    pages = blocks_page1 + blocks_page2

    # Cluster pages based on layout structure
    clusters = cluster_pages(pages)

    # Print clusters
    for i, cluster in enumerate(clusters):
        # Generate wrapper for the cluster
        wrapper = generate_wrapper(cluster)
        print(f"Wrapper {i}:")
        print(wrapper)

webstemmer("./webpages/rtvslo.si/rtvslo-1.html", "utf-8", "./webpages/rtvslo.si/rtvslo-2.html", "utf-8")