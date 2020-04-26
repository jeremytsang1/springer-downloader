#!/usr/bin/env python3

"""
Downloader for PDFs and EPUBs from Springer.com
"""

from bs4 import BeautifulSoup
import requests


class SpringerDownloader():
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

    def __init__(self, url_suffix):
        self._URL_SUFFIX = url_suffix

    def execute_on_all_pages(self, action, start_page_num=1,):
        """Loop through each page performing action on each page."""
        page_num = start_page_num
        next_page_arrow_imgs = [None]  # If empty then reached the last page.
        result_soups = []

        # Keep going until there is no arrow link to a following page.
        while len(next_page_arrow_imgs) > 0:
            print(79 * "-")
            print(f'Processing page {page_num}')

            url = (SpringerDownloader.URL_SEARCH_BASE + str(page_num)
                   + self._URL_SUFFIX)

            source = requests.get(url).text
            result_soup = BeautifulSoup(source, 'lxml')
            result_soups.append(result_soup)  # save the current pages soup
            action(result_soup)

            # Find arrow button links to next page.
            next_page_arrow_imgs = result_soup.main.find_all('img', alt='next')
            page_num += 1

        return result_soups  # return all soups for debugging

    def download_books(self, result_soup):
        anchors = result_soup.main.find_all('a', class_='title')
        for anchor in anchors:
            title = anchor.text
            book_url = SpringerDownloader.URL_BASE + anchor.get('href')
            self.download_book(book_url, title)

    def download_book(self, book_url, title):
        isbn = book_url[book_url.rfind('/') + 1:]

        # Go to the individual book's page.
        source = requests.get(book_url).text
        book_soup = BeautifulSoup(source, 'lxml')
        print(book_soup.title)

        # Check which formats are available to download.

        # Download available formats


def dummy_function(soup):
    """Dummy function."""
    return soup


if __name__ == '__main__':
    URL_SUFFIX = '?facet-content-type=%22Book%22&package=mat-covid19_textbooks&fbclid=IwAR2dD_eYkJArztAjIwg501C7aa9sSA9FGh8ov0PCS6-eY3QFxz2NVqNanHs&facet-language=%22En%22&facet-discipline=%22Computer+Science%22'
    dl = SpringerDownloader(URL_SUFFIX)
    result_soups = dl.execute_on_all_pages(dl.download_books)
