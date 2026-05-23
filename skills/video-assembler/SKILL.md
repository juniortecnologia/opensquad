---
name: video-assembler
description: >
  Monta vídeos a partir de imagens + áudio + legendas usando FFmpeg e MoviePy.
  Aceita config JSON com cenas, narração, música de fundo e legendas.
  Presets por plataforma: YouTube (1920×1080), TikTok/Reels/Shorts (1080×1920).
  Saída: MP4 pronto para publicação via blotato.
description_pt-BR: >
  Monta vídeos de imagens + áudio + legendas via FFmpeg/MoviePy.
  Config JSON com cenas, narração, música e legendas. Presets por plataforma.
  Saída: MP4 pronto para publicação.
type: script
version: "1.0.0"
script:
  path: scripts/assemble_video.py
  runtime: python3
  invoke: "python3 {skill_path}/scripts/assemble_video.py --config \"{config}\" --output \"{output}\""
categories: [video, assembly, ffmpeg, moviepy, production, editing]
---

# Video Assembler

## When to use

Use o Video Assembler quando o pipeline tiver:
1. ✅ Imagens das cenas (PNG/JPG) geradas por local-image-gen ou image-ai-generator
2. ✅ Narração em MP3 gerada por local-tts
3. ✅ Legendas em SRT ou ASS geradas por subtitle-generator (opcional)
4. ✅ Música de fundo em MP3 (opcional)

**Pré-requisito obrigatório:** FFmpeg instalado no sistema.
Verifique com: `ffmpeg -version`
Instale com: `brew install ffmpeg` (macOS) ou `apt install ffmpeg` (Linux)

Instale também: `pip install moviepy ffmpeg-python`

## Config JSON

O agente deve criar um arquivo JSON de configuração antes de chamar o assembler:

```json
{
  "scenes": [
    {"image": "squads/{squad}/output/{run_id}/scenes/scene-01.png", "duration": 5},
    {"image": "squads/{squad}/output/{run_id}/scenes/scene-02.png", "duration": 4},
    {"image": "squads/{squad}/output/{run_id}/scenes/scene-03.png", "duration": 6}
  ],
  "audio": "squads/{squad}/output/{run_id}/narration.mp3",
  "subtitles": "squads/{squad}/output/{run_id}/subtitles.ass",
  "music": "squads/{squad}/output/{run_id}/background.mp3",
  "music_volume": 0.15,
  "platform": "tiktok",
  "transitions": "crossfade",
  "fade_duration": 0.3
}
```

Campos obrigatórios: `scenes`, `audio`, `platform`
Campos opcionais: `subtitles`, `music`, `music_volume` (padrão: 0.15), `transitions` (padrão: crossfade), `fade_duration` (padrão: 0.3)

## Presets de plataforma

| Platform | Resolução | FPS | Bitrate | Uso |
|----------|-----------|-----|---------|-----|
| `youtube` | 1920×1080 | 30 | 8M | YouTube vídeos longos |
| `shorts` | 1080×1920 | 30 | 6M | YouTube Shorts |
| `tiktok` | 1080×1920 | 30 | 6M | TikTok |
| `reels` | 1080×1920 | 30 | 6M | Instagram Reels |

## Instruções para o agente

### 1. Calcular duração de cada cena

A duração de cada cena deve coincidir com a narração daquele trecho.
Use a fórmula: `duração (s) = número de palavras ÷ 150 × 60`

Para vídeos com narração contínua:
- A soma das durações das cenas DEVE ser igual (ou maior em até 5%) que a duração do MP3 de narração
- Se a narração for mais longa, adicione a última cena com a duração restante

### 2. Criar config JSON

```bash
# O agente cria o arquivo manualmente com base no storyboard.yaml
# Exemplo de saída esperada: squads/{squad}/output/{run_id}/video-config.json
```

### 3. Montar o vídeo

```bash
python3 skills/video-assembler/scripts/assemble_video.py \
  --config "squads/{squad}/output/{run_id}/video-config.json" \
  --output "squads/{squad}/output/{run_id}/video/final-tiktok.mp4"
```

### 4. Verificar output

Após a montagem, verificar:
- Tamanho do arquivo > 0 MB
- Duração próxima do esperado (±5%)
- `ffprobe output.mp4` para confirmar resolução e codec

## Transitions disponíveis

- `crossfade` — Dissolve suave entre cenas (padrão, recomendado)
- `none` — Corte direto (mais dinâmico para TikTok)
- `fade` — Fade in/out preto entre cenas (mais formal, YouTube)

## Burn-in de legendas

Para formatos SRT, o assembler converte automaticamente para burn-in via FFmpeg.
Para ASS, aplica diretamente com estilização preservada.

**Legenda ASS recomendada para TikTok/Reels** — gerada pelo subtitle-generator com fonte grande.

## Error handling

- **FFmpeg não instalado:** mensagem clara com instrução de instalação
- **Imagem não encontrada:** lista as imagens faltantes e para a execução
- **Áudio mais longo que cenas:** estende a última cena automaticamente
- **Áudio mais curto que cenas:** corta o vídeo no fim do áudio
- **Formato de legenda inválido:** aviso e continua sem legendas
