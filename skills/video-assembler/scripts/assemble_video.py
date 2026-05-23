#!/usr/bin/env python3
"""
Video Assembler — Opensquad Skill
Monta vídeos a partir de imagens + áudio + legendas usando FFmpeg e MoviePy.

Config JSON:
{
  "scenes": [{"image": "scene-01.png", "duration": 5}, ...],
  "audio": "narration.mp3",
  "subtitles": "subs.ass",       (opcional)
  "music": "background.mp3",     (opcional)
  "music_volume": 0.15,
  "platform": "tiktok",          (youtube | tiktok | reels | shorts)
  "transitions": "crossfade",    (crossfade | none | fade)
  "fade_duration": 0.3
}

Uso:
  python3 assemble_video.py --config video-config.json --output final.mp4
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

# Presets de exportação por plataforma
PLATFORM_PRESETS = {
    "youtube": {"width": 1920, "height": 1080, "fps": 30, "bitrate": "8M", "audio_bitrate": "192k"},
    "shorts":  {"width": 1080, "height": 1920, "fps": 30, "bitrate": "6M", "audio_bitrate": "192k"},
    "tiktok":  {"width": 1080, "height": 1920, "fps": 30, "bitrate": "6M", "audio_bitrate": "192k"},
    "reels":   {"width": 1080, "height": 1920, "fps": 30, "bitrate": "6M", "audio_bitrate": "192k"},
}


def check_ffmpeg() -> None:
    """Verifica se FFmpeg está instalado."""
    try:
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        version = result.stdout.decode().split("\n")[0]
        print(f"FFmpeg: {version[:50]}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("ERRO: FFmpeg não encontrado.")
        print("Instale com:")
        print("  macOS: brew install ffmpeg")
        print("  Linux: sudo apt install ffmpeg")
        sys.exit(1)


def check_moviepy() -> None:
    """Verifica se MoviePy está instalado."""
    try:
        import moviepy  # noqa: F401
    except ImportError:
        print("ERRO: moviepy não instalado.")
        print("Instale com: pip install moviepy")
        sys.exit(1)


def load_config(config_path: str) -> dict:
    """Carrega e valida o arquivo de config JSON."""
    path = Path(config_path)
    if not path.exists():
        print(f"ERRO: Config não encontrada: {config_path}")
        sys.exit(1)

    config = json.loads(path.read_text(encoding="utf-8"))

    # Validação mínima
    if "scenes" not in config or not config["scenes"]:
        print("ERRO: Config deve conter 'scenes' com pelo menos uma cena")
        sys.exit(1)
    if "audio" not in config:
        print("ERRO: Config deve conter 'audio' com o path da narração")
        sys.exit(1)
    if "platform" not in config:
        print("AVISO: 'platform' não especificado, usando 'tiktok'")
        config["platform"] = "tiktok"

    return config


def validate_files(config: dict) -> None:
    """Verifica se todos os arquivos referenciados existem."""
    missing = []

    for i, scene in enumerate(config["scenes"]):
        img_path = Path(scene["image"])
        if not img_path.exists():
            missing.append(f"  Cena {i+1}: {scene['image']}")

    audio_path = Path(config["audio"])
    if not audio_path.exists():
        missing.append(f"  Áudio: {config['audio']}")

    if config.get("subtitles"):
        subs_path = Path(config["subtitles"])
        if not subs_path.exists():
            print(f"AVISO: Arquivo de legendas não encontrado: {config['subtitles']}")
            print("  Continuando sem legendas...")
            config["subtitles"] = None

    if config.get("music"):
        music_path = Path(config["music"])
        if not music_path.exists():
            print(f"AVISO: Arquivo de música não encontrado: {config['music']}")
            config["music"] = None

    if missing:
        print("ERRO: Arquivos não encontrados:")
        for m in missing:
            print(m)
        sys.exit(1)


def get_audio_duration(audio_path: str) -> float:
    """Obtém a duração do áudio em segundos via ffprobe."""
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_streams", audio_path],
        capture_output=True,
        text=True,
    )
    info = json.loads(result.stdout)
    for stream in info.get("streams", []):
        if stream.get("codec_type") == "audio":
            return float(stream.get("duration", 0))
    return 0.0


def create_slideshow(scenes: list, preset: dict, transitions: str, fade_duration: float, temp_dir: str) -> str:
    """
    Cria slideshow de imagens como vídeo mudo usando FFmpeg.
    Retorna path do arquivo de vídeo temporário.
    """
    from moviepy.editor import ImageClip, concatenate_videoclips

    width = preset["width"]
    height = preset["height"]
    fps = preset["fps"]

    clips = []
    for scene in scenes:
        img_path = scene["image"]
        duration = float(scene.get("duration", 5))

        clip = ImageClip(img_path, duration=duration)

        # Redimensiona mantendo aspecto (preenche com crop central)
        clip = clip.resize(height=height)
        if clip.w < width:
            clip = clip.resize(width=width)
        # Crop central para fit exato
        clip = clip.crop(
            x_center=clip.w / 2,
            y_center=clip.h / 2,
            width=width,
            height=height,
        )

        # Fade in/out para crossfade
        if transitions == "crossfade" and fade_duration > 0:
            clip = clip.crossfadein(fade_duration)
        elif transitions == "fade" and fade_duration > 0:
            clip = clip.fadein(fade_duration).fadeout(fade_duration)

        clips.append(clip)

    if transitions == "crossfade" and fade_duration > 0:
        video = concatenate_videoclips(clips, method="compose", padding=-fade_duration)
    else:
        video = concatenate_videoclips(clips, method="compose")

    video = video.set_fps(fps)

    # Exporta vídeo mudo temporário
    slideshow_path = str(Path(temp_dir) / "slideshow_muted.mp4")
    print(f"Exportando slideshow ({len(clips)} cenas, {video.duration:.1f}s)...")
    video.write_videofile(
        slideshow_path,
        fps=fps,
        codec="libx264",
        audio=False,
        logger=None,
        verbose=False,
    )

    return slideshow_path


def mix_audio(narration: str, music: str | None, music_volume: float, duration: float, temp_dir: str) -> str:
    """Mixa narração com música de fundo (se fornecida) usando FFmpeg."""
    output_path = str(Path(temp_dir) / "audio_mixed.mp3")

    if music:
        # Mixa narração (100%) + música (volume reduzido) com duração da narração
        cmd = [
            "ffmpeg",
            "-i", narration,
            "-stream_loop", "-1", "-i", music,
            "-filter_complex",
            f"[1:a]volume={music_volume}[bg]; [0:a][bg]amix=inputs=2:duration=first:dropout_transition=2[out]",
            "-map", "[out]",
            "-t", str(duration),
            "-c:a", "libmp3lame",
            "-q:a", "2",
            output_path,
            "-y",
        ]
    else:
        # Apenas copia a narração
        cmd = [
            "ffmpeg",
            "-i", narration,
            "-t", str(duration),
            "-c:a", "libmp3lame",
            "-q:a", "2",
            output_path,
            "-y",
        ]

    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        print("AVISO: Falha na mixagem de áudio, usando narração sem música")
        return narration

    return output_path


def combine_video_audio(slideshow: str, audio: str, preset: dict, output: str) -> None:
    """Combina vídeo mudo com áudio usando FFmpeg."""
    cmd = [
        "ffmpeg",
        "-i", slideshow,
        "-i", audio,
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", preset["audio_bitrate"],
        "-shortest",
        output,
        "-y",
    ]
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        print("ERRO: Falha ao combinar vídeo e áudio")
        print(result.stderr.decode()[-500:])
        sys.exit(1)


def burn_subtitles(video_input: str, subtitles: str | None, preset: dict, output: str) -> None:
    """Aplica burn-in de legendas via FFmpeg."""
    if not subtitles:
        # Sem legendas — apenas re-encode com preset correto
        cmd = [
            "ffmpeg",
            "-i", video_input,
            "-c:v", "libx264",
            "-b:v", preset["bitrate"],
            "-c:a", "copy",
            output,
            "-y",
        ]
    else:
        subs_path = str(Path(subtitles).resolve())
        ext = Path(subtitles).suffix.lower()

        if ext == ".ass":
            # ASS: usa filtro ass (preserva estilo)
            subs_filter = f"ass='{subs_path}'"
        else:
            # SRT/VTT: usa subtitles com force_style para fonte grande
            subs_filter = (
                f"subtitles='{subs_path}':force_style="
                f"'FontName=Arial,FontSize=60,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,"
                f"BorderStyle=1,Outline=3,Shadow=1,Alignment=2'"
            )

        cmd = [
            "ffmpeg",
            "-i", video_input,
            "-vf", subs_filter,
            "-c:v", "libx264",
            "-b:v", preset["bitrate"],
            "-c:a", "copy",
            output,
            "-y",
        ]

    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        print("AVISO: Falha ao aplicar legendas")
        print(result.stderr.decode()[-300:])
        # Tenta sem legendas como fallback
        if subtitles:
            print("Continuando sem legendas...")
            burn_subtitles(video_input, None, preset, output)


def main() -> None:
    check_ffmpeg()
    check_moviepy()

    parser = argparse.ArgumentParser(
        description="Video Assembler — Opensquad Skill",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--config", required=True, help="Arquivo JSON de configuração")
    parser.add_argument("--output", required=True, help="Arquivo MP4 de saída")

    args = parser.parse_args()

    print("\n=== Video Assembler — Opensquad ===\n")

    config = load_config(args.config)
    validate_files(config)

    platform = config.get("platform", "tiktok").lower()
    if platform not in PLATFORM_PRESETS:
        print(f"AVISO: Plataforma '{platform}' desconhecida, usando 'tiktok'")
        platform = "tiktok"
    preset = PLATFORM_PRESETS[platform]

    transitions = config.get("transitions", "crossfade")
    fade_duration = float(config.get("fade_duration", 0.3))
    music_volume = float(config.get("music_volume", 0.15))

    print(f"Plataforma: {platform} ({preset['width']}×{preset['height']}, {preset['fps']}fps)")
    print(f"Cenas: {len(config['scenes'])}")
    print(f"Transições: {transitions}")

    # Obtém duração da narração
    audio_duration = get_audio_duration(config["audio"])
    print(f"Duração da narração: {audio_duration:.1f}s")

    # Ajusta durações das cenas para cobrir o áudio
    scenes = config["scenes"]
    total_scene_duration = sum(float(s.get("duration", 5)) for s in scenes)

    if total_scene_duration < audio_duration:
        # Estende a última cena para cobrir o áudio
        extra = audio_duration - total_scene_duration + 0.5  # margem de 0.5s
        scenes[-1]["duration"] = float(scenes[-1].get("duration", 5)) + extra
        print(f"Última cena estendida em {extra:.1f}s para cobrir narração")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as temp_dir:
        # 1. Cria slideshow
        print("\n[1/4] Criando slideshow de imagens...")
        slideshow_path = create_slideshow(scenes, preset, transitions, fade_duration, temp_dir)

        # 2. Mixa áudio
        print("\n[2/4] Mixando áudio...")
        mixed_audio = mix_audio(
            config["audio"],
            config.get("music"),
            music_volume,
            audio_duration,
            temp_dir,
        )

        # 3. Combina vídeo + áudio
        print("\n[3/4] Combinando vídeo e áudio...")
        combined_path = str(Path(temp_dir) / "combined.mp4")
        combine_video_audio(slideshow_path, mixed_audio, preset, combined_path)

        # 4. Burn-in legendas + exportação final
        print("\n[4/4] Aplicando legendas e exportando...")
        burn_subtitles(combined_path, config.get("subtitles"), preset, str(output_path))

    if output_path.exists() and output_path.stat().st_size > 0:
        size_mb = output_path.stat().st_size / (1024 * 1024)
        # Obtém duração real do vídeo final
        dur = get_audio_duration(str(output_path))
        print(f"\n✓ Vídeo montado: {output_path}")
        print(f"  Resolução: {preset['width']}×{preset['height']}")
        print(f"  Duração: {dur:.1f}s")
        print(f"  Tamanho: {size_mb:.1f} MB")
    else:
        print(f"\nERRO: Arquivo de saída não criado: {output_path}")
        sys.exit(1)


if __name__ == "__main__":
    main()
