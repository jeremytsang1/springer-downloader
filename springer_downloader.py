#!/usr/bin/env python3

"""
Downloader for PDFs and EPUBs from Springer.com
"""

from bs4 import BeautifulSoup
import requests


class SpringerDownloader():
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


if __name__ == '__main__':
    URL_SUFFIX = '?facet-content-type=%22Book%22&package=mat-covid19_textbooks&fbclid=IwAR2dD_eYkJArztAjIwg501C7aa9sSA9FGh8ov0PCS6-eY3QFxz2NVqNanHs&facet-language=%22En%22&facet-discipline=%22Computer+Science%22'
    downloader = SpringerDownloader(URL_SUFFIX)
