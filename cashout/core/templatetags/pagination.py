from django import template


register = template.Library()


@register.filter
def pagination_link(get, page):
    get = get.copy()
    get["page"] = page
    query_list = []
    for query_key, query_value in get.items():
        query_list.append("{}={}".format(query_key, query_value))
    query_string = "&".join(query_list)
    query_string = "?{}".format(query_string)
    return query_string
