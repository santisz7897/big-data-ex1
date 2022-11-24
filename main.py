import requests
import lxml.html
import time
from bs4 import BeautifulSoup


# test with urls = crawl("https://en.wikipedia.org/wiki/Elizabeth_II", [])


def filter_links(xpath, list):
    if xpath is None:
        return list
    result = []
    for link in list:
        time.sleep(1)
        res = requests.get(link)
        doc = lxml.html.fromstring(res.content)
        urls = doc.xpath(xpath)
        print(urls)
        if urls:
            print(link)
            result.append(link)
    return result


def british_crawler(url, verify_xpath, descendant_xpaths=None, ancestor_xpaths=None, royalty_xpaths=None):
    tmp_urls, queue_of_urls = set(), set()
    queue_of_urls.add(url)
    link_to_descendants = {}
    visited_links = [url]

    # for t in doc.xpath("//a[starts-with(@href, '/wiki')]"):
    #     current_url = t.attrib['href']
    #     current_url = 'https://en.wikipedia.org' + current_url
    #     tmp_urls.add(current_url)
    #
    # after_filter = filter_links(verify_xpath, tmp_urls)
    # for filtered_link in after_filter:
    #     if filtered_link not in visited_links:
    #         queue_of_urls.add(filtered_link)

    while len(visited_links) < 30:
        current_url = queue_of_urls.pop()
        print(current_url)
        tmp_urls = set()
        visited_links.append(current_url)
        res = requests.get(current_url)
        doc = lxml.html.fromstring(res.content)
        after_filter = []
        if descendant_xpaths is not None:

            for link in doc.xpath(descendant_xpaths):
                link = 'https://en.wikipedia.org' + link
                tmp_urls.add(link)
            after_filter = filter_links(verify_xpath, tmp_urls)
            for link in after_filter:
                if link not in link_to_descendants:
                    link_to_descendants[link] = 0
            if current_url not in link_to_descendants:
                link_to_descendants[current_url] = 0
            link_to_descendants[current_url] += len(after_filter)
        tmp_urls = set()

        if ancestor_xpaths is not None:
            for link in doc.xpath(ancestor_xpaths):
                link = 'https://en.wikipedia.org' + link
                tmp_urls.add(link)
            after_filter = filter_links(verify_xpath, tmp_urls)
            for link in after_filter:
                if link not in link_to_descendants:
                    link_to_descendants[link] = 0
                link_to_descendants[link] += link_to_descendants[current_url] + 1
        tmp_urls = set()
        if royalty_xpaths is not None:
            for link in doc.xpath(royalty_xpaths):
                link = 'https://en.wikipedia.org' + link
                tmp_urls.add(link)
            after_filter = filter_links(verify_xpath, tmp_urls)
            for link in after_filter:
                if link not in link_to_descendants:
                    link_to_descendants[link] = 0

        link_to_descendants = dict(sorted(link_to_descendants.items(), key=lambda item: item[1]))
        for key in link_to_descendants.keys():
            if key not in visited_links:
                visited_links.append(key)
                queue_of_urls.add(key)
        print(link_to_descendants)
        print(visited_links)
        print(queue_of_urls)


verify = '//p[contains(., \'was a member\')]/a[@title=\'British royal family\'] | //table[@class="infobox vcard"]//a[contains(text(),\'Head of the Commonwealth\')] | //th//a[@title=\'King of the United Kingdom\']'
ancestor = '//table[@class=\"infobox vcard\"]//th[contains(text(),\'Mother\') or contains(text(), \'Father\')]/..//@href[contains(.,\'wiki\')]'
children = "//tr//a[contains(@href,'/wiki') and contains(text(),'Prince')]/@href"
royalty = "//tr//a[contains(@href,'/wiki') and contains(text(),'royal')]/@href"
british_crawler('https://en.wikipedia.org/wiki/George_VI', verify, children, ancestor, royalty)
