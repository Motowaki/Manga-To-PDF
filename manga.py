class Chapters:
    def __init__(self, start, end):
        self.start = start
        self.end = end


class Manga:
    def __init__(self, manga, chapters):
        self.manga_name = manga
        self.formatted_manga_name = self.manga_name.replace(' ', '-').lower()
        self.start = chapters.start
        self.end = chapters.end

