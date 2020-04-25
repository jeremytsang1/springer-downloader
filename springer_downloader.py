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
    FILETYPES = {'pdf', 'epub'}
    DOWNLOAD_TEMPLATES = {
        'epub': 'https://link.springer.com/content/pdf/10.1007%2F{}.pdf',
        'pdf': 'https://link.springer.com/download/epub/10.1007%2F{}.epub'
    }

    def __init__(self, url_suffix):
        self._URL_SUFFIX = url_suffix

    def execute_on_all_pages(self, action, start_page_num=1,):
        """Loop through each page performing action on each page."""
        page_num = start_page_num
        next_page_arrow_imgs = [None]  # If empty then reached the last page.

        # Keep going until there is no arrow link to a following page.
        while len(next_page_arrow_imgs) > 0:
            print(79 * "-")
            print(f'Processing page {page_num}')

            url = (SpringerDownloader.URL_SEARCH_BASE + str(page_num)
                   + self._URL_SUFFIX)

            source = requests.get(url).text
            soup = BeautifulSoup(source, 'lxml')
            print(soup.title(soup)

            # Find arrow button links to next page.
            next_page_arrow_imgs = soup.main.find_all('img', alt='next')
            page_num += 1


def dummy_function(soup):
    """Dummy function."""
    return soup


if __name__ == '__main__':
    URL_SUFFIX = '?facet-content-type=%22Book%22&package=mat-covid19_textbooks&fbclid=IwAR2dD_eYkJArztAjIwg501C7aa9sSA9FGh8ov0PCS6-eY3QFxz2NVqNanHs&facet-language=%22En%22&facet-discipline=%22Computer+Science%22'
    downloader = SpringerDownloader(URL_SUFFIX)
    downloader.execute_on_all_pages(dummy_function)
