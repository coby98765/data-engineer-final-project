import os

import requests


class HtmlFetcher:
    def __init__(self):
        pass
    """"
    This function receives a url and scans the site with the "requests" library and gets all the information in html.
    """
    def fetch_html(self, url):
        try:
            response = requests.get(url, timeout=24)
            response.raise_for_status()
            return response.text
        except Exception as error:
            print(f"שגיאה בשאיבת האתר {url}: {error}")
            return None
    """
    This function saves the information we received from the site in a local file.
    """
    def save_html_to_file(self, html_content):
        if not os.path.exists('tmp'):
            os.mkdir('tmp')
        with open("tmp/data.html", "w", encoding="utf-8") as file:
            file.write(html_content)
