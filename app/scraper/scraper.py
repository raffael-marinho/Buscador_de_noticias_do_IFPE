import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
import time
from app.schemas.schema import Noticia
from app.repository.repository import salvar_noticia

TARGET_URLS = {
    "Igarassu": "https://portal.ifpe.edu.br/igarassu/noticias",
    "Recife": "https://portal.ifpe.edu.br/recife/noticias",
    "Jaboatao": "https://portal.ifpe.edu.br/jaboatao/noticias",
    "Noticias Gerais": "https://portal.ifpe.edu.br/noticias"
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
}

def get_soup(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except requests.RequestException as e:
        print(f"Erro ao buscar a URL {url}: {e}")
        return None

def parse_full_article_content(article_url):
    """Extrai o conteudo completo de uma noticia"""
    soup = get_soup(article_url)
    if not soup:
        return ""
    
    # Procura pelo conteudo principal do artigo
    content_element = soup.find('div', class_='entry-content')
    
    if content_element:
        paragrafos = content_element.find_all('p')
        if paragrafos:
            content = "\n".join([p.get_text(strip=True) for p in paragrafos])
            return re.sub(r'\s+', ' ', content).strip()
    
    return "Conteudo nao disponivel"

def scrape_campus_news(campus_name, list_url):
    print(f"\n{'='*70}")
    print(f"Buscando noticias: {campus_name}")
    print(f"{'='*70}")
    
    soup = get_soup(list_url)
    if not soup:
        return []

    news_list = []
    
    # Busca especificamente por <article class="noticia">
    articles = soup.find_all('article', class_='noticia')
    
    total_encontrados = len(articles)
    print(f"Total de artigos encontrados: {total_encontrados}")
    
    if total_encontrados == 0:
        print("Nenhum artigo encontrado. A estrutura do site pode ter mudado.\n")
        return []
    
    print(f"\nExtraindo as 5 primeiras noticias:\n")
    
    # Processa apenas os 5 primeiros
    for idx, article in enumerate(articles[:5], 1):
        try:
            # Pega o link principal da noticia
            link = article.find('a', class_='noticia__link')
            
            if not link:
                print(f"[{idx}] Aviso: Link nao encontrado, pulando...")
                continue
            
            url_noticia = link.get('href', '')
            
            if not url_noticia:
                continue
            
            # Pega o titulo
            titulo_element = article.find('h2', class_='noticia__titulo')
            
            if not titulo_element:
                print(f"[{idx}] Aviso: Titulo nao encontrado, pulando...")
                continue
            
            titulo = titulo_element.get_text(strip=True)
            
            # Remove caracteres HTML especiais
            titulo = titulo.replace('&#8217;', "'").replace('&#8220;', '"').replace('&#8221;', '"')
            
            print(f"[{idx}] {titulo}")
            print(f"    URL: {url_noticia}\n")
            
            # Extrai conteudo (desabilitado para velocidade)
            conteudo = extract_main_news_content(soup)

            dados_da_noticia = extract_relevant_data_from_news(url_noticia)

            news_data = {
                "titulo": titulo,
                "html_puro": dados_da_noticia["html_puro"],
                "conteudo": dados_da_noticia["conteudo"],
                "campus": campus_name,
                "url": url_noticia,
                "coletado_em": str(time.time())
            }
            news_list.append(news_data)
            
            time.sleep(0.3)

        except Exception as e:
            print(f"[{idx}] Erro ao processar item: {e}")
            continue

    print(f"Total extraido de {campus_name}: {len(news_list)} noticias\n")
    
    return news_list

def extract_main_news_content(given_soup):
    main_news_content_element = given_soup.find('div', class_='post__content')
    extracted_content = ''
    if not main_news_content_element:
        return None
    extracted_content = main_news_content_element.get_text(strip=True)
    return extracted_content

def extract_relevant_data_from_news(news_url):
    response = requests.get(news_url, headers=HEADERS, timeout=15)
    response.raise_for_status()
    response.encoding = response.apparent_encoding
    response_content = response.text

    news_soup = BeautifulSoup(response_content, 'html.parser')
    main_news_content = extract_main_news_content(news_soup)

    minified_html = re.sub(r">\s+<", "><", response_content)
    minified_html = re.sub(r"\s+", " ", minified_html).strip()
    return {"conteudo": main_news_content, "html_puro": minified_html}

def run_full_scrape():
    all_news = []
    print("\n" + "="*70)
    print("INICIANDO SCRAPER DO IFPE")
    print("="*70)
    
    for campus, url in TARGET_URLS.items():
        campus_news = scrape_campus_news(campus, url)
        all_news.extend(campus_news)
    
    print("="*70)
    print(f"CONCLUIDO: {len(all_news)} noticias extraidas no total")
    print("="*70 + "\n")
    
    return all_news