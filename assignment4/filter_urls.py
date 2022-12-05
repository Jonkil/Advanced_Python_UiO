import re
from urllib.parse import urljoin

## -- Task 2 -- ##


def find_urls(
    html: str,
    base_url: str = "https://en.wikipedia.org",
    output: str = None,
) -> set:
    """Find all the url links in a html text using regex
    Arguments:
        html (str): html string to parse
    Returns:
        urls (set) : set with all the urls found in html text
    """
    # create and compile regular expression(s)
    # a_pat finds all the <a href=... > snippets
    # this finds <a and collects everything up to the closing '>'
    a_pat = re.compile(r"<a[^>]+>", flags=re.IGNORECASE)
    
    # href finds the text between quotes of the `href` attribute
    href_pat = re.compile(r'href="([^"]+)"', flags=re.IGNORECASE)
    urls = set()
    
    # get protocol part of the base_url for later use
    protocol = base_url.split('//')[0]
    
    # 1. find all the anchor tags, then
    # 2. find the urls href attributes
    for a_tag in a_pat.findall(html):
        match = href_pat.search(a_tag)
        if match:
            # handle different types of links
            link = match.group(1)
            
            # pointer
            # some links contain 'index.php' -- decided to omit them
            if link.startswith('#') or 'index.php?' in link:
                continue
            # only the part until '#' must be added
            elif '#' in link:
                link = link.split('#')[0]

            # page without protocol
            if link.startswith('//'):
                urls.add(protocol+link)
            # subpath
            elif link.startswith('/'):
                urls.add(base_url+link)
            else:
                urls.add(link)
                

    # Write to file if requested
    if output:
        print(f"Writing to: {output}")
        # if output is specified, urls are printed to a
        # txt file with the name in `output`
        with open(output,'w',encoding = 'utf-8') as f:
            for link in urls:
                f.write(link + "\n")
        return None

    return urls


def find_articles(html: str, output=None) -> set:
    """Finds all the wiki articles inside a html text. Make call to find urls, and filter
    arguments:
        - text (str) : the html text to parse
    returns:
        - (set) : a set with urls to all the articles found
    """
    urls = find_urls(html)
    pattern = 'wikipedia.org'
    articles = set()
    
    for url in urls:
        # the `pattern` must be in the beginning of the link
        if pattern in url.partition('/wiki/')[0]:
            articles.add(url)

    # Write to file if wanted
    if output:
        print(f"Writing to: {output}")
        # if output is specified, urls are printed to a
        # txt file with the name in `output`
        with open(output,'w',encoding = 'utf-8') as f:
            for article in articles:
                f.write(article + "\n")
        return None

    return articles


## Regex example
def find_img_src(html: str):
    """Find all src attributes of img tags in an HTML string

    Args:
        html (str): A string containing some HTML.

    Returns:
        src_set (set): A set of strings containing image URLs

    The set contains every found src attibute of an img tag in the given HTML.
    """
    # img_pat finds all the <img alt="..." src="..."> snippets
    # this finds <img and collects everything up to the closing '>'
    img_pat = re.compile(r"<img[^>]+>", flags=re.IGNORECASE)
    # src finds the text between quotes of the `src` attribute
    src_pat = re.compile(r'src="([^"]+)"', flags=re.IGNORECASE)
    src_set = set()
    # first, find all the img tags
    for img_tag in img_pat.findall(html):
        # then, find the src attribute of the img, if any
        match = src_pat.search(img_tag)
        if match:
            src_set.add(match.group(1))
    return src_set
