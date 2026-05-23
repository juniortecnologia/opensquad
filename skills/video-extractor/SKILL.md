---
name: video-extractor
description: >
  Baixa e extrai conteúdo de plataformas de vídeo usando yt-dlp.
  Suporta YouTube, TikTok, Instagram, Twitter/X e 1000+ plataformas.
  Operações: download de vídeo (MP4), extração de áudio (MP3), captura de frames (PNG),
  obtenção de metadados (JSON) e transcrição automática quando disponível.
description_pt-BR: >
  Baixa e extrai conteúdo de plataformas de vídeo usando yt-dlp.
  Suporta YouTube, TikTok, Instagram, Twitter/X e 1000+ plataformas.
  Operações: download de vídeo (MP4), extração de áudio (MP3), captura de frames (PNG),
  metadados (JSON) e transcrição automática quando disponível.
type: script
version: "1.0.0"
script:
  path: scripts/extract_video.py
  runtime: python3
  invoke: "python3 {skill_path}/scripts/extract_video.py --url \"{url}\" --operation \"{operation}\" --output \"{output}\""
categories: [video, download, extraction, youtube, tiktok, repurposing]
---

# Video Extractor

## When to use

Use o Video Extractor para:
- **Baixar vídeos de referência** para análise de concorrentes ou repurposing
- **Extrair áudio** de vídeos para transcrição com subtitle-generator
- **Capturar frames** de vídeos para criar thumbnails ou storyboards
- **Obter metadados** (título, descrição, duração, tags) para pesquisa de SEO

**IMPORTANTE: Use somente para conteúdo público com uso permitido.** Nunca use para infringir direitos autorais. Vídeos protegidos por paywall ou privados não devem ser baixados sem autorização do criador.

Instale yt-dlp antes de usar: `pip install yt-dlp`

## Operações disponíveis

### `download` — Baixar vídeo completo (MP4)
```bash
python3 skills/video-extractor/scripts/extract_video.py \
  --url "https://www.youtube.com/watch?v=XXXXXXXXXXX" \
  --operation download \
  --output "squads/{squad}/output/{run_id}/video/source.mp4"
```

### `audio` — Extrair apenas o áudio (MP3)
```bash
python3 skills/video-extractor/scripts/extract_video.py \
  --url "https://www.youtube.com/watch?v=XXXXXXXXXXX" \
  --operation audio \
  --output "squads/{squad}/output/{run_id}/audio/source.mp3"
```

### `frames` — Capturar frames a cada N segundos (PNG)
```bash
python3 skills/video-extractor/scripts/extract_video.py \
  --url "https://www.youtube.com/watch?v=XXXXXXXXXXX" \
  --operation frames \
  --output "squads/{squad}/output/{run_id}/frames/" \
  --fps 1
```
Cria arquivos frame-000001.png, frame-000002.png, etc. na pasta especificada.

### `metadata` — Obter metadados do vídeo (JSON)
```bash
python3 skills/video-extractor/scripts/extract_video.py \
  --url "https://www.youtube.com/watch?v=XXXXXXXXXXX" \
  --operation metadata \
  --output "squads/{squad}/output/{run_id}/metadata.json"
```
Retorna: title, description, duration, view_count, like_count, tags, upload_date, channel.

### `transcript` — Obter transcrição automática (SRT/JSON)
```bash
python3 skills/video-extractor/scripts/extract_video.py \
  --url "https://www.youtube.com/watch?v=XXXXXXXXXXX" \
  --operation transcript \
  --output "squads/{squad}/output/{run_id}/transcript.srt"
```
Usa legendas automáticas do YouTube quando disponíveis. Se não houver legendas automáticas, retorna erro e instrui usar subtitle-generator no áudio extraído.

## Instruções para o agente

1. **Sempre verifique** se yt-dlp está instalado: `yt-dlp --version`
2. Para vídeos longos (>10 min), prefira `audio` + `subtitle-generator` em vez de `download` — é mais rápido e econômico em disco
3. O `metadata` não faz download do vídeo — é rápido e gratuito em termos de largura de banda
4. Para repurposing: use `download` + `audio` em sequência para ter ambos os arquivos
5. Após `frames`, selecione os frames mais representativos para análise (não use todos)
6. Reporte sempre o tamanho do arquivo gerado e o path completo

## Plataformas suportadas

YouTube, TikTok, Instagram (públicos), Twitter/X, Facebook (públicos), Vimeo, Reddit, Twitch VODs e 1000+ outras plataformas via yt-dlp.

## Qualidade de download

- Padrão: melhor qualidade disponível até 1080p (para economizar espaço)
- Para `audio`: sempre extrai como MP3 a 192kbps

## Error handling

- **yt-dlp não instalado:** script exibe instrução de instalação e sai com código 1
- **URL privada ou protegida:** mensagem clara de que o conteúdo não está acessível
- **Rate limit:** yt-dlp lida automaticamente com rate limits do YouTube; para outros sites, pode ser necessário aguardar
- **Vídeo indisponível:** mensagem de erro clara com o status retornado pela plataforma
