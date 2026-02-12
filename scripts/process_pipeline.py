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

def process_all_in_batches(batch_size=10):
    raw_path = os.path.join("D:\\cmas-mcp", "data", "raw", "youtube", "videos.jsonl")
    proc_dir = os.path.join("D:\\cmas-mcp", "data", "processed", "youtube")
    os.makedirs(proc_dir, exist_ok=True)
    
    if not os.path.exists(raw_path):
        print("No hay datos crudos.")
        return

    lexical_index = collections.defaultdict(list)
    
    with open(raw_path, 'r', encoding='utf-8') as f_in:
        lines = f_in.readlines()
    
    total_videos = len(lines)
    print(f"Iniciando procesamiento de {total_videos} videos en lotes de {batch_size}...")

    output_file = os.path.join(proc_dir, "processed_videos_v1.jsonl")
    # Limpiar archivo de salida si existe para empezar de cero "todos"
    if os.path.exists(output_file):
        os.remove(output_file)

    for i in range(0, total_videos, batch_size):
        batch = lines[i:i + batch_size]
        processed_items = []
        
        print(f"Procesando lote {i//batch_size + 1}: videos {i+1} a {min(i+batch_size, total_videos)}...")

        for line in batch:
            video = json.loads(line)
            desc = video.get("description") or ""
            title = video.get("title") or ""
            raw_text = desc + " " + title
            cleaned = clean_text(raw_text)
            chunks = chunk_text(cleaned)
            keywords = extract_keywords(cleaned)
            
            item_id = video["id"]
            
            for word in set(cleaned.split()):
                if len(word) > 3:
                    lexical_index[word].append(item_id)
            
            mock_embedding = [0.123, 0.456, 0.789, 0.0, 0.1, 0.2, 0.3, 0.4]

            processed_item = {
                "id": item_id,
                "title": title,
                "summary_short": desc[:150] + "..." if desc else "Sin descripción",
                "keywords": keywords,
                "entities": [],
                "chunks": chunks,
                "embedding": mock_embedding,
                "version": "1.1",
                "processed_at": datetime.now().isoformat()
            }
            processed_items.append(processed_item)

        # Guardar lote (append)
        with open(output_file, 'a', encoding='utf-8') as f:
            for item in processed_items:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')

    # Guardar índice léxico final
    with open(os.path.join(proc_dir, "lexical_index.json"), 'w', encoding='utf-8') as f:
        json.dump(lexical_index, f, ensure_ascii=False, indent=2)

    print(f"Procesamiento completo: {total_videos} videos procesados en {output_file}")

if __name__ == "__main__":
    process_all_in_batches(10)
