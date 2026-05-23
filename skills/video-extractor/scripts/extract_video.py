#!/usr/bin/env python3
"""
Video Extractor — Opensquad Skill
Baixa e extrai conteúdo de plataformas de vídeo usando yt-dlp.

Operações:
  download   — Baixar vídeo completo (MP4)
  audio      — Extrair apenas o áudio (MP3)
  frames     — Capturar frames a cada N segundos (PNG)
  metadata   — Obter metadados do vídeo (JSON)
  transcript — Obter transcrição automática (SRT)

Uso:
  python3 extract_video.py --url "https://..." --operation download --output video.mp4
  python3 extract_video.py --url "https://..." --operation metadata --output meta.json
  python3 extract_video.py --url "https://..." --operation frames --output frames/ --fps 1
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def check_ytdlp() -> None:
    """Verifica se yt-dlp está instalado."""
    try:
        subprocess.run(["yt-dlp", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("ERRO: yt-dlp não encontrado.")
        print("Instale com: pip install yt-dlp")
        sys.exit(1)


def check_ffmpeg() -> None:
    """Verifica se FFmpeg está instalado (necessário para frames e audio)."""
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("ERRO: FFmpeg não encontrado.")
        print("Instale com: brew install ffmpeg (macOS) ou apt install ffmpeg (Linux)")
        sys.exit(1)


def download_video(url: str, output: str) -> None:
    """Baixa vídeo completo em MP4 (melhor qualidade até 1080p)."""
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "yt-dlp",
        "--format", "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best",
        "--merge-output-format", "mp4",
        "--output", str(output_path),
        "--no-playlist",
        url,
    ]

    print(f"Baixando vídeo de: {url}")
    result = subprocess.run(cmd, capture_output=False)
    if result.returncode != 0:
        print(f"ERRO: yt-dlp falhou ao baixar o vídeo (código {result.returncode})")
        sys.exit(1)

    if output_path.exists():
        size_mb = output_path.stat().st_size / (1024 * 1024)
        print(f"Vídeo salvo: {output_path} ({size_mb:.1f} MB)")
    else:
        print("ERRO: Arquivo de saída não foi criado")
        sys.exit(1)


def extract_audio(url: str, output: str) -> None:
    """Extrai apenas o áudio como MP3 a 192kbps."""
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # yt-dlp usa o caminho sem extensão para o template; adicionamos .mp3 depois
    output_template = str(output_path.with_suffix(""))

    cmd = [
        "yt-dlp",
        "--extract-audio",
        "--audio-format", "mp3",
        "--audio-quality", "192K",
        "--output", output_template + ".%(ext)s",
        "--no-playlist",
        url,
    ]

    print(f"Extraindo áudio de: {url}")
    result = subprocess.run(cmd, capture_output=False)
    if result.returncode != 0:
        print(f"ERRO: yt-dlp falhou ao extrair áudio (código {result.returncode})")
        sys.exit(1)

    # yt-dlp pode nomear o arquivo diferente — encontramos o MP3 gerado
    mp3_file = output_path if output_path.suffix == ".mp3" else Path(output_template + ".mp3")
    if mp3_file.exists():
        size_mb = mp3_file.stat().st_size / (1024 * 1024)
        print(f"Áudio salvo: {mp3_file} ({size_mb:.1f} MB)")
    else:
        print("AVISO: Arquivo MP3 pode ter sido salvo com nome diferente no diretório")


def extract_frames(url: str, output_dir: str, fps: float = 1.0) -> None:
    """Captura frames do vídeo a cada N segundos usando FFmpeg."""
    check_ffmpeg()
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Primeiro baixa o vídeo temporariamente
    temp_video = output_path / "_temp_video.mp4"
    download_video(url, str(temp_video))

    # Extrai frames com FFmpeg
    frame_pattern = str(output_path / "frame-%06d.png")
    cmd = [
        "ffmpeg",
        "-i", str(temp_video),
        "-vf", f"fps={fps}",
        "-q:v", "2",
        frame_pattern,
        "-y",
    ]

    print(f"Extraindo frames (1 frame a cada {1/fps:.1f}s)...")
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        print(f"ERRO: FFmpeg falhou ao extrair frames")
        print(result.stderr.decode())
        temp_video.unlink(missing_ok=True)
        sys.exit(1)

    # Remove vídeo temporário
    temp_video.unlink(missing_ok=True)

    frames = list(output_path.glob("frame-*.png"))
    print(f"Frames extraídos: {len(frames)} imagens em {output_path}")


def get_metadata(url: str, output: str) -> None:
    """Obtém metadados do vídeo (sem download) como JSON."""
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "yt-dlp",
        "--dump-json",
        "--no-playlist",
        url,
    ]

    print(f"Obtendo metadados de: {url}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ERRO: Falha ao obter metadados")
        print(result.stderr)
        sys.exit(1)

    try:
        raw = json.loads(result.stdout)
    except json.JSONDecodeError:
        print("ERRO: Resposta inválida do yt-dlp")
        sys.exit(1)

    # Extrai apenas os campos relevantes
    metadata = {
        "title": raw.get("title"),
        "description": raw.get("description"),
        "duration": raw.get("duration"),
        "duration_string": raw.get("duration_string"),
        "view_count": raw.get("view_count"),
        "like_count": raw.get("like_count"),
        "comment_count": raw.get("comment_count"),
        "upload_date": raw.get("upload_date"),
        "uploader": raw.get("uploader"),
        "channel": raw.get("channel"),
        "channel_url": raw.get("channel_url"),
        "tags": raw.get("tags", []),
        "categories": raw.get("categories", []),
        "webpage_url": raw.get("webpage_url"),
        "thumbnail": raw.get("thumbnail"),
        "width": raw.get("width"),
        "height": raw.get("height"),
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    print(f"Metadados salvos: {output_path}")
    print(f"  Título: {metadata['title']}")
    print(f"  Duração: {metadata['duration_string']}")
    print(f"  Views: {metadata['view_count']:,}" if metadata['view_count'] else "  Views: N/A")


def get_transcript(url: str, output: str, lang: str = "pt") -> None:
    """Obtém transcrição automática do vídeo quando disponível."""
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Tenta baixar legendas automáticas em PT-BR, PT ou EN
    langs_to_try = [lang, "pt-BR", "pt", "en"] if lang not in ["pt-BR", "pt", "en"] else [lang, "pt-BR", "pt", "en"]
    langs_str = ",".join(dict.fromkeys(langs_to_try))  # deduplica mantendo ordem

    output_template = str(output_path.with_suffix(""))

    cmd = [
        "yt-dlp",
        "--write-auto-sub",
        "--skip-download",
        "--sub-langs", langs_str,
        "--sub-format", "srt",
        "--convert-subs", "srt",
        "--output", output_template,
        "--no-playlist",
        url,
    ]

    print(f"Obtendo transcrição automática de: {url}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    # Procura arquivo SRT gerado
    srt_files = list(output_path.parent.glob(f"{output_path.stem}*.srt"))
    if srt_files:
        srt_file = srt_files[0]
        # Move para o caminho de output esperado
        if str(srt_file) != str(output_path):
            srt_file.rename(output_path)
        size = output_path.stat().st_size
        print(f"Transcrição salva: {output_path} ({size} bytes)")
    else:
        print("AVISO: Transcrição automática não disponível para este vídeo.")
        print("Use subtitle-generator com o áudio extraído para gerar legendas via Whisper:")
        print(f"  python3 skills/subtitle-generator/scripts/generate_subtitles.py \\")
        print(f"    --input audio.mp3 --output {output_path} --format srt")
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Video Extractor — Opensquad Skill",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--url", required=True, help="URL do vídeo")
    parser.add_argument(
        "--operation",
        required=True,
        choices=["download", "audio", "frames", "metadata", "transcript"],
        help="Operação a executar",
    )
    parser.add_argument("--output", required=True, help="Caminho de saída (arquivo ou pasta para frames)")
    parser.add_argument("--fps", type=float, default=1.0, help="Frames por segundo para operação 'frames' (padrão: 1)")
    parser.add_argument("--lang", default="pt", help="Idioma para transcrição (padrão: pt)")

    args = parser.parse_args()

    check_ytdlp()

    ops = {
        "download": lambda: download_video(args.url, args.output),
        "audio": lambda: extract_audio(args.url, args.output),
        "frames": lambda: extract_frames(args.url, args.output, args.fps),
        "metadata": lambda: get_metadata(args.url, args.output),
        "transcript": lambda: get_transcript(args.url, args.output, args.lang),
    }

    ops[args.operation]()


if __name__ == "__main__":
    main()
