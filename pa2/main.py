import re
from lxml import etree
from bs4 import BeautifulSoup
from difflib import SequenceMatcher
from sklearn.cluster import AgglomerativeClustering
import numpy as np

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


# extract_rtv_regex(open("./pa2/webpages/rtvslo.si/rtvslo-2.html", "r"))
# extract_overstock_regex(open("./pa2/webpages/overstock.com/jewelry02.html", "r", encoding="latin-1"))
# extract_24ur_regex(open("./pa2/webpages/24ur.com/novica2.html", "r"))
# extract_kosarka_regex(open("./pa2/webpages/kosarka.si/novica2.html", "r"))


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


# extract_rtv_xpath(open("./pa2/webpages/rtvslo.si/rtvslo-1.html", "r"))
# extract_overstock_xpath(open("./pa2/webpages/overstock.com/jewelry01.html", "r", encoding="latin-1"))
# extract_24ur_xpath(open("./pa2/webpages/24ur.com/novica2.html", "r"))
# extract_kosarka_xpath(open("./pa2/webpages/kosarka.si/novica2.html", "r"))


# PART 3
def parse_html(file_path, encoding):
    with open(file_path, "r", encoding=encoding) as f:
        soup = BeautifulSoup(f, 'html.parser')

    # Extract relevant HTML block elements (e.g., <p>, <div>, <h1>, <title>)
    layout_blocks = [tag.name for tag in soup.find_all(['p', 'div', 'h1', 'title'])]
    return layout_blocks


def compute_similarity(page1_blocks, page2_blocks):
    # Calculate the similarity between two pages based on the edit distance of their layout block sequences
    return SequenceMatcher(None, page1_blocks, page2_blocks).ratio()


def pairwise_similarity(layout_blocks):
    n = len(layout_blocks)
    similarities = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            similarities[i, j] = compute_similarity(layout_blocks[i], layout_blocks[j])
    return similarities


def cluster_pages(similarities, threshold):
    # Group pages with similar layouts into clusters using hierarchical clustering
    clustering = AgglomerativeClustering(n_clusters=None, distance_threshold=threshold, linkage='average').fit(similarities)
    return clustering.labels_


def generate_layout_patterns(clusters, pages):
    layout_patterns = []
    for cluster_id in set(clusters):
        cluster_pages = [page for i, page in enumerate(pages) if clusters[i] == cluster_id]
        # Extract common layout blocks shared by the pages in the cluster
        common_blocks = set.intersection(*map(set, cluster_pages))
        layout_patterns.append(common_blocks)
    return layout_patterns


def remove_static_parts(layout_patterns):
    # Identify and remove static parts like banners and navigation links from the layout patterns
    # Use a threshold-based approach to determine which parts to remove
    filtered_patterns = []
    for pattern in layout_patterns:
        # Implement your logic to filter out static parts based on thresholds
        filtered_patterns.append(pattern)
    return filtered_patterns


def discover_title_and_main_text(layout_patterns):
    titles = []
    main_texts = []
    for pattern in layout_patterns:
        # Implement logic to identify title and main text blocks
        # For example, find the block with the most common words or the largest block as title
        title = max(pattern, key=len)
        main_text = max(pattern, key=lambda x: len(x) if x != title else 0)
        titles.append(title)
        main_texts.append(main_text)
    return titles, main_texts


def extract_texts(html_content, layout_patterns):
    extracted_texts = []
    for pattern in layout_patterns:
        title_block = None
        main_text_blocks = []

        # Discover title block
        for block in pattern:
            if block.startswith('h') or block == 'title':
                title_block = block
                break

        # Discover main text blocks
        for block in pattern:
            if block != title_block:
                main_text_blocks.append(block)

        extracted_texts.append({'main_text': main_text_blocks, 'title': title_block})

    return extracted_texts


def webstemmer(filename, encoding):
    # Step 1: Parse HTML Pages
    layout_blocks = parse_html(filename, encoding)

    # Step 2: Compute Similarity
    similarities = pairwise_similarity(layout_blocks)

    # Step 3: Clustering
    threshold = 0.5  # Adjust the threshold as needed
    clusters = cluster_pages(similarities, threshold)

    # Step 4: Generate Layout Patterns
    layout_patterns = generate_layout_patterns(clusters, layout_blocks)

    # Step 5: Remove Banners and Navigation Links
    layout_patterns = remove_static_parts(layout_patterns)

    # Step 6: Discover Title and Main Text
    titles, main_texts = discover_title_and_main_text(layout_patterns)

    # Step 7: Extract Texts
    extracted_texts = extract_texts(filename, layout_patterns)

    # Output extracted texts
    for text in extracted_texts:
        print(text)


# webstemmer("./webpages/rtvslo.si/rtvslo-2.html", "utf-8")
# webstemmer("./webpages/overstock.com/jewelry02.html", "latin-1")
# webstemmer("./webpages/24ur.com/novica2.html", "utf-8")
# webstemmer("./webpages/kosarka.si/novica2.html", "utf-8")