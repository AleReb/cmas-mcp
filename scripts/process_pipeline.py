import os
import json
import re
from datetime import datetime

def clean_text(text):
    if not text: return ""
    # Remover URLs, caracteres especiales excesivos
    text = re.sub(r'http\S+', '', text)
    text = " ".join(text.split())
    return text

def chunk_text(text, chunk_size=500):
    words = text.split()
    return [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

def process_batch(batch_size=10):
    raw_path = os.path.join("D:\\cmas-mcp", "data", "raw", "youtube", "videos.jsonl")
    proc_dir = os.path.join("D:\\cmas-mcp", "data", "processed", "youtube")
    os.makedirs(proc_dir, exist_ok=True)
    
    if not os.path.exists(raw_path):
        print("No hay datos crudos para procesar.")
        return

    print(f"Procesando lote de {batch_size} videos...")
    
    processed_count = 0
    with open(raw_path, 'r', encoding='utf-8') as f_in, \
         open(os.path.join(proc_dir, "processed_videos.jsonl"), 'a', encoding='utf-8') as f_out:
        
        for line in f_in:
            if processed_count >= batch_size: break
            
            video = json.loads(line)
            content = video.get("description", "")
            cleaned = clean_text(content)
            chunks = chunk_text(cleaned)
            
            # Metadata enriquecida (Phase 3)
            processed_item = {
                "id": video["id"],
                "title": video["title"],
                "summary_short": cleaned[:200] + "..." if len(cleaned) > 200 else cleaned,
                "keywords": ["innovación", "ingeniería"], # Placeholder para extracción real
                "entities": [], # Placeholder
                "chunks": chunks,
                "version": "1.0",
                "processed_at": datetime.now().isoformat()
            }
            
            f_out.write(json.dumps(processed_item, ensure_ascii=False) + '\n')
            processed_count += 1

    print(f"Lote completado. {processed_count} videos procesados.")

if __name__ == "__main__":
    process_batch(10)
