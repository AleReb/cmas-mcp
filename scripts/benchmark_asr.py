import json
import os
import time
from pathlib import Path

AUDIO = Path(r"D:\cmas-mcp\transcription\input\sample.ogg")
OUT = Path(r"D:\cmas-mcp\transcription\bench")
OUT.mkdir(parents=True, exist_ok=True)

results = {
    "audio": str(AUDIO),
    "runs": []
}

# 1) openai-whisper
try:
    import whisper
    t0 = time.time()
    model = whisper.load_model("base")
    t1 = time.time()
    r = model.transcribe(str(AUDIO), language="es", fp16=False)
    t2 = time.time()
    text = (r.get("text") or "").strip()
    (OUT / "whisper_base.txt").write_text(text, encoding="utf-8")
    results["runs"].append({
        "engine": "openai-whisper",
        "model": "base",
        "load_s": round(t1 - t0, 3),
        "transcribe_s": round(t2 - t1, 3),
        "total_s": round(t2 - t0, 3),
        "chars": len(text),
        "ok": True
    })
except Exception as e:
    results["runs"].append({
        "engine": "openai-whisper",
        "model": "base",
        "ok": False,
        "error": str(e)
    })

# 2) faster-whisper
try:
    from faster_whisper import WhisperModel
    t0 = time.time()
    model = WhisperModel("base", device="cpu", compute_type="int8")
    t1 = time.time()
    segments, info = model.transcribe(str(AUDIO), language="es")
    segs = list(segments)
    text = " ".join([(s.text or "").strip() for s in segs]).strip()
    t2 = time.time()
    (OUT / "faster_whisper_base.txt").write_text(text, encoding="utf-8")
    results["runs"].append({
        "engine": "faster-whisper",
        "model": "base/int8/cpu",
        "load_s": round(t1 - t0, 3),
        "transcribe_s": round(t2 - t1, 3),
        "total_s": round(t2 - t0, 3),
        "chars": len(text),
        "ok": True
    })
except Exception as e:
    results["runs"].append({
        "engine": "faster-whisper",
        "model": "base/int8/cpu",
        "ok": False,
        "error": str(e)
    })

(OUT / "benchmark.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(results, ensure_ascii=False, indent=2))
