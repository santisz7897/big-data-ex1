import time
import requests
import lxml.html


def british_crawler(url, verify_xpath, descendant_xpaths=None, ancestor_xpaths=None, royalty_xpaths=None):
    tmp_urls, queue_of_urls = set(), set()
    queue_of_urls.add(url)
    link_to_descendants = {}
    visited_links = []
    descendants_to_ancestors = {}
    result = list()

    while len(visited_links) < 30:
        if not queue_of_urls:
            break
        current_url = queue_of_urls.pop()

        descendant_set, ancestor_set, royalty_set = set(), set(), set()
        visited_links.append(current_url)
        res = requests.get(current_url)
        doc = lxml.html.fromstring(res.content)
        to_update = [item for item in result if item[1] == current_url]
        if verify_xpath:
            after_filter = doc.xpath(verify_xpath)
            if not after_filter:
                if to_update:
                    for item in to_update:
                        result.remove(item)
                time.sleep(3)
                continue
        if to_update:
            for item in to_update:
                item.append(1)

        if descendant_xpaths is not None:
            for link in doc.xpath(descendant_xpaths):
                link = 'https://en.wikipedia.org' + link
                descendant_set.add(link)
                item = [current_url, link]
                if item not in result:
                    result.append(item)
                if link not in link_to_descendants:
                    link_to_descendants[link] = 0
            if current_url not in link_to_descendants:
                link_to_descendants[current_url] = 0
            link_to_descendants[current_url] += len(descendant_set)

        if ancestor_xpaths is not None:
            for link in doc.xpath(ancestor_xpaths):
                link = 'https://en.wikipedia.org' + link
                ancestor_set.add(link)
                item = [current_url, link]
                if item not in result:
                    result.append(item)
                if link not in link_to_descendants:
                    link_to_descendants[link] = 0
            descendants_to_ancestors[current_url] = ancestor_set

        updated = set()
        for ancestor in ancestor_set:
            if ancestor in updated:
                continue
            link_to_descendants[ancestor] += len(descendant_set) + 1
            updated.add(ancestor)

            if ancestor not in descendants_to_ancestors.keys():
                continue

            for grand in descendants_to_ancestors[ancestor]:
                if grand in updated:
                    continue
                link_to_descendants[grand] += len(descendant_set) + 1
                updated.add(grand)

        if royalty_xpaths is not None:
            for link in doc.xpath(royalty_xpaths):
                link = 'https://en.wikipedia.org' + link
                royalty_set.add(link)
                item = [current_url, link]
                if item not in result:
                    result.append(item)
                if link not in link_to_descendants:
                    link_to_descendants[link] = 0

        queue_of_urls = set()
        link_to_descendants = dict(sorted(link_to_descendants.items(), key=lambda item: item[1]))
        for key in link_to_descendants.keys():
            if key not in visited_links:
                queue_of_urls.add(key)

    for item in result:
        if item and len(item) == 2:
            item.append(0)

    time.sleep(3)
    return result
