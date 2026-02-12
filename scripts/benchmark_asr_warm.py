import json, time
from pathlib import Path
AUDIO=Path(r"D:\cmas-mcp\transcription\input\sample.ogg")
OUT=Path(r"D:\cmas-mcp\transcription\bench")
OUT.mkdir(parents=True, exist_ok=True)
res={"audio":str(AUDIO),"warm_runs":[]}

# openai-whisper warm (model loaded once)
try:
    import whisper
    t0=time.time(); m=whisper.load_model("base"); t1=time.time()
    times=[]
    txt=''
    for _ in range(3):
        a=time.time(); r=m.transcribe(str(AUDIO), language='es', fp16=False); b=time.time(); times.append(round(b-a,3)); txt=(r.get('text') or '').strip()
    res['warm_runs'].append({"engine":"openai-whisper","load_s":round(t1-t0,3),"transcribe_runs_s":times,"avg_transcribe_s":round(sum(times)/len(times),3),"chars":len(txt),"ok":True})
except Exception as e:
    res['warm_runs'].append({"engine":"openai-whisper","ok":False,"error":str(e)})

# faster-whisper warm
try:
    from faster_whisper import WhisperModel
    t0=time.time(); m=WhisperModel('base', device='cpu', compute_type='int8'); t1=time.time()
    times=[]
    txt=''
    for _ in range(3):
        a=time.time(); seg,_=m.transcribe(str(AUDIO), language='es'); seg=list(seg); txt=' '.join([(s.text or '').strip() for s in seg]).strip(); b=time.time(); times.append(round(b-a,3))
    res['warm_runs'].append({"engine":"faster-whisper","load_s":round(t1-t0,3),"transcribe_runs_s":times,"avg_transcribe_s":round(sum(times)/len(times),3),"chars":len(txt),"ok":True})
except Exception as e:
    res['warm_runs'].append({"engine":"faster-whisper","ok":False,"error":str(e)})

(OUT/'benchmark_warm.json').write_text(json.dumps(res,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(res,ensure_ascii=False,indent=2))
