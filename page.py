#!/usr/bin/env python3
import requests, os, sys, re, glob
from fpdf import FPDF
from PIL import Image
from time import sleep
from bs4 import BeautifulSoup
import shutil
from response import Response

# gets rid of all jpg's in current directory
def purge_imgs():
    cwd = os.getcwd()
    os.chdir(cwd)
    files = glob.glob('*.jpg')
    for file in files:
        os.unlink(file)


class PdfPage:
    def __init__(self, headers, manga):
        self.headers = headers
        self.manga = manga
        self.responses = Response(self.headers, self.manga)
        self.pdf = FPDF()

    def create_img(self, curr_page):
        chapter_name = '{} Chapter {} Pg {}.jpg'.format(self.manga.manga_name, self.manga.start, curr_page)
        with open(chapter_name, 'wb') as out_file:
            shutil.copyfileobj(self.responses.img_resp.raw, out_file)

    def store_pdf(self):
        self.pdf.output('{} Chapter {}.pdf'.format(self.manga.manga_name, self.manga.start).replace('\'', ''), 'F')
        self.pdf.close()

    def make_pdf(self):
        curr_manga_page = 1
        print("{} Chapter: {}".format(self.manga.manga_name, str(self.manga.start)))
        while curr_manga_page <= self.responses.last_page:
            self.pdf.add_page()
            self.responses = Response(self.headers, self.manga, curr_manga_page)
            self.create_img(curr_manga_page)
            self.pdf.image('{} Chapter {} Pg {}.jpg'.format(self.manga.manga_name, self.manga.start, curr_manga_page),
                            x=0, y=20,
                            w=205, h=255)
            print('Current Page: {}'.format(curr_manga_page))
            curr_manga_page += 1
        self.store_pdf()
        # deletes all jpgs in directory~
        purge_imgs()


