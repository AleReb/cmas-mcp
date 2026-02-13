import httpx
import lxml.html
import json
import os
import time
import xml.etree.ElementTree as ET

def scrape_cmas_via_sitemap(base_url, output_path):
    print(f"Iniciando scrape de: {base_url} vía Sitemap")
    
    # 1. Obtener URLs del sitemap
    sitemap_url = base_url.rstrip('/') + "/sitemap_index.xml"
    urls_to_visit = []
    
    try:
        response = httpx.get(sitemap_url, timeout=15.0, follow_redirects=True)
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            # Los sitemaps de Yoast suelen tener sub-sitemaps
            for sitemap in root.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}sitemap'):
                loc = sitemap.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text
                # Incluimos más categorías para asegurar contenido relevante
                if any(x in loc for x in ['post', 'page', 'noticia', 'proyecto', 'investigador', 'lab']):
                    print(f"Leyendo sub-sitemap: {loc}")
                    sub_resp = httpx.get(loc, timeout=15.0)
                    if sub_resp.status_code == 200:
                        sub_root = ET.fromstring(sub_resp.content)
                        for url_entry in sub_root.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
                            page_loc = url_entry.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text
                            urls_to_visit.append(page_loc)
        else:
            print("No se pudo acceder al sitemap principal. Usando fallback de navegación.")
            urls_to_visit = [base_url]
    except Exception as e:
        print(f"Error procesando sitemap: {e}. Usando fallback.")
        urls_to_visit = [base_url]

    # Eliminar duplicados y limitar
    urls_to_visit = list(set(urls_to_visit))
    print(f"Encontradas {len(urls_to_visit)} URLs potenciales.")
    
    visited = set()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        count = 0
        for url in urls_to_visit:
            if count >= 50: break # Límite de seguridad
            
            print(f"[{count+1}] Visitando: {url}")
            try:
                headers = {"User-Agent": "Mozilla/5.0 (compatible; CMASBot/1.0; +https://cmas.udd.cl/)"}
                response = httpx.get(url, timeout=15.0, follow_redirects=True, headers=headers)
                if response.status_code == 200:
                    tree = lxml.html.fromstring(response.content)
                    title_elem = tree.xpath('//title/text()')
                    title = title_elem[0].strip() if title_elem else "Sin título"
                    
                    # Limpiar contenido
                    for bad in tree.xpath('//script|//style|//nav|//footer|//header'):
                        try:
                            bad.getparent().remove(bad)
                        except: pass
                    
                    content_nodes = tree.xpath('//article|//main|//div[contains(@class, "content")]')
                    if content_nodes:
                        text = " ".join([n.text_content() for n in content_nodes])
                    else:
                        text = tree.text_content()
                        
                    text = " ".join(text.split())
                    
                    if len(text) < 200: continue # Ignorar páginas vacías
                    
                    page_data = {
                        "url": url,
                        "title": title,
                        "content": text[:8000],
                        "scraped_at": time.strftime("%Y-%m-%dT%H:%M:%SZ")
                    }
                    f.write(json.dumps(page_data, ensure_ascii=False) + '\n')
                    visited.add(url)
                    count += 1
                
                time.sleep(0.5)
            except Exception as e:
                print(f"Error visitando {url}: {e}")

    print(f"Proceso finalizado. {len(visited)} páginas guardadas en {output_path}")

if __name__ == "__main__":
    BASE_URL = "https://cmas.udd.cl/"
    OUTPUT = os.path.join("D:\\cmas-mcp", "data", "raw", "cmas_web", "pages.jsonl")
    scrape_cmas_via_sitemap(BASE_URL, OUTPUT)
