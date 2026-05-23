---
name: "Video Production Pipeline"
platform: "multi"
content_type: "production"
description: "Guia do pipeline completo de produção de vídeo: storyboard → cenas → narração → montagem → legendas. Cobre tools, timings, configurações por plataforma e quality gates."
whenToUse: |
  Criando agentes que executam o pipeline completo de produção de vídeo.
  Para roteiros, ver youtube-script.md. Para SEO, ver youtube-seo.md.
  Para TikTok específico, ver tiktok-video.md.
version: "1.0.0"
---

# Video Production Pipeline

## Visão Geral do Pipeline

```
Roteiro aprovado
    │
    ▼
[Storyboarder] → storyboard.yaml
    │
    ├──▶ [Narrator] → narration.mp3 (local-tts)
    │
    └──▶ [Scene Designer] → scenes/*.png (local-image-gen ou image-ai-generator)
                │
                ▼
         [Video Editor] → video-config.json
                │
                ├──▶ [Subtitle Generator] → subtitles.srt/.ass (subtitle-generator)
                │
                └──▶ [Video Assembler] → final-{platform}.mp4 (video-assembler)
                                │
                                ▼
                         [Thumbnail Creator] → thumbnail.png
                                │
                                ▼
                         [Publisher] → publicado ✓
```

## Fase 1: Storyboard

### O que é um storyboard neste contexto
Não é um storyboard de Hollywood. É uma lista estruturada de cenas com:
- **Narração** de cada cena (trecho exato do roteiro para aquele momento)
- **Prompt de imagem** para gerar a visual da cena
- **Duração estimada** em segundos
- **Texto on-screen** (opcional — text overlay que aparece no vídeo)
- **Tipo de transição** para a próxima cena

### Calculando a duração de cada cena

**Fórmula para PT-BR:**
```
duração (s) = (número de palavras ÷ 150) × 60 × 1.1
```
- 150 palavras/minuto = velocidade natural de fala em PT-BR
- × 1.1 = margem de 10% para pausas naturais

**Exemplos:**
- 25 palavras → ~11s
- 40 palavras → ~16s
- 15 palavras → ~7s

### Regra de ouro para cenas
- **1 cena = 1 beat narrativo** (uma ideia, um dado, uma emoção)
- Vídeo de 60s → 8-15 cenas
- Vídeo de 5 min → 30-50 cenas (use cenas "de transição" para manter ritmo)
- **Nunca menos de 3s por cena** — muito rápido para processar visualmente

### Formato do storyboard.yaml
```yaml
storyboard:
  video_title: "Título do Vídeo"
  platform: "tiktok"          # youtube | tiktok | reels | shorts
  total_duration_target: 45   # segundos alvo
  visual_style: "fotorrealismo 4K, iluminação suave de estúdio, paleta azul e branca"
  
  scenes:
    - scene: 1
      narration: "71% dos profissionais usam IA sem contar para o chefe."
      duration_seconds: 6
      image_prompt: "Profissional discreto olhando tela de laptop em escritório moderno, expressão de segredo, iluminação suave, fotorrealismo 4K, 9:16 vertical"
      text_overlay: "71% escondem o uso de IA"
      transition: crossfade
      notes: "Cena âncora — o dado principal do hook"

    - scene: 2
      narration: "E os que assumem têm 3x mais promoções."
      duration_seconds: 5
      image_prompt: "Profissional confiante apresentando resultados em reunião, gráfico de crescimento na tela atrás, iluminação de estúdio corporativo, fotorrealismo 4K, 9:16 vertical"
      text_overlay: "3x mais promoções"
      transition: crossfade
```

**IMPORTANTE:** O campo `visual_style` deve ser copiado LITERALMENTE no `image_prompt` de cada cena para manter consistência visual.

## Fase 2: Geração de Imagens de Cena

### Consistência de estilo
Defina um "descriptor de estilo" único no começo e use em TODAS as cenas:
```
"fotorrealismo 4K, iluminação suave, cores quentes, fundo desfocado, câmera de 85mm"
```

**Nunca misture estilos** (ex: fotorrealismo em umas cenas e ilustração em outras — parece amador).

### Orientação de prompts por plataforma
- **TikTok/Reels/Shorts:** sempre `9:16 vertical, 1080×1920`
- **YouTube:** sempre `16:9 horizontal, 1920×1080`

### Fluxo de geração
1. Gere a cena 1 primeiro para validar o estilo
2. Mostre ao usuário antes de gerar todas as cenas
3. Se aprovado, gere o restante em batch via `--batch`
4. **local-image-gen** para iteração e validação
5. **image-ai-generator** (production) para cenas principais do vídeo final

## Fase 3: Geração de Narração

### Pré-processamento do roteiro
Antes de chamar local-tts, limpe o texto:
```python
# Remover cues de produção: [B-roll: escritório] → ""
# Remover headings markdown: ## Seção → ""
# Remover bold/italic: **texto** → "texto"
# Remover URLs
# Adicionar pontuação em frases sem ela
```

O script `generate_narration.py` faz isso automaticamente.

### Configurações de voz por plataforma

**YouTube (vídeos longos):**
- Voz: `pt-BR-AntonioNeural` (masculino, mais formal) ou `pt-BR-FranciscaNeural` (feminina, clara)
- Tom: mais pausado, didático, com entonação variada

**TikTok/Reels (curtos):**
- Voz: `pt-BR-ThalitaNeural` (mais energética, jovem) ou `pt-BR-FranciscaNeural`
- Tom: mais rápido, energia alta, direto

### Verificação da narração
Após gerar o MP3:
```bash
# Verificar duração
ffprobe -v quiet -print_format json -show_streams narration.mp3 | python3 -c "
import json,sys; s=json.load(sys.stdin)['streams']; 
[print(f'Duração: {float(x[\"duration\"]):.1f}s') for x in s if x.get('codec_type')=='audio']"
```

A duração da narração é a "duração verdadeira" do vídeo. Ajuste as durações de cena no storyboard para somar ±5% da duração da narração.

## Fase 4: Geração de Legendas

### Quando gerar legendas
- **TikTok/Reels/Shorts:** SEMPRE — burn-in obrigatório
- **YouTube:** SRT para upload na plataforma (não burn-in)

### Comando para legendas de narração
```bash
python3 skills/subtitle-generator/scripts/generate_subtitles.py \
  --input narration.mp3 \
  --output subtitles.ass \       # ass para TikTok/Reels (burn-in)
  --format ass \
  --language pt
```

```bash
python3 skills/subtitle-generator/scripts/generate_subtitles.py \
  --input narration.mp3 \
  --output subtitles.srt \       # srt para YouTube (upload)
  --format srt \
  --language pt
```

### Modelo recomendado para M1 8GB
Use `base` (padrão). Nunca `large`. O modelo é baixado automaticamente na primeira execução.

## Fase 5: Montagem de Vídeo

### Criando o video-config.json
O agente de edição de vídeo deve criar este arquivo a partir do storyboard.yaml:

```json
{
  "scenes": [
    {"image": "squads/meu-squad/output/2026-05-02-120000/scenes/scene-01.png", "duration": 6},
    {"image": "squads/meu-squad/output/2026-05-02-120000/scenes/scene-02.png", "duration": 5}
  ],
  "audio": "squads/meu-squad/output/2026-05-02-120000/narration.mp3",
  "subtitles": "squads/meu-squad/output/2026-05-02-120000/subtitles.ass",
  "music": null,
  "music_volume": 0.15,
  "platform": "tiktok",
  "transitions": "crossfade",
  "fade_duration": 0.3
}
```

### Montagem
```bash
python3 skills/video-assembler/scripts/assemble_video.py \
  --config video-config.json \
  --output squads/meu-squad/output/2026-05-02-120000/video/final-tiktok.mp4
```

## Configurações de Exportação por Plataforma

| Plataforma | Resolução | FPS | Codec | Bitrate | Áudio |
|------------|-----------|-----|-------|---------|-------|
| YouTube | 1920×1080 | 30 | H.264 | 8 Mbps | AAC 192k |
| YouTube Shorts | 1080×1920 | 30 | H.264 | 6 Mbps | AAC 192k |
| TikTok | 1080×1920 | 30 | H.264 | 6 Mbps | AAC 192k |
| Instagram Reels | 1080×1920 | 30 | H.264 | 6 Mbps | AAC 192k |

Todos estes presets estão configurados no `video-assembler` automaticamente.

## Quality Gate — Antes de Publicar

Verifique:
- [ ] Duração do vídeo final dentro de ±10% do alvo
- [ ] Resolução correta para a plataforma (use `ffprobe final.mp4`)
- [ ] Áudio normalizado — não muito alto, não muito baixo
- [ ] Legendas legíveis — verifique a 1/4 do tamanho da tela
- [ ] Thumbnail legível a 200px de largura
- [ ] Sem frames pretos no início ou fim (além do fade esperado)

### Verificação com ffprobe
```bash
ffprobe -v quiet -print_format json -show_streams final.mp4 | python3 -c "
import json,sys; data=json.load(sys.stdin)
for s in data['streams']:
  if s.get('codec_type')=='video':
    print(f\"Vídeo: {s['width']}x{s['height']}, {s['r_frame_rate']}fps, duração: {float(s['duration']):.1f}s\")
  elif s.get('codec_type')=='audio':
    print(f\"Áudio: {s['codec_name']}, {s.get('sample_rate','?')}Hz\")"
```

## Convenção de Nomes de Arquivo

```
squads/{squad-code}/output/{YYYY-MM-DD-HHmmss}/
├── script.md                    # Roteiro aprovado
├── storyboard.yaml              # Storyboard com cenas
├── narration.mp3                # Narração gerada
├── subtitles.srt                # Legendas para upload
├── subtitles.ass                # Legendas para burn-in
├── scenes/
│   ├── scene-01.png
│   ├── scene-02.png
│   └── ...
├── video-config.json            # Configuração de montagem
├── video/
│   └── final-tiktok.mp4        # Vídeo final
├── thumbnail.png                # Thumbnail
└── seo-package.yaml            # Pacote de SEO
```

## Anti-patterns

- ❌ Narração sem limpeza de markdown (o TTS lê os asteriscos)
- ❌ Cenas muito curtas (<3s) — não dá tempo de processar
- ❌ Cenas muito longas (>12s) sem movimento — parece vídeo parado
- ❌ Misturar estilos visuais entre cenas (fotorrealismo + cartoon)
- ❌ Música de fundo muito alta (>20%) — cobre a narração
- ❌ Legenda sem burn-in para TikTok/Reels (40% dos usuários têm som baixo)
- ❌ Não verificar duração com ffprobe após montagem
- ❌ Thumbnail criada sem verificar legibilidade a 200px
