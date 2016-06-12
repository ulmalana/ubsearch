# adding keyword into index
def add_to_index(index, keyword, url):
    for entry in index:
        if entry[0] == keyword:
            if url not in entry[1]:
                entry[1].append(url)
            return
    index.append([keyword, [url]])

# find keyword on the index
def lookup(index, keyword):
    for entry in index:
        if entry[0] == keyword:
            return entry[1]
    return []

# adding all the keyword from a webpage to index
def add_page_to_index(index, url, content):
    words = content.split()
    for word in words:
        add_to_index(index, word, url)

# split content into what split_items character contains
def split_string(source,split_items):
    output = []
    start_index = 0
    stop_index = 0
    for char in source:
        if char in split_items:
            content = source[start_index:stop_index]
            if len(content) > 0:
                output.append(content)
            start_index = stop_index + 1
        stop_index = stop_index + 1
    if len(source[start_index:]) > 0:
        output.append(source[start_index:])
    return output