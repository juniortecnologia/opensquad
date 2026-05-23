#!/usr/bin/env python3
"""
Local Image Generator — Opensquad Skill
Gera imagens localmente ou via APIs gratuitas.

Providers: diffusers (padrão, SDXL-turbo, MPS no M1), auto1111, comfyui

Uso:
  python3 generate_image_local.py --prompt "cena..." --output scene.png
  python3 generate_image_local.py --batch scenes.json --preset vertical
  python3 generate_image_local.py --prompt "..." --provider auto1111 --output out.png
"""

import argparse
import json
import os
import sys
from pathlib import Path

# Presets de resolução por plataforma
PRESETS = {
    "vertical":  {"width": 1080, "height": 1920},  # TikTok / Reels / Shorts
    "youtube":   {"width": 1920, "height": 1080},  # YouTube landscape
    "square":    {"width": 1080, "height": 1080},  # Instagram feed / square
    "thumbnail": {"width": 1280, "height": 720},   # YouTube thumbnail
    "custom":    None,                              # usa --width e --height
}


def load_env() -> None:
    try:
        from dotenv import load_dotenv
        load_dotenv(override=False)
    except ImportError:
        pass


def get_defaults() -> tuple[str, str]:
    provider = os.environ.get("LOCAL_IMAGE_PROVIDER", "diffusers")
    model = os.environ.get("LOCAL_IMAGE_MODEL", "stabilityai/sdxl-turbo")
    return provider, model


# ── diffusers (SDXL-turbo, MPS no M1) ───────────────────────────────────────

def generate_diffusers(prompt: str, output: str, width: int, height: int, model_id: str) -> None:
    """Gera imagem via HuggingFace diffusers com SDXL-turbo (MPS no M1)."""
    try:
        import torch
        from diffusers import AutoPipelineForText2Image
    except ImportError:
        print("ERRO: diffusers/torch não instalados.")
        print("Instale com: pip install diffusers transformers accelerate torch")
        sys.exit(1)

    # Detecta device: MPS (M1/M2), CUDA (NVIDIA) ou CPU
    if torch.backends.mps.is_available():
        device = "mps"
        dtype = torch.float16
        print("Usando MPS (Metal) — Apple Silicon")
    elif torch.cuda.is_available():
        device = "cuda"
        dtype = torch.float16
        print(f"Usando CUDA — {torch.cuda.get_device_name(0)}")
    else:
        device = "cpu"
        dtype = torch.float32
        print("Usando CPU (mais lento)")

    print(f"Carregando modelo: {model_id}")
    print("(Download automático na primeira execução — pode demorar ~5-15 min)")

    pipe = AutoPipelineForText2Image.from_pretrained(
        model_id,
        torch_dtype=dtype,
        use_safetensors=True,
        variant="fp16" if dtype == torch.float16 else None,
    ).to(device)

    # SDXL-turbo: 1-4 steps sem guidance_scale
    is_turbo = "turbo" in model_id.lower()
    gen_kwargs = {
        "prompt": prompt,
        "width": width,
        "height": height,
    }
    if is_turbo:
        gen_kwargs["num_inference_steps"] = 4
        gen_kwargs["guidance_scale"] = 0.0
    else:
        gen_kwargs["num_inference_steps"] = 30
        gen_kwargs["guidance_scale"] = 7.5

    print(f"Gerando imagem {width}×{height}...")
    image = pipe(**gen_kwargs).images[0]

    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(str(output_path))

    # Libera RAM no M1 (importante com 8GB)
    if device == "mps":
        import gc
        del pipe
        gc.collect()
        torch.mps.empty_cache()

    size_kb = output_path.stat().st_size / 1024
    print(f"Imagem salva: {output_path} ({size_kb:.0f} KB, {width}×{height}px)")


# ── AUTOMATIC1111 ─────────────────────────────────────────────────────────────

def generate_auto1111(
    prompt: str,
    output: str,
    width: int,
    height: int,
    url: str = "http://127.0.0.1:7860",
) -> None:
    """Gera imagem via AUTOMATIC1111 REST API (deve estar rodando localmente)."""
    import base64
    import urllib.request
    import urllib.error

    payload = {
        "prompt": prompt,
        "negative_prompt": "blurry, low quality, deformed, ugly, watermark",
        "width": width,
        "height": height,
        "steps": 28,
        "cfg_scale": 7,
        "sampler_name": "DPM++ 2M Karras",
    }

    api_url = f"{url}/sdapi/v1/txt2img"
    print(f"Enviando para AUTOMATIC1111 em {url}...")

    try:
        data = json.dumps(payload).encode()
        req = urllib.request.Request(
            api_url,
            data=data,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read())
    except urllib.error.URLError as e:
        print(f"ERRO: Não foi possível conectar ao AUTOMATIC1111 em {url}")
        print(f"  Verifique se o servidor está rodando: {e}")
        print("  Inicie com: cd stable-diffusion-webui && ./webui.sh --api")
        sys.exit(1)

    if not result.get("images"):
        print("ERRO: Nenhuma imagem na resposta do AUTOMATIC1111")
        sys.exit(1)

    img_data = base64.b64decode(result["images"][0])
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(img_data)

    size_kb = output_path.stat().st_size / 1024
    print(f"Imagem salva: {output_path} ({size_kb:.0f} KB, {width}×{height}px)")


# ── ComfyUI ──────────────────────────────────────────────────────────────────

def generate_comfyui(
    prompt: str,
    output: str,
    width: int,
    height: int,
    url: str = "http://127.0.0.1:8188",
) -> None:
    """Gera imagem via ComfyUI API (workflow simples de texto para imagem)."""
    import base64
    import json as _json
    import time
    import urllib.request
    import urllib.error
    import uuid

    # Workflow mínimo para txt2img no ComfyUI
    workflow = {
        "prompt": {
            "3": {"class_type": "KSampler", "inputs": {"cfg": 7, "denoise": 1, "latent_image": ["5", 0], "model": ["4", 0], "negative": ["7", 0], "positive": ["6", 0], "sampler_name": "euler", "scheduler": "normal", "seed": 42, "steps": 20}},
            "4": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "v1-5-pruned-emaonly.safetensors"}},
            "5": {"class_type": "EmptyLatentImage", "inputs": {"batch_size": 1, "height": height, "width": width}},
            "6": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["4", 1], "text": prompt}},
            "7": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["4", 1], "text": "bad quality, blurry, watermark"}},
            "8": {"class_type": "VAEDecode", "inputs": {"samples": ["3", 0], "vae": ["4", 2]}},
            "9": {"class_type": "SaveImage", "inputs": {"filename_prefix": "opensquad_", "images": ["8", 0]}},
        },
        "client_id": str(uuid.uuid4()),
    }

    print(f"Enviando para ComfyUI em {url}...")
    try:
        data = json.dumps(workflow).encode()
        req = urllib.request.Request(f"{url}/prompt", data=data, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
        prompt_id = result["prompt_id"]
    except urllib.error.URLError as e:
        print(f"ERRO: Não foi possível conectar ao ComfyUI em {url}: {e}")
        print("  Inicie o ComfyUI e tente novamente.")
        sys.exit(1)

    # Aguarda conclusão
    print("Aguardando geração no ComfyUI...")
    for _ in range(60):
        time.sleep(2)
        try:
            with urllib.request.urlopen(f"{url}/history/{prompt_id}", timeout=10) as resp:
                hist = json.loads(resp.read())
            if prompt_id in hist:
                outputs = hist[prompt_id].get("outputs", {})
                for node_output in outputs.values():
                    for img in node_output.get("images", []):
                        img_url = f"{url}/view?filename={img['filename']}&subfolder={img.get('subfolder','')}&type={img.get('type','output')}"
                        with urllib.request.urlopen(img_url) as img_resp:
                            img_data = img_resp.read()
                        output_path = Path(output)
                        output_path.parent.mkdir(parents=True, exist_ok=True)
                        output_path.write_bytes(img_data)
                        size_kb = len(img_data) / 1024
                        print(f"Imagem salva: {output_path} ({size_kb:.0f} KB)")
                        return
        except Exception:
            pass
    print("ERRO: Timeout aguardando ComfyUI. Verifique o servidor.")
    sys.exit(1)


# ── Batch ─────────────────────────────────────────────────────────────────────

def process_batch(batch_file: str, provider: str, model_id: str, preset: dict) -> None:
    """Processa um arquivo JSON de batch de imagens."""
    batch_path = Path(batch_file)
    if not batch_path.exists():
        print(f"ERRO: Arquivo de batch não encontrado: {batch_file}")
        sys.exit(1)

    items = json.loads(batch_path.read_text(encoding="utf-8"))
    print(f"Processando batch: {len(items)} imagens")

    success = 0
    for i, item in enumerate(items, 1):
        prompt = item.get("prompt", "")
        output = item.get("output", "")
        if not prompt or not output:
            print(f"  [{i}/{len(items)}] AVISO: item inválido (sem prompt ou output)")
            continue

        w = item.get("width", preset["width"])
        h = item.get("height", preset["height"])
        print(f"  [{i}/{len(items)}] Gerando: {Path(output).name}")

        try:
            _generate_single(prompt, output, provider, model_id, w, h)
            success += 1
        except SystemExit:
            print(f"  [{i}/{len(items)}] FALHOU")

    print(f"\nBatch concluído: {success}/{len(items)} imagens geradas")


def _generate_single(prompt: str, output: str, provider: str, model_id: str, width: int, height: int) -> None:
    """Gera uma única imagem com o provider especificado."""
    if provider == "diffusers":
        generate_diffusers(prompt, output, width, height, model_id)
    elif provider == "auto1111":
        generate_auto1111(prompt, output, width, height)
    elif provider == "comfyui":
        generate_comfyui(prompt, output, width, height)
    else:
        print(f"ERRO: Provider desconhecido: {provider}")
        sys.exit(1)


def main() -> None:
    load_env()
    default_provider, default_model = get_defaults()

    parser = argparse.ArgumentParser(
        description="Local Image Generator — Opensquad Skill",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--prompt", help="Prompt de geração de imagem")
    parser.add_argument("--output", help="Arquivo de saída PNG")
    parser.add_argument("--batch", help="Arquivo JSON de batch com lista de {prompt, output}")
    parser.add_argument(
        "--provider",
        default=default_provider,
        choices=["diffusers", "auto1111", "comfyui"],
        help=f"Provider de geração (padrão: {default_provider})",
    )
    parser.add_argument(
        "--model",
        default=default_model,
        help=f"Modelo para diffusers (padrão: {default_model})",
    )
    parser.add_argument(
        "--preset",
        default="vertical",
        choices=list(PRESETS.keys()),
        help="Preset de resolução (padrão: vertical = 1080×1920)",
    )
    parser.add_argument("--width", type=int, help="Largura em pixels (substitui preset)")
    parser.add_argument("--height", type=int, help="Altura em pixels (substitui preset)")

    args = parser.parse_args()

    # Resolve resolução
    if args.width and args.height:
        preset = {"width": args.width, "height": args.height}
    elif args.preset and args.preset != "custom":
        preset = PRESETS[args.preset]
    else:
        preset = PRESETS["vertical"]

    if args.batch:
        process_batch(args.batch, args.provider, args.model, preset)
    elif args.prompt and args.output:
        _generate_single(args.prompt, args.output, args.provider, args.model, preset["width"], preset["height"])
    else:
        print("ERRO: Forneça --prompt e --output, ou --batch com arquivo JSON")
        sys.exit(1)


if __name__ == "__main__":
    main()
