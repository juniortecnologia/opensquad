---
name: subtitle-generator
description: >
  Gera legendas a partir de áudio ou vídeo usando faster-whisper (local, gratuito).
  Suporta PT-BR e 99+ idiomas. Formatos de saída: SRT (upload), VTT (web),
  ASS (burn-in estilizado para redes sociais com fonte grande centralizada).
  Otimizado para MacBook Air M1 com device="auto" e compute_type="int8".
description_pt-BR: >
  Gera legendas a partir de áudio ou vídeo usando faster-whisper (local, gratuito).
  Suporta PT-BR e 99+ idiomas. Formatos: SRT (upload), VTT (web),
  ASS (burn-in estilizado para redes sociais). Otimizado para M1 com int8.
type: script
version: "1.0.0"
script:
  path: scripts/generate_subtitles.py
  runtime: python3
  invoke: "python3 {skill_path}/scripts/generate_subtitles.py --input \"{input}\" --output \"{output}\" --format \"{format}\" --language \"{language}\""
env:
  - WHISPER_MODEL_SIZE
categories: [subtitles, transcription, whisper, video, accessibility, local]
---

# Subtitle Generator

## When to use

Use o Subtitle Generator quando o pipeline precisar de:
- **Legendas para burn-in:** use formato `ass` antes de chamar video-assembler
- **Legendas para upload:** use formato `srt` (YouTube, TikTok, Instagram)
- **Transcrição de conteúdo:** use `srt` ou `json` para análise de texto de vídeos

Instale faster-whisper antes de usar: `pip install faster-whisper`

**Nota de download:** Na primeira execução, o modelo Whisper é baixado automaticamente:
- `tiny`: ~75 MB, mais rápido, menos preciso
- `base`: ~145 MB, boa precisão para PT-BR (padrão)
- `small`: ~465 MB, melhor precisão, mais lento

**Nunca use `large` em 8GB RAM** — causará travamento do sistema.

## Formatos de saída

### SRT — Para upload em plataformas
Padrão da indústria. Aceito pelo YouTube, TikTok, Instagram, e praticamente toda plataforma.
```
1
00:00:00,000 --> 00:00:02,500
Olá, bem-vindo ao canal!

2
00:00:02,800 --> 00:00:05,200
Hoje vamos falar sobre IA.
```

### VTT — Para web players
WebVTT, similar ao SRT mas para players HTML5.

### ASS — Para burn-in estilizado (TikTok/Reels padrão)
Fonte grande centralizada na base da tela, estilo padrão para vídeos virais.
O video-assembler aplica automaticamente com FFmpeg.

## Instruções para o agente

### Gerar legendas em SRT (padrão)
```bash
python3 skills/subtitle-generator/scripts/generate_subtitles.py \
  --input "squads/{squad}/output/{run_id}/narration.mp3" \
  --output "squads/{squad}/output/{run_id}/subtitles.srt" \
  --format srt \
  --language pt
```

### Gerar legendas ASS para burn-in (TikTok/Reels)
```bash
python3 skills/subtitle-generator/scripts/generate_subtitles.py \
  --input "squads/{squad}/output/{run_id}/narration.mp3" \
  --output "squads/{squad}/output/{run_id}/subtitles.ass" \
  --format ass \
  --language pt
```

### Com modelo específico
```bash
python3 skills/subtitle-generator/scripts/generate_subtitles.py \
  --input audio.mp3 \
  --output subs.srt \
  --format srt \
  --language pt \
  --model small
```

### A partir de arquivo de vídeo
```bash
python3 skills/subtitle-generator/scripts/generate_subtitles.py \
  --input "video.mp4" \
  --output "subs.srt" \
  --format srt
```

## Modelos disponíveis (via WHISPER_MODEL_SIZE)

| Modelo | Tamanho | RAM  | Qualidade PT-BR | Quando usar |
|--------|---------|------|-----------------|-------------|
| tiny   | 75 MB   | ~1GB | Básica          | Testes rápidos |
| base   | 145 MB  | ~1GB | Boa             | Padrão (recomendado) |
| small  | 465 MB  | ~2GB | Melhor          | Quando base não for suficiente |

## Estilo ASS para redes sociais

O formato ASS gerado por esta skill usa:
- Fonte: **Arial Bold** 60px (legível na miniatura)
- Cor: Branco puro com contorno preto 3px
- Posição: Centralizado na parte inferior (margem 10%)
- Resolução: 1080×1920 (vertical para TikTok/Reels/Shorts)

Para YouTube (horizontal), use `--resolution youtube` para ajustar para 1920×1080.

## Error handling

- **faster-whisper não instalado:** mensagem clara com comando de instalação
- **Arquivo não encontrado:** mensagem de erro com path completo
- **Modelo não disponível:** download automático na primeira execução (pode demorar)
- **Idioma não detectado:** use `--language pt` explicitamente para PT-BR
- **RAM insuficiente:** use modelo menor (tiny > base > small)
