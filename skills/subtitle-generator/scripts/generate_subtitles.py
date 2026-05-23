#!/usr/bin/env python3
"""
Subtitle Generator — Opensquad Skill
Gera legendas de áudio/vídeo usando faster-whisper (local, gratuito).

Formatos de saída: SRT, VTT, ASS (burn-in estilizado para redes sociais)
Otimizado para MacBook Air M1 (device=auto, compute_type=int8)

Uso:
  python3 generate_subtitles.py --input narration.mp3 --output subs.srt --format srt
  python3 generate_subtitles.py --input video.mp4 --output subs.ass --format ass --language pt
  python3 generate_subtitles.py --input audio.mp3 --output subs.srt --model small --language pt
"""

import argparse
import os
import sys
from pathlib import Path

# Estilo ASS para vídeos verticais (TikTok/Reels/Shorts) — 1080×1920
ASS_STYLE_VERTICAL = """\
[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,60,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,1,2,108,108,192,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

# Estilo ASS para vídeos horizontais (YouTube) — 1920×1080
ASS_STYLE_HORIZONTAL = """\
[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,56,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,1,2,192,192,80,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def check_faster_whisper() -> None:
    """Verifica se faster-whisper está instalado."""
    try:
        import faster_whisper  # noqa: F401
    except ImportError:
        print("ERRO: faster-whisper não encontrado.")
        print("Instale com: pip install faster-whisper")
        sys.exit(1)


def get_model_size() -> str:
    """Obtém tamanho do modelo da variável de ambiente ou padrão."""
    return os.environ.get("WHISPER_MODEL_SIZE", "base")


def format_timestamp_srt(seconds: float) -> str:
    """Converte segundos para formato SRT (HH:MM:SS,mmm)."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def format_timestamp_ass(seconds: float) -> str:
    """Converte segundos para formato ASS (H:MM:SS.cc)."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    centis = int((seconds % 1) * 100)
    return f"{hours}:{minutes:02d}:{secs:02d}.{centis:02d}"


def transcribe(input_file: str, model_size: str, language: str) -> list:
    """
    Transcreve o áudio/vídeo usando faster-whisper.
    Retorna lista de segmentos: [{"start": float, "end": float, "text": str}, ...]
    """
    from faster_whisper import WhisperModel

    print(f"Carregando modelo Whisper '{model_size}' (download automático na primeira vez)...")
    model = WhisperModel(model_size, device="auto", compute_type="int8")

    lang = language if language and language != "auto" else None
    print(f"Transcrevendo: {input_file}" + (f" (idioma: {lang})" if lang else " (detecção automática)"))

    segments_iter, info = model.transcribe(
        input_file,
        language=lang,
        beam_size=5,
        vad_filter=True,  # Remove silêncio
        word_timestamps=False,
    )

    segments = []
    for seg in segments_iter:
        segments.append({
            "start": seg.start,
            "end": seg.end,
            "text": seg.text.strip(),
        })

    print(f"Transcrição concluída: {len(segments)} segmentos, idioma detectado: {info.language}")
    return segments


def to_srt(segments: list) -> str:
    """Converte segmentos para formato SRT."""
    lines = []
    for i, seg in enumerate(segments, 1):
        start = format_timestamp_srt(seg["start"])
        end = format_timestamp_srt(seg["end"])
        lines.append(f"{i}\n{start} --> {end}\n{seg['text']}\n")
    return "\n".join(lines)


def to_vtt(segments: list) -> str:
    """Converte segmentos para formato WebVTT."""
    lines = ["WEBVTT\n"]
    for i, seg in enumerate(segments, 1):
        start = format_timestamp_srt(seg["start"]).replace(",", ".")
        end = format_timestamp_srt(seg["end"]).replace(",", ".")
        lines.append(f"{i}\n{start} --> {end}\n{seg['text']}\n")
    return "\n".join(lines)


def to_ass(segments: list, resolution: str = "vertical") -> str:
    """Converte segmentos para formato ASS estilizado para redes sociais."""
    style = ASS_STYLE_VERTICAL if resolution == "vertical" else ASS_STYLE_HORIZONTAL
    lines = [style]
    for seg in segments:
        start = format_timestamp_ass(seg["start"])
        end = format_timestamp_ass(seg["end"])
        # Remove caracteres especiais que quebram o ASS
        text = seg["text"].replace("{", "").replace("}", "").replace("\n", "\\N")
        lines.append(f"Dialogue: 0,{start},{end},Default,,0,0,0,,{text}")
    return "\n".join(lines)


def main() -> None:
    # Carrega .env se existir
    try:
        from dotenv import load_dotenv
        load_dotenv(override=False)
    except ImportError:
        pass

    parser = argparse.ArgumentParser(
        description="Subtitle Generator — Opensquad Skill",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--input", required=True, help="Arquivo de entrada (MP3, MP4, WAV, etc.)")
    parser.add_argument("--output", required=True, help="Arquivo de saída (SRT, VTT ou ASS)")
    parser.add_argument(
        "--format",
        choices=["srt", "vtt", "ass"],
        default="srt",
        help="Formato de saída (padrão: srt)",
    )
    parser.add_argument(
        "--language",
        default="pt",
        help="Idioma do áudio: pt (padrão), en, es, auto (detecção automática)",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Tamanho do modelo Whisper: tiny, base (padrão), small",
    )
    parser.add_argument(
        "--resolution",
        choices=["vertical", "horizontal"],
        default="vertical",
        help="Resolução para estilo ASS: vertical (padrão, TikTok/Reels) ou horizontal (YouTube)",
    )

    args = parser.parse_args()

    check_faster_whisper()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERRO: Arquivo de entrada não encontrado: {args.input}")
        sys.exit(1)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    model_size = args.model or get_model_size()
    segments = transcribe(str(input_path), model_size, args.language)

    if not segments:
        print("AVISO: Nenhum segmento de fala detectado no áudio.")
        sys.exit(1)

    fmt = args.format.lower()
    if fmt == "srt":
        content = to_srt(segments)
    elif fmt == "vtt":
        content = to_vtt(segments)
    elif fmt == "ass":
        content = to_ass(segments, args.resolution)
    else:
        print(f"ERRO: Formato desconhecido: {fmt}")
        sys.exit(1)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    size = output_path.stat().st_size
    print(f"Legendas salvas: {output_path} ({size} bytes, {len(segments)} segmentos)")


if __name__ == "__main__":
    main()
