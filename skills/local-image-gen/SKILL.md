---
name: local-image-gen
description: >
  Gera imagens localmente ou via APIs gratuitas, sem custo por imagem.
  Provider primário: diffusers com SDXL-turbo (MPS no M1, 1-4 steps, rápido).
  Alternativas: AUTOMATIC1111 (localhost:7860), ComfyUI (localhost:8188).
  Para qualidade de produção final, use image-ai-generator (pago, superior).
description_pt-BR: >
  Gera imagens localmente usando diffusers/SDXL-turbo (MPS no M1), AUTOMATIC1111 ou ComfyUI.
  Gratuito e sem limite. Use image-ai-generator para qualidade de produção.
type: script
version: "1.0.0"
script:
  path: scripts/generate_image_local.py
  runtime: python3
  invoke: "python3 {skill_path}/scripts/generate_image_local.py --prompt \"{prompt}\" --output \"{output}\" --provider \"{provider}\""
env:
  - LOCAL_IMAGE_PROVIDER
  - LOCAL_IMAGE_MODEL
categories: [images, ai, generation, local, free, video, scenes]
---

# Local Image Generator

## When to use

Use local-image-gen quando precisar gerar imagens para:
- **Cenas de vídeo** (storyboard → imagens reais)
- **Testes e iteração** antes de usar image-ai-generator (pago)
- **Geração em lote** onde custo seria proibitivo com API paga

**Quando usar image-ai-generator em vez desta skill:**
- Imagens de capa (thumbnails) para publicação — qualidade importa muito
- Quando o cliente pediu qualidade premium
- Quando a cena principal do vídeo precisa de máxima qualidade

Instale dependências: `pip install diffusers transformers accelerate torch`

**Para M1 8GB:** Use SDXL-turbo (padrão) — usa ~3-4GB de RAM via MPS (Metal).
Execute apenas uma geração por vez. Chame `--cleanup` após batch para liberar RAM.

## Providers disponíveis

### diffusers (padrão — SDXL-turbo, MPS no M1)
- **Gratuito:** Sim
- **Requer internet:** Apenas para download inicial do modelo (~2 GB)
- **Velocidade no M1:** ~15-30s por imagem
- **Qualidade:** Boa para iteração e cenas de vídeo
- **GPU:** MPS (Metal) no M1 automaticamente; CPU em outros sistemas

### auto1111 (AUTOMATIC1111 local)
- **Requer:** Servidor AUTOMATIC1111 rodando em http://localhost:7860
- **Acessa qualquer modelo SD** instalado no servidor
- **Qualidade:** Excelente (depende do modelo configurado)

### comfyui (ComfyUI local)
- **Requer:** ComfyUI rodando em http://localhost:8188
- **Flexível:** Suporta workflows customizados
- **Qualidade:** Excelente

## Presets de resolução por plataforma

| Plataforma | Resolução | Ratio | Argumento |
|------------|-----------|-------|-----------|
| TikTok / Reels / Shorts | 1080×1920 | 9:16 | `--preset vertical` |
| YouTube | 1920×1080 | 16:9 | `--preset youtube` |
| Instagram Feed / Thumbnail | 1080×1080 | 1:1 | `--preset square` |
| YouTube Thumbnail | 1280×720 | 16:9 | `--preset thumbnail` |

## Instruções para o agente

### Gerar imagem de cena (vertical para TikTok/Reels)
```bash
python3 skills/local-image-gen/scripts/generate_image_local.py \
  --prompt "Escritório moderno, profissional trabalhando em laptop, luz suave, fotorrealismo 4K" \
  --output "squads/{squad}/output/{run_id}/scenes/scene-01.png" \
  --preset vertical
```

### Gerar em lote (a partir de storyboard)
```bash
python3 skills/local-image-gen/scripts/generate_image_local.py \
  --batch "squads/{squad}/output/{run_id}/scenes-batch.json" \
  --preset vertical
```

Formato do JSON de batch:
```json
[
  {"prompt": "Cena 1: ...", "output": "scenes/scene-01.png"},
  {"prompt": "Cena 2: ...", "output": "scenes/scene-02.png"}
]
```

### Com AUTOMATIC1111 ou ComfyUI
```bash
python3 skills/local-image-gen/scripts/generate_image_local.py \
  --prompt "Cena de escritório..." \
  --output "scene.png" \
  --provider auto1111
```

## Guia de prompts para cenas de vídeo

Estrutura recomendada:
```
[Sujeito + ação], [ambiente], [iluminação], [estilo fotográfico], [qualidade técnica]
```

Exemplos bons:
- `"Jovem profissional sorrindo para câmera, escritório moderno com plantas, luz natural suave pela janela, fotografia editorial, 4K ultra-detalhado"`
- `"Smartphone na mão de uma pessoa, tela com gráficos de crescimento, fundo desfocado de cidade, fotorrealismo, perspectiva de primeiro plano"`

Regras:
- Sempre especifique estilo (fotorrealismo, ilustração vetorial, etc.)
- Nunca peça texto nas imagens (IA não renderiza texto bem)
- Mantenha o mesmo modificador de estilo em TODAS as cenas do mesmo vídeo

## Cost awareness

- **local-image-gen:** Totalmente gratuito (custo de eletricidade apenas)
- **image-ai-generator (test mode):** ~R$0.01-0.02 por imagem
- **image-ai-generator (production):** ~R$0.07-0.10 por imagem
- Para vídeos com 20 cenas: R$0 (local) vs ~R$1.40-2.00 (image-ai-generator production)

## Error handling

- **diffusers não instalado:** mensagem clara com comando de instalação
- **RAM insuficiente no M1:** sugestão de fechar outros apps ou usar auto1111 com modelo menor
- **auto1111/comfyui offline:** mensagem de erro com instrução para iniciar o servidor local
- **Modelo não baixado:** download automático na primeira execução (pode demorar ~5-15 min)
