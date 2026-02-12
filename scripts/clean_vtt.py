import re

def clean_vtt(vtt_content):
    # Remover el header WEBVTT
    lines = vtt_content.split('\n')
    text_lines = []
    for line in lines:
        # Saltar lineas vacias, WEBVTT, lineas de tiempo y numeros de secuencia
        if not line.strip() or line.strip() == "WEBVTT" or "-->" in line or line.strip().isdigit():
            continue
        # Limpiar tags de formato <c> etc
        clean_line = re.sub(r'<[^>]+>', '', line).strip()
        if clean_line:
            text_lines.append(clean_line)
    
    # Unir y remover duplicados consecutivos (comun en VTT de YT)
    final_lines = []
    for line in text_lines:
        if not final_lines or line != final_lines[-1]:
            final_lines.append(line)
    
    return " ".join(final_lines)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            print(clean_vtt(f.read()))
