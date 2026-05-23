---
name: local-tts
description: >
  Gera narração em áudio a partir de texto usando TTS gratuito.
  Provider primário: Edge-TTS (Microsoft, gratuito, online, zero GPU, PT-BR nativo).
  Alternativas locais: Kokoro (82M params, cabe em M1), Piper (ultra-leve, CPU).
  Saída: arquivo MP3 pronto para uso no video-assembler.
description_pt-BR: >
  Gera narração em áudio a partir de texto usando TTS gratuito.
  Primário: Edge-TTS (Microsoft, gratuito, PT-BR nativo). Alternativas: Kokoro, Piper.
  Saída: MP3 pronto para video-assembler.
type: script
version: "1.0.0"
script:
  path: scripts/generate_narration.py
  runtime: python3
  invoke: "python3 {skill_path}/scripts/generate_narration.py --text \"{text}\" --output \"{output}\""
env:
  - LOCAL_TTS_MODEL
  - LOCAL_TTS_VOICE
categories: [audio, tts, narration, video, local, free]
---

# Local TTS — Gerador de Narração

## When to use

Use local-tts quando o pipeline precisar gerar narração em áudio para vídeos. Priorize Edge-TTS em quase todos os casos — é gratuito, não usa GPU, não requer instalação pesada e tem voz PT-BR de alta qualidade.

Instale Edge-TTS antes de usar: `pip install edge-tts`

**Atenção:** Edge-TTS requer conexão com a internet (envia texto para servidores Microsoft e recebe MP3). Para uso offline, use `--provider kokoro` ou `--provider piper`.

## Providers disponíveis

### Edge-TTS (padrão — recomendado)
- **Gratuito:** Sim (sem API key, sem cobrança)
- **Requer internet:** Sim
- **Qualidade:** Excelente — voz neural natural
- **GPU necessária:** Não
- **Instalação:** `pip install edge-tts`

### Kokoro (local, sem internet)
- **Gratuito:** Sim
- **Requer internet:** Não
- **Qualidade:** Muito boa (82M params)
- **GPU necessária:** Não (M1 usa MPS automaticamente)
- **Instalação:** `pip install kokoro-onnx soundfile`

### Piper (local, ultra-leve)
- **Gratuito:** Sim
- **Requer internet:** Apenas para download inicial do modelo
- **Qualidade:** Boa (voz sintetizada)
- **GPU necessária:** Não
- **Instalação:** `pip install piper-tts`

## Vozes PT-BR disponíveis (Edge-TTS)

| Voz | Gênero | Características |
|-----|--------|-----------------|
| `pt-BR-FranciscaNeural` | Feminina | Clara, profissional, natural (padrão) |
| `pt-BR-AntonioNeural` | Masculino | Direto, confiante, bom para tech |
| `pt-BR-ThalitaNeural` | Feminina | Jovem, animada, boa para TikTok |
| `pt-BR-DonatoNeural` | Masculino | Mais formal, bom para documentários |

Liste todas as vozes disponíveis:
```bash
python3 skills/local-tts/scripts/generate_narration.py --list-voices
```

## Instruções para o agente

### Narração simples (Edge-TTS)
```bash
python3 skills/local-tts/scripts/generate_narration.py \
  --text "Bem-vindo ao canal! Hoje vamos explorar como a inteligência artificial..." \
  --output "squads/{squad}/output/{run_id}/narration.mp3"
```

### A partir de arquivo de texto
```bash
python3 skills/local-tts/scripts/generate_narration.py \
  --file "squads/{squad}/output/{run_id}/script-clean.txt" \
  --output "squads/{squad}/output/{run_id}/narration.mp3" \
  --voice "pt-BR-AntonioNeural"
```

### Com provider específico
```bash
python3 skills/local-tts/scripts/generate_narration.py \
  --text "Texto aqui" \
  --output "narration.mp3" \
  --provider kokoro
```

## Pré-processamento do roteiro (IMPORTANTE)

Antes de chamar local-tts, o agente deve limpar o roteiro:
1. Remover marcações markdown (`**texto**` → `texto`, `# Título` → `Título`)
2. Remover cues de B-roll: `[B-roll: câmera pan]` → ``
3. Remover notas de produção entre colchetes: `[Gráfico aparece]` → ``
4. Substituir emojis por equivalentes textuais ou remover
5. Adicionar pontuação final em frases que terminam sem ela

Para textos longos (>500 chars), o script faz chunking automático e concatena.

## Cost awareness

- **Edge-TTS:** Totalmente gratuito — sem limite documentado de uso
- **Kokoro/Piper:** Gratuitos, processamento local
- Comparativo com Elevenlabs (pago): ~$0.30 por 1000 chars vs $0 com Edge-TTS

## Error handling

- **Edge-TTS offline:** script tenta 3 vezes antes de falhar. Verifique conexão com internet.
- **Arquivo de saída com 0 bytes:** indica falha na geração — o script relata e sai com código 1
- **Texto muito longo:** o script faz chunking automático em parágrafos de até 500 chars
- **Voz não encontrada:** o script lista vozes disponíveis e sugere a mais próxima
