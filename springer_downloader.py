#!/usr/bin/env python3

"""
Downloader for PDFs and EPUBs from Springer.com
"""

from bs4 import BeautifulSoup
import requests
import os


class SpringerDL():
    """Defines a class for downloading PDF and EPUB files from a given
    Springer package search result."""

    # CONSTANTS
    URL_BASE = 'https://link.springer.com/'
    URL_SEARCH_BASE = 'https://link.springer.com/search/page/'
    DOWNLOAD_TEMPLATES = {
        'epub': 'https://link.springer.com/content/pdf/10.1007%2F{}.pdf',
        'pdf': 'https://link.springer.com/download/epub/10.1007%2F{}.epub'
    }
    FILETYPES = set(DOWNLOAD_TEMPLATES.keys())
    DOWNLOAD_DIR = 'downloads'

    def __init__(self, url_suffix):
        self._URL_SUFFIX = url_suffix
        self._result_soups = None

    def download(self):
        self._result_soups = self.execute_on_all_pages(SpringerDL.download_books)

    def execute_on_all_pages(self, action, start_page_num=1,):
        """Loop through each page performing action on each page."""
        page_num = start_page_num
        next_page_arrow_imgs = [None]  # If empty then reached the last page.
        result_soups = []

        # Keep going until there is no arrow link to a following page.
        while len(next_page_arrow_imgs) > 0:
            print(79 * "-")
            print(f'Processing page {page_num}')

            url = (SpringerDL.URL_SEARCH_BASE + str(page_num)
                   + self._URL_SUFFIX)

            source = requests.get(url).text
            result_soup = BeautifulSoup(source, 'lxml')
            result_soups.append(result_soup)  # save the current pages soup
            action(result_soup)

            # Find arrow button links to next page.
            next_page_arrow_imgs = result_soup.main.find_all('img', alt='next')
            page_num += 1

        return result_soups  # return all soups for debugging

    @staticmethod
    def download_books(result_soup):
        anchors = result_soup.main.find_all('a', class_='title')
        for anchor in anchors:
            book_url = SpringerDL.URL_BASE + anchor.get('href')
            SpringerDL.download_book(book_url)

    @staticmethod
    def download_book(book_url):
        isbn = book_url[book_url.rfind('/') + 1:]

        # Go to the individual book's page.
        source = requests.get(book_url).text
        book_soup = BeautifulSoup(source, 'lxml')

        # Check which formats are available to download.
        for filetype in SpringerDL.find_filetypes(book_soup):
            download_url = SpringerDL.DOWNLOAD_TEMPLATES[filetype].format(isbn)
            filename = SpringerDL.generate_filename(book_soup, filetype)
            print(filename, download_url, sep='\n  ')
            # SpringerDL.save_file(download_url, filename)

    @staticmethod
    def find_filetypes(book_soup):
        available_filetypes = set()
        title_val_template = "Download this book in {} format"

        for filetype in SpringerDL.FILETYPES:
            title_val = title_val_template.format(filetype.upper())
            if len(book_soup.find_all('a', title=title_val)) != 0:
                available_filetypes.add(filetype)
        return available_filetypes

    @staticmethod
    def generate_filename(book_soup, filetype):
        author = SpringerDL.find_author(book_soup)
        title = SpringerDL.find_title(book_soup)
        return author + '-' + title + '.' + filetype

    @staticmethod
    def find_author(book_soup):
        author = book_soup.find(class_="authors__name").text

        # Fix unicode space.
        author = author.replace(u'\xa0', u' ')

        # Grab the last name and make lower case.
        author = author[author.rfind(' ') + 1:].lower()

        # Remove apostrophes in name
        author = author.replace("'", "_")

        return author

    @staticmethod
    def find_title(book_soup):
        title = book_soup.find('div', class_="page-title").h1.text

        # Convert to lowercase and remove spaces.
        title = title.lower().replace(' ', '_')

        # Handle special characters
        title = title.replace(',', '_')
        title = title.replace('\\', '-')
        title = title.replace('/', '-')

        return title

    @staticmethod
    def save_file(download_url, base_filename):
        directory = SpringerDL.DOWNLOAD_DIR

        if not os.path.exists(directory):
            os.mkdir(directory)

        filename = os.path.join(directory, base_filename)

        if os.path.exists(filename):
            print(f'{base_filename} exists: skipping download')
        else:
            download_request = requests.get(download_url, allow_redirects=True)
            open(filename, 'wb').write(download_request.content)


if __name__ == '__main__':
    URL_SUFFIX = '?facet-content-type=%22Book%22&package=mat-covid19_textbooks&fbclid=IwAR2dD_eYkJArztAjIwg501C7aa9sSA9FGh8ov0PCS6-eY3QFxz2NVqNanHs&facet-language=%22En%22&facet-discipline=%22Computer+Science%22'
    dl = SpringerDL(URL_SUFFIX)
    dl.download()
