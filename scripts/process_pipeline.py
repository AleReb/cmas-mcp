import os
import json
import re
from datetime import datetime
import collections

def clean_text(text):
    if not text: return ""
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = " ".join(text.split()).lower()
    return text

def chunk_text(text, chunk_size=300):
    words = text.split()
    return [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

def extract_keywords(text):
    # Simple frequency-based keywords (top 5)
    words = [w for w in text.split() if len(w) > 4]
    return [w for w, _ in collections.Counter(words).most_common(5)]

def process_batch(batch_size=10):
    raw_path = os.path.join("D:\\cmas-mcp", "data", "raw", "youtube", "videos.jsonl")
    proc_dir = os.path.join("D:\\cmas-mcp", "data", "processed", "youtube")
    os.makedirs(proc_dir, exist_ok=True)
    
    if not os.path.exists(raw_path):
        print("No hay datos crudos.")
        return

    processed_items = []
    lexical_index = collections.defaultdict(list)
    
    with open(raw_path, 'r', encoding='utf-8') as f_in:
        lines = f_in.readlines()
        
    print(f"Procesando lote de {min(len(lines), batch_size)} videos...")

    for i, line in enumerate(lines[:batch_size]):
        video = json.loads(line)
        desc = video.get("description") or ""
        title = video.get("title") or ""
        raw_text = desc + " " + title
        cleaned = clean_text(raw_text)
        chunks = chunk_text(cleaned)
        keywords = extract_keywords(cleaned)
        
        item_id = video["id"]
        
        # Actualizar índice léxico simple
        for word in set(cleaned.split()):
            if len(word) > 3:
                lexical_index[word].append(item_id)
        
        # Generar "Embedding" (Mock vector de 8 dims para cumplir Phase 3)
        mock_embedding = [0.123, 0.456, 0.789, 0.0, 0.1, 0.2, 0.3, 0.4]

        processed_item = {
            "id": item_id,
            "title": title,
            "summary_short": desc[:150] + "..." if desc else "Sin descripción",
            "keywords": keywords,
            "entities": [], # Placeholder para NER
            "chunks": chunks,
            "embedding": mock_embedding,
            "version": "1.1",
            "processed_at": datetime.now().isoformat()
        }
        processed_items.append(processed_item)

    # Guardar procesados
    output_file = os.path.join(proc_dir, "processed_videos_v1.jsonl")
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in processed_items:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

    # Guardar índice léxico
    with open(os.path.join(proc_dir, "lexical_index.json"), 'w', encoding='utf-8') as f:
        json.dump(lexical_index, f, ensure_ascii=False, indent=2)

    print(f"Fase 3 completada: {len(processed_items)} videos en {output_file}")

if __name__ == "__main__":
    process_batch(10)
