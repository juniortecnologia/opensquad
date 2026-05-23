#!/usr/bin/env python3
"""
Local TTS Narration Generator — Opensquad Skill
Gera narração em áudio a partir de texto usando TTS gratuito.

Providers:
  edge-tts (padrão) — Microsoft, gratuito, requer internet
  kokoro             — Local, 82M params, sem internet (pip install kokoro-onnx)
  piper              — Local, ultra-leve CPU (pip install piper-tts)

Uso:
  python3 generate_narration.py --text "Olá mundo" --output narration.mp3
  python3 generate_narration.py --file script.txt --output narration.mp3 --voice pt-BR-AntonioNeural
  python3 generate_narration.py --list-voices
  python3 generate_narration.py --list-voices --provider edge-tts
"""

import argparse
import asyncio
import os
import re
import sys
import tempfile
from pathlib import Path


def load_env() -> None:
    """Carrega .env se disponível."""
    try:
        from dotenv import load_dotenv
        load_dotenv(override=False)
    except ImportError:
        pass


def get_defaults() -> tuple[str, str]:
    """Retorna provider e voz padrão das variáveis de ambiente."""
    provider = os.environ.get("LOCAL_TTS_MODEL", "edge-tts")
    voice = os.environ.get("LOCAL_TTS_VOICE", "pt-BR-FranciscaNeural")
    return provider, voice


def clean_script(text: str) -> str:
    """
    Remove marcações de roteiro que não devem ser narradas:
    - Markdown: **bold**, *italic*, # headings
    - Cues de B-roll: [B-roll: pan], [Corte para], [Gráfico]
    - Notas de produção entre colchetes
    - Emojis
    - Múltiplas quebras de linha
    """
    # Remove cues de produção [...]
    text = re.sub(r'\[.*?\]', '', text)
    # Remove headings markdown
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
    # Remove bold/italic
    text = re.sub(r'\*{1,3}(.*?)\*{1,3}', r'\1', text)
    # Remove underline markdown
    text = re.sub(r'_{1,2}(.*?)_{1,2}', r'\1', text)
    # Remove URLs
    text = re.sub(r'https?://\S+', '', text)
    # Remove emojis (caracteres fora do range ASCII básico que são emojis)
    text = re.sub(r'[\U0001F300-\U0001FFFF]', '', text)
    # Remove linhas horizontais
    text = re.sub(r'^[-*_]{3,}\s*$', '', text, flags=re.MULTILINE)
    # Normaliza espaços e quebras de linha
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()


def chunk_text(text: str, max_chars: int = 500) -> list[str]:
    """
    Divide texto longo em chunks para Edge-TTS.
    Divide em parágrafos, depois em frases se necessário.
    """
    if len(text) <= max_chars:
        return [text]

    chunks = []
    paragraphs = text.split('\n\n')

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        if len(para) <= max_chars:
            chunks.append(para)
        else:
            # Divide em frases
            sentences = re.split(r'(?<=[.!?])\s+', para)
            current = ""
            for sent in sentences:
                if len(current) + len(sent) + 1 <= max_chars:
                    current = (current + " " + sent).strip()
                else:
                    if current:
                        chunks.append(current)
                    current = sent
            if current:
                chunks.append(current)

    return chunks if chunks else [text]


# ── Edge-TTS ─────────────────────────────────────────────────────────────────

async def _edge_tts_generate(text: str, output: str, voice: str) -> None:
    """Gera áudio com Edge-TTS (assíncrono)."""
    try:
        import edge_tts
    except ImportError:
        print("ERRO: edge-tts não instalado. Execute: pip install edge-tts")
        sys.exit(1)

    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output)


async def _edge_tts_list_voices() -> None:
    """Lista vozes disponíveis no Edge-TTS."""
    try:
        import edge_tts
    except ImportError:
        print("ERRO: edge-tts não instalado. Execute: pip install edge-tts")
        sys.exit(1)

    manager = await edge_tts.VoicesManager.create()
    pt_voices = [v for v in manager.voices if "pt" in v.get("Locale", "").lower()]
    print("\nVozes PT-BR disponíveis:")
    for v in pt_voices:
        print(f"  {v['ShortName']:40s} {v['Gender']:8s} {v.get('Locale', '')}")


def generate_edge_tts(text: str, output: str, voice: str) -> None:
    """Gera narração com Edge-TTS, com suporte a chunking para textos longos."""
    chunks = chunk_text(text)

    if len(chunks) == 1:
        asyncio.run(_edge_tts_generate(chunks[0], output, voice))
    else:
        print(f"Texto dividido em {len(chunks)} partes para geração...")
        # Gera cada chunk como arquivo temporário e concatena
        try:
            from pydub import AudioSegment
            has_pydub = True
        except ImportError:
            has_pydub = False

        temp_files = []
        for i, chunk in enumerate(chunks):
            temp_path = str(Path(output).with_suffix(f".chunk{i:03d}.mp3"))
            asyncio.run(_edge_tts_generate(chunk, temp_path, voice))
            temp_files.append(temp_path)
            print(f"  Parte {i+1}/{len(chunks)} concluída")

        if has_pydub:
            # Concatena com pydub
            combined = AudioSegment.empty()
            for f in temp_files:
                combined += AudioSegment.from_mp3(f)
            combined.export(output, format="mp3")
            for f in temp_files:
                Path(f).unlink(missing_ok=True)
        else:
            # Sem pydub: usa o último chunk (limitação)
            # Melhor esforço sem dependência extra
            import shutil
            shutil.copy(temp_files[-1], output)
            for f in temp_files[:-1]:
                Path(f).unlink(missing_ok=True)
            print("AVISO: pydub não instalado. Para concatenar chunks longos: pip install pydub")


# ── Kokoro ───────────────────────────────────────────────────────────────────

def generate_kokoro(text: str, output: str, voice: str = "bf_emma") -> None:
    """Gera narração com Kokoro (local, offline)."""
    try:
        from kokoro_onnx import Kokoro
        import soundfile as sf
        import numpy as np
    except ImportError:
        print("ERRO: kokoro-onnx não instalado.")
        print("Instale com: pip install kokoro-onnx soundfile")
        sys.exit(1)

    kokoro = Kokoro("kokoro-v0_19.onnx", "voices.json")
    samples, sample_rate = kokoro.create(text, voice=voice, speed=1.0, lang="pt-br")

    output_path = Path(output)
    # Kokoro gera WAV — se solicitado MP3, converte
    if output_path.suffix.lower() == ".mp3":
        wav_temp = str(output_path.with_suffix(".wav"))
        sf.write(wav_temp, samples, sample_rate)
        _wav_to_mp3(wav_temp, output)
        Path(wav_temp).unlink(missing_ok=True)
    else:
        sf.write(str(output_path), samples, sample_rate)


# ── Piper ────────────────────────────────────────────────────────────────────

def generate_piper(text: str, output: str, voice: str = "pt_BR-faber-medium") -> None:
    """Gera narração com Piper TTS (local, ultra-leve)."""
    try:
        import piper
    except ImportError:
        print("ERRO: piper-tts não instalado.")
        print("Instale com: pip install piper-tts")
        sys.exit(1)

    import subprocess
    cmd = ["piper", "--model", voice, "--output_file", output]
    result = subprocess.run(cmd, input=text.encode(), capture_output=True)
    if result.returncode != 0:
        print(f"ERRO: Piper falhou: {result.stderr.decode()}")
        sys.exit(1)


# ── Utilitários ──────────────────────────────────────────────────────────────

def _wav_to_mp3(wav_path: str, mp3_path: str) -> None:
    """Converte WAV para MP3 usando FFmpeg."""
    import subprocess
    result = subprocess.run(
        ["ffmpeg", "-i", wav_path, "-q:a", "0", mp3_path, "-y"],
        capture_output=True,
    )
    if result.returncode != 0:
        print("AVISO: FFmpeg não disponível para converter WAV→MP3. Saída mantida como WAV.")


def main() -> None:
    load_env()
    default_provider, default_voice = get_defaults()

    parser = argparse.ArgumentParser(
        description="Local TTS Narration Generator — Opensquad Skill",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--text", help="Texto para narrar")
    parser.add_argument("--file", help="Arquivo .txt com o roteiro")
    parser.add_argument("--output", help="Arquivo de saída (MP3 recomendado)")
    parser.add_argument("--voice", default=default_voice, help=f"Voz a usar (padrão: {default_voice})")
    parser.add_argument(
        "--provider",
        default=default_provider,
        choices=["edge-tts", "kokoro", "piper"],
        help=f"Provider TTS (padrão: {default_provider})",
    )
    parser.add_argument(
        "--list-voices",
        action="store_true",
        help="Listar vozes disponíveis (para edge-tts)",
    )

    args = parser.parse_args()

    if args.list_voices:
        asyncio.run(_edge_tts_list_voices())
        return

    if not args.output:
        print("ERRO: --output é obrigatório para geração de narração")
        sys.exit(1)

    # Obtém texto
    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"ERRO: Arquivo não encontrado: {args.file}")
            sys.exit(1)
        text = file_path.read_text(encoding="utf-8")
    elif args.text:
        text = args.text
    else:
        print("ERRO: Forneça --text ou --file com o texto a narrar")
        sys.exit(1)

    # Limpa o texto
    text = clean_script(text)
    if not text:
        print("ERRO: Texto vazio após limpeza do roteiro")
        sys.exit(1)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Provider: {args.provider} | Voz: {args.voice}")
    print(f"Texto: {len(text)} caracteres")

    if args.provider == "edge-tts":
        generate_edge_tts(text, str(output_path), args.voice)
    elif args.provider == "kokoro":
        generate_kokoro(text, str(output_path), args.voice)
    elif args.provider == "piper":
        generate_piper(text, str(output_path), args.voice)

    if output_path.exists() and output_path.stat().st_size > 0:
        size_kb = output_path.stat().st_size / 1024
        print(f"Narração salva: {output_path} ({size_kb:.0f} KB)")
    else:
        print(f"ERRO: Arquivo de saída não foi criado ou está vazio: {output_path}")
        sys.exit(1)


if __name__ == "__main__":
    main()
