from app.scraper.scraper import run_full_scrape
from app.service.service import processar_lista_de_noticias
import json 

if __name__ == "__main__":
    print("Iniciando scraper manual...")
    
    depth_for_page = 5

    noticias = run_full_scrape(depth_for_page)
    
    if noticias:
        processar_lista_de_noticias(noticias)
        print(f"\nTotal de notícias extraídas: {len(noticias)}")

    else:
        print("Nenhuma notícia foi extraída. Verifique os seletores no scraper.py")