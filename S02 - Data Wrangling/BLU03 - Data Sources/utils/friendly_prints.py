def friendly_print_string(s):
    print(s[:500])


def friendly_print_beers(response):
    return response[:1]


def friendly_print_soup_children(soup_children):
    soup_children[3] = soup_children[3][:500]
    
    return soup_children
        