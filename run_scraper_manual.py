from app.scraper.scraper import run_full_scrape
import json 

if __name__ == "__main__":
    print("Iniciando scraper manual...")
    
    noticias = run_full_scrape()
    
    if noticias:
        print(f"\nTotal de notícias extraídas: {len(noticias)}")

    else:
        print("Nenhuma notícia foi extraída. Verifique os seletores no scraper.py")