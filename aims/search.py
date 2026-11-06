def search_by_title(items, keyword):
    return [dvd for dvd in items if keyword in dvd.title]
