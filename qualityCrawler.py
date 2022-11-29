import britishCrawler

def crawlerQuality(listOfPairs):
    if not listOfPairs:
        return {"precision": 0, "recall": 0, "F1": 0}

    start_page = listOfPairs[0][0]
    p1 = [item[1] for item in listOfPairs if item[2] == 0]
    p_tag = [item[0] for item in listOfPairs if item[0] != start_page]
    tmp = [item[1] for item in listOfPairs if item[1] != start_page]
    p1 = list(dict.fromkeys(p1))
    p_tag = list(dict.fromkeys(p_tag))
    tmp = list(dict.fromkeys(tmp))
    for item in tmp:
        if item not in p_tag:
            p_tag.append(item)
    intersection = len([x for x in p1 if x in p_tag])
    recall = intersection / len(p1)
    precision = intersection / len(p_tag)
    f1 = (2 * precision * recall) / (precision + recall)

    return {"precision": precision, "recall": recall, "F1": f1}


verify = '//p[contains(., \'was a member\')]/a[@title=\'British royal family\'] | //table[@class="infobox vcard"]//a[contains(text(),\'Head of the Commonwealth\')] | //th//a[@title=\'King of the United Kingdom\']'
ancestor = '//table[@class=\"infobox vcard\"]//th[contains(text(),\'Mother\') or contains(text(), \'Father\')]/..//@href[contains(.,\'wiki\')]'
children = "//tr//a[contains(@href,'/wiki') and contains(text(),'son')]/@href"
royalty = "//tr//a[contains(@href,'/wiki') and contains(text(),'royal')]/@href"
x = britishCrawler.british_crawler('https://en.wikipedia.org/wiki/Charles_III', None, children, ancestor, royalty)
print(x)
print(crawlerQuality(x))
