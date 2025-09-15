import requests


class HtmlFetcher:
    def __init__(self):
        pass

    def fetch_html(self, url):
        try:
            response = requests.get(url, timeout=24)
            response.raise_for_status()
            return response.text
        except Exception as error:
            print(f"שגיאה בשאיבת האתר {url}: {error}")
            return None

    def save_html_to_file(self, html_content, filename="page_temp.html"):
        with open(filename, "w", encoding="utf-8") as file:
            file.write(html_content)
