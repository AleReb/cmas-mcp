import os
import json
import re
from datetime import datetime
import collections
import subprocess

def clean_text(text):
    if not text: return ""
    text = re.sub(r'http\S+', '', text)
    # text = re.sub(r'[^\w\s]', '', text) # Mantener algunos signos para resumen mejor
    text = " ".join(text.split())
    return text

def clean_vtt(vtt_content):
    lines = vtt_content.split('\n')
    text_lines = []
    for line in lines:
        if not line.strip() or line.strip() == "WEBVTT" or "-->" in line or line.strip().isdigit():
            continue
        clean_line = re.sub(r'<[^>]+>', '', line).strip()
        if clean_line:
            text_lines.append(clean_line)
    final_lines = []
    for line in text_lines:
        if not final_lines or line != final_lines[-1]:
            final_lines.append(line)
    return " ".join(final_lines)

def get_llm_summary(text):
    if not text or len(text) < 50:
        return "Contenido insuficiente para resumir."
    
    prompt = f"Resume el siguiente texto de un video de ingeniería/innovación, extrayendo la información más valiosa en 2-3 oraciones:\n\n{text[:4000]}"
    try:
        # Usar gemini CLI para el resumen
        result = subprocess.run(['gemini', '-p', prompt], capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception as e:
        print(f"Error llamando a Gemini CLI: {e}")
    
    return text[:200] + "..."

def process_all_in_batches(batch_size=10, limit=None):
    raw_path = os.path.join("D:\\cmas-mcp", "data", "raw", "youtube", "videos.jsonl")
    cap_dir = os.path.join("D:\\cmas-mcp", "data", "raw", "youtube", "captions")
    proc_dir = os.path.join("D:\\cmas-mcp", "data", "processed", "youtube")
    os.makedirs(proc_dir, exist_ok=True)
    
    if not os.path.exists(raw_path):
        print("No hay datos crudos.")
        return

    lexical_index = collections.defaultdict(list)
    
    with open(raw_path, 'r', encoding='utf-8') as f_in:
        lines = f_in.readlines()
    
    if limit:
        lines = lines[:limit]
        
    total_videos = len(lines)
    print(f"Iniciando procesamiento de {total_videos} videos en lotes de {batch_size} con resúmenes LLM...")

    output_file = os.path.join(proc_dir, "processed_videos_v2.jsonl")
    if os.path.exists(output_file):
        os.remove(output_file)

    for i in range(0, total_videos, batch_size):
        batch = lines[i:i + batch_size]
        processed_items = []
        
        print(f"Procesando lote {i//batch_size + 1}...")

        for line in batch:
            video = json.loads(line)
            vid_id = video['id']
            title = video.get("title") or ""
            desc = video.get("description") or ""
            
            # Buscar subtítulos
            transcript = ""
            for lang in ['es', 'en']:
                cap_path = os.path.join(cap_dir, f"{vid_id}.{lang}.vtt")
                if os.path.exists(cap_path):
                    with open(cap_path, 'r', encoding='utf-8') as f_cap:
                        transcript = clean_vtt(f_cap.read())
                    break
            
            full_text = f"Título: {title}\nDescripción: {desc}\nTranscripción: {transcript}"
            cleaned = clean_text(full_text)
            
            print(f"  - Resumiendo: {title[:50]}...")
            summary = get_llm_summary(cleaned)
            
            # Keywords de la descripción/título (simple)
            words = [w.lower() for w in re.findall(r'\w+', cleaned) if len(w) > 4]
            keywords = [w for w, _ in collections.Counter(words).most_common(5)]
            
            item_id = vid_id
            for word in set(words):
                if len(word) > 3:
                    lexical_index[word].append(item_id)
            
            mock_embedding = [0.123] * 8 # Placeholder

            processed_item = {
                "id": item_id,
                "title": title,
                "summary": summary,
                "keywords": keywords,
                "has_transcript": bool(transcript),
                "version": "2.0",
                "processed_at": datetime.now().isoformat()
            }
            processed_items.append(processed_item)

        with open(output_file, 'a', encoding='utf-8') as f:
            for item in processed_items:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')

    with open(os.path.join(proc_dir, "lexical_index_v2.json"), 'w', encoding='utf-8') as f:
        json.dump(lexical_index, f, ensure_ascii=False, indent=2)

    print(f"Procesamiento completo: {total_videos} videos en {output_file}")

if __name__ == "__main__":
    # Solo procesaremos los primeros 10 para probar el flujo de resúmenes (por tiempo/costo)
    process_all_in_batches(10, limit=10)
