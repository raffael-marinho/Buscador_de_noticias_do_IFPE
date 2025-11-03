# app/scraper.py

import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

TARGET_URLS = {
    "Igarassu": "https://www.ifpe.edu.br/campus/igarassu/noticias",
    "Recife": "https://www.ifpe.edu.br/campus/recife/noticias",
    "Jaboatão": "https://www.ifpe.edu.br/campus/jaboatao/noticias",
    "Notícias Gerais": "https://www.ifpe.edu.br/noticias"
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_soup(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except requests.RequestException as e:
        print(f"Erro ao buscar a URL {url}: {e}")
        return None

def parse_full_article_content(article_url):
    soup = get_soup(article_url)
    if not soup:
        return ""

    content_element = soup.find('div', id='parent-fieldname-text')
    
    if content_element:
        paragrafos = content_element.find_all('p')
        content = "\n".join([p.get_text(strip=True) for p in paragrafos])
        return re.sub(r'\s+', ' ', content).strip()
    
    print(f"Aviso: Não foi possível encontrar o conteúdo principal em {article_url}")
    return ""

def scrape_campus_news(campus_name, list_url):
    print(f"Iniciando varredura em: {campus_name} ({list_url})")
    soup = get_soup(list_url)
    if not soup:
        return []

    news_list = []
    
    articles = soup.find_all('article', class_='entry') 
    
    if not articles:
         articles = soup.find_all('div', class_='summary')

    print(f"Encontrados {len(articles)} artigos na página.")

    for item in articles:
        try:
            title_element = item.find('a', title=True)
            if not title_element:
                 title_element = item.find('class_').find('h2')

            if not title_element:
                print("Aviso: Item pulado, não foi possível encontrar o título/link.")
                continue

            titulo = title_element.get_text(strip=True)
            
            url_noticia = urljoin(list_url, title_element['href'])

            date_element = item.find('span', class_='documentPublishedDate')
            if not date_element:
                date_element = item.find('span', class_='summary-view-icon')

            data_publicacao = date_element.get_text(strip=True) if date_element else "Data não encontrada"

            print(f"  Extraindo: {titulo}...")
            conteudo = parse_full_article_content(url_noticia)

            if conteudo:
                news_data = {
                    "titulo": titulo,
                    "data_publicacao": data_publicacao,
                    "conteudo": conteudo,
                    "campus": campus_name,
                    "url": url_noticia
                }
                news_list.append(news_data)

        except Exception as e:
            print(f"Erro ao processar um item: {e}")

    return news_list

def run_full_scrape():
    all_news = []
    for campus, url in TARGET_URLS.items():
        all_news.extend(scrape_campus_news(campus, url))
    
    print(f"\n--- Varredura Concluída: {len(all_news)} notícias extraídas ---")
    return all_news