#!/usr/bin/env python3
import argparse
from page import PdfPage
from manga import Manga, Chapters
from fake_useragent import UserAgent, FakeUserAgentError

# Download's multiple manga images from mangareader.net and converts to pdf


def parse_arguments():
    parser = argparse.ArgumentParser(description="Manga-To-PDF Scraper!")
    parser.add_argument('-n', '--name', type=str, help='type the name of the manga you want (requires "") ')
    parser.add_argument('-s', '--start', type=int, help='start volume number')
    parser.add_argument('-e', '--end', type=int, help='end volume number')
    args = parser.parse_args()
    return args


def main():

    # sets up headers
    try:
        user_agent = UserAgent().chrome
        headers = {'User-Agent': user_agent}
    except FakeUserAgentError:
        user_agent = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/59.0.3071.115 Safari/537.36'")
        headers = {'User-Agent': user_agent}

    # create pdfs based off user commands
    arguments = parse_arguments()
    manga_name = arguments.name
    start = arguments.start
    end = arguments.end
    if end == None:
        end = start
    while start <= end:
        chapters = Chapters(start, end)
        manga = Manga(manga_name, chapters)
        p = PdfPage(headers, manga)
        p.make_pdf()
        start += 1

if __name__ == "__main__":
    main()

