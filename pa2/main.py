import re


def extract_rtv(html_file):
    html_content = html_file.read()

    title_match = re.search(re.compile(r'(?<=<h1>)(.*?)(?=<\/h1>)'), html_content)
    title = title_match.group(0)
    title = " ".join(title.split())

    author_match = re.search(re.compile(r'(?<=\<div class="author-name"\>).*?(?=\<\/div\>)', re.DOTALL), html_content)
    author = author_match.group(0)
    author = " ".join(author.split())
    
    published_time_match = re.search(re.compile(r'(?<=\<div class="publish-meta"\>).*?(?=\<\/div\>)', re.DOTALL), html_content)
    published_time = published_time_match.group(0)
    published_time = " ".join(published_time.split())

    subtitle_match = re.search(re.compile(r'(?<=\<div class="subtitle"\>).*?(?=\<\/div\>)', re.DOTALL), html_content)
    subtitle = subtitle_match.group(0)
    subtitle = " ".join(subtitle.split())

    lead_match = re.search(re.compile(r'(?<=\<p class="lead"\>).*?(?=\<\/p\>)', re.DOTALL), html_content)    
    lead = lead_match.group(0)
    lead = " ".join(lead.split())

    body_paragraphs = re.findall(r'<p class="Body">(.*?)</p>', html_content, re.DOTALL)
    content = ""
    for paragraph in body_paragraphs:
        content += paragraph.strip()
    content = " ".join(content.split())
    content = re.sub(r'<.*?>', '', content)

    print("Title:", title)
    print("Author:", author)
    print("Published time:", published_time)
    print("Subtitle:", subtitle)
    print("Lead:", lead)
    print("Content:", content)


# extract_rtv(open("./pa2/webpages/rtvslo.si/rtvslo-2.html", "r"))


def extract_overstock(html_file):
    html_content = html_file.read()

    title_matches = re.findall(r'<td valign="top">\s*<a href=".*?"><b>(.*?)</b></a><br>', html_content, re.DOTALL)
    listPrice_matches = re.findall(r'<td align="right" nowrap="nowrap"><b>List Price:</b></td>\s*<td align="left" nowrap="nowrap"><s>(.*?)</s></td>', html_content, re.DOTALL)
    price_matches = re.findall(r'<td align="right" nowrap="nowrap"><b>Price:</b></td>\s*<td align="left" nowrap="nowrap"><span class="bigred"><b>(.*?)</b></span></td>', html_content, re.DOTALL)
    savings_matches = re.findall(r'<td align="right" nowrap="nowrap"><b>You Save:</b></td>\s*<td align="left" nowrap="nowrap"><span class="littleorange">(\$[\d,.]+)', html_content, re.DOTALL)
    savingPercent_matches = re.findall(r'\((\d+%)\)', html_content, re.DOTALL)
    content_matches = re.findall(r'<span class="normal">(.*?)<br>', html_content, re.DOTALL)

    print("Titles:", title_matches)
    print("List prices:", listPrice_matches)
    print("Prices:", price_matches)
    print("Savings:", savings_matches)
    print("Saving percents:", savingPercent_matches)
    print("Contents:", content_matches)


# extract_overstock(open("./pa2/webpages/overstock.com/jewelry02.html", "r", encoding="latin-1"))


def extract_24ur(html_file):
    html_content = html_file.read()

    title_match = re.search(re.compile(r'<h1 class=".*?">(.*?)</h1>'), html_content)
    title = title_match.group(1).strip()
    title = " ".join(title.split())

    author_match = re.search(re.compile(r'<div class="text-14 font-semibold text-black/80 dark:text-white/80">(.*?)</div>', re.DOTALL), html_content)
    author = author_match.group(1).strip()
    author = " ".join(author.split())
    
    published_time_match = re.search(re.compile(r'<p class="text-black/60 dark:text-white/60 mb-16 leading-caption">(.*?) \|', re.DOTALL), html_content)
    published_time = published_time_match.group(1).strip()
    published_time = " ".join(published_time.split())

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

    print("Title:", title)
    print("Author:", author)
    print("Published time:", published_time)
    print("Subtitle:", subtitle)
    print("Content:", content)


# extract_24ur(open("./pa2/webpages/24ur.com/novica2.html", "r"))


def extract_sportal(html_file):
    html_content = html_file.read()

    title_match = re.search(r'<h1[^>]*>(.*?)<\/h1>', html_content)
    title = title_match.group(1).strip()
    title = " ".join(title.split())

    author_match = re.search(re.compile(r'<span class="author-name">(.*?)<\/span>', re.DOTALL), html_content)
    author = author_match.group(1).strip()
    author = " ".join(author.split())
    
    published_time_match = re.search(re.compile(r'Objavljeno: (\d{2}\.\d{2}\.\d{4} ob \d{2}:\d{2})', re.DOTALL), html_content)
    published_time = published_time_match.group(1)
    published_time = " ".join(published_time.split())

    category_match = re.search(re.compile(r'<span><a href=".*?">(.*?)<\/a><\/span>', re.DOTALL), html_content)
    category = category_match.group(1).strip()
    category = re.sub(r'<p.*?>(.*?)', '', category, flags=re.DOTALL)
    category = " ".join(category.split())

    body_paragraphs = re.findall(r'<p>(.*?)<p>', html_content, re.DOTALL)
    content = ""
    for paragraph in body_paragraphs:
        content += paragraph.strip()
    content = " ".join(content.split())
    content = re.sub(r'<.*?>', '', content)

    print("Title:", title)
    print("Author:", author)
    print("Published time:", published_time)
    print("Category:", category)
    print("Content:", content)


# extract_sportal(open("./pa2/webpages/sportal.net/novica2.html", "r"))