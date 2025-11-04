from requests_html import HTMLSession
from bs4 import BeautifulSoup, Comment, NavigableString
import re

class Scraper():

    def getAppName(self, tag):

        # Calling aptoide web server -> Used in the website we want to scrape
        url = f"https://ws75.aptoide.com/api/7/apps/search?query={tag}"
        session = HTMLSession()
        result = session.get(url)

        if result.status_code != 200:
            print("Request failed:", result.status_code)
            return None
        
        # Acess the name of the app we want
        try:
            uname = result.json()['datalist']['list'][0]['uname']
        except (KeyError, IndexError) as e:
            raise ValueError(f"Error while finding the uname: {e}")

        return uname

    def getAppPage(self, tag):

        # Url with the App we want to scrape
        url = f"https://{tag}.pt.aptoide.com/app"
        session = HTMLSession()
        result = session.get(url)

        if result.status_code != 200:
            raise RuntimeError(f"Request failed: {result.status_code}")

        return result

    def scrapeData(self, tag):

        # getting the name of the app we want to get the correct url
        scraper = Scraper()
        name = scraper.getAppName(tag)

        # getting the page with the data from the app
        page = scraper.getAppPage(name)
        soup = BeautifulSoup(page.content, "html.parser")

        # only the div with all the app info 
        container = soup.select_one('div[class^="info__InfoContainer"]')

        if not container:
            raise ValueError("couldn't find info container")

        def normalize_key(s: str) -> str:
            # some normalization to make it possible to extract values
            s = re.sub(r'\s+', ' ', s).strip()
            s = re.sub(r'[:\u00a0]+$', '', s).strip()

            return s

        def extract_value(container, key_text):
            key_text_norm = normalize_key(key_text).lower()

            for strong in container.find_all('strong'):
                # get normalized key
                strong_text = normalize_key(strong.get_text(" ", strip=True))
                if not strong_text:
                    continue

                if key_text_norm in strong_text.lower() or re.search(re.escape(key_text_norm), strong_text, re.I):
                    parts = []

                    for sib in strong.next_siblings:
                        # skip comments & empty strings
                        if isinstance(sib, Comment):
                            continue

                        if isinstance(sib, NavigableString):
                            txt = sib.strip()
                            if txt:
                                parts.append(txt)

                        else:
                            txt = sib.get_text(" ", strip=True)
                            if txt:
                                parts.append(txt)

                    value = " ".join(parts).strip()

                    if value:
                        # remove any leading colon or the key label that might still be present
                        value = re.sub(rf'^{re.escape(strong_text)}\s*:?\s*', '', value, flags=re.I).strip()
                        return value

                    # fallback: try parent text minus key
                    parent_text = normalize_key(strong.parent.get_text(" ", strip=True))
                    fallback = re.sub(rf'^{re.escape(strong_text)}\s*:?\s*', '', parent_text, flags=re.I).strip()
                    return fallback if fallback else "n/a"

            return "N/A"

        fields = {
            "name": "Nome",
            "size": "Tamanho",
            "downloads": "Transferências",
            "version": "Versão",
            "release_date": "Data de lançamento",
            "min_screen": "Ecrã mínimo",
            "supported_cpu": "CPU Suportado",
            "package_id": "ID do Pacote",
            "sha1_signature": "Assinatura SHA1",
            "developer_cn": "Programador (CN)",
            "organization": "Organização (O)",
            "local": "Localização (L)",
            "country": "País (C)",
            "state_city": "Estado/Cidade (ST)",
        }

        # extraction
        result = {k: extract_value(container, v) for k, v in fields.items()}

        return result

