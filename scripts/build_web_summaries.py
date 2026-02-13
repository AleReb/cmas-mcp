import json, re, os
from collections import Counter

in_path = r'D:\cmas-mcp\data\raw\cmas_web\pages.jsonl'
out_path = r'D:\cmas-mcp\data\processed\cmas_web\web_summaries.json'

stopwords = set('''de la que el en y a los del se las por un para con no una su al lo como más pero sus le ya o este sí porque esta entre cuando muy sin sobre también me hasta hay donde quien desde todo nos durante todos uno les ni contra otros ese eso ante ellos e esto mí antes algunos qué unos yo otro otras otra él tanto esa estos mucho quienes nada muchos cual poco ella estar estas algunas algo nosotros mi mis tú te ti tu tus ellas nosotras vosotros vosotras os mío mía míos mías tuyo tuya tuyos tuyas suyo suya suyos suyas nuestro nuestra nuestros nuestras vuestro vuestra vuestros vuestras esos esas estoy estás está estamos están esté estés estén estaré estará estarán sería serían fue fueron ser siendo sido son es'''.split())

def clean_text(t):
    return re.sub(r'\s+', ' ', t or '').strip()

def split_sentences(text):
    s = re.split(r'(?<=[\.!?])\s+', text)
    return [x.strip() for x in s if len(x.strip()) > 40]

def keywords(text, k=5):
    words = re.findall(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]{4,}", text.lower())
    words = [w for w in words if w not in stopwords]
    c = Counter(words)
    return [w for w, _ in c.most_common(k)]

def entities(text, title):
    cand = re.findall(r'\b(?:[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){0,3}|[A-Z]{2,}(?:\s+[A-Z]{2,})*)\b', title + ' ' + text[:2000])
    bad = {'Inicio', 'Noticias', 'Proyecto', 'Universidad', 'Centro'}
    out = []
    for e in cand:
        e = e.strip(' .,;:()[]"\'')
        if len(e) < 3 or e in bad:
            continue
        if e not in out:
            out.append(e)
        if len(out) >= 8:
            break
    return out

rows = []
with open(in_path, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        obj = json.loads(line)
        url = obj.get('url', '')
        title = clean_text(obj.get('title', 'Sin título'))
        content = clean_text(obj.get('content', ''))

        sents = split_sentences(content)
        if len(sents) >= 3:
            summary = ' '.join(sents[:3])
        elif len(sents) == 2:
            summary = ' '.join(sents)
        elif len(sents) == 1:
            summary = sents[0]
        else:
            summary = (content[:420] + '...') if len(content) > 420 else content

        rows.append({
            'url': url,
            'title': title,
            'summary': summary,
            'keywords': keywords(title + ' ' + content, 5)[:5],
            'entities': entities(content, title)
        })

os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(rows, f, ensure_ascii=False, indent=2)

print(f'processed={len(rows)}')
print(out_path)
