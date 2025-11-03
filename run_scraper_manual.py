from app.scraper import run_full_scrape
import json 

if __name__ == "__main__":
    print("Iniciando scraper manual...")
    
    noticias = run_full_scrape()
    
    if noticias:
        print(f"\nTotal de notícias extraídas: {len(noticias)}")
        print("\nExemplo da primeira notícia:")
        print(json.dumps(noticias[0], indent=2, ensure_ascii=False))
    else:
        print("Nenhuma notícia foi extraída. Verifique os seletores no scraper.py")