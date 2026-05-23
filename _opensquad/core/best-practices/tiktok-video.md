---
name: "TikTok Video"
platform: "tiktok"
content_type: "video"
description: "Estratégia e formato de conteúdo para TikTok: hooks virais, estrutura de vídeo curto, TikTok SEO e publicação otimizada para o algoritmo FYP"
whenToUse: |
  Criando agentes que produzem conteúdo em vídeo para TikTok.
  Inclui roteiro, cenas visuais, narração, legendas burn-in e publicação.
constraints:
  max_duration_seconds: 600
  recommended_duration: "15-60s"
  sweet_spot_duration: "21-34s"
  aspect_ratio: "9:16 vertical"
  resolution: "1080×1920"
  caption_max_chars: 2200
  max_hashtags: 10
  recommended_hashtags: "3-5"
  min_fps: 24
  recommended_fps: 30
version: "1.0.0"
---

# TikTok Video

## Platform Rules

O TikTok distribui vídeos pelo **For You Page (FYP)** — o feed principal. O algoritmo prioriza:

1. **Taxa de conclusão** (completion rate) — percentual de espectadores que assistem até o final
   - O sinal mais importante para o algoritmo
   - Vídeos curtos (15-30s) têm taxas de conclusão mais altas
   - Um loop perfeito (o fim parece o início) dobra o tempo de visualização

2. **Replays** — quantas vezes o mesmo usuário assiste novamente
   - Vídeos que "surpreendem no final" geram replays naturais

3. **Compartilhamentos e saves** — mais valiosos do que likes e comentários
   - Um vídeo compartilhado demonstra alto valor percebido

4. **Primeiros 1-3 segundos** determinam distribuição
   - Se o usuário passar nos primeiros 3s, o TikTok para de distribuir
   - O hook visual/textual deve aparecer no frame 1 — sem intro, sem logo, sem créditos

5. **Cultura de som ativo** — 60%+ dos usuários assistem com som
   - Áudio faz parte do conteúdo, não apenas acompanha
   - Sons virais (trending sounds) aumentam alcance quando relevantes

6. **TikTok indexa o áudio falado** para SEO — diga a keyword em voz alta

## Content Structure

### Hook (0-1s) — CRÍTICO
- **Objetivo:** Impedir que o usuário deslize
- O hook começa ANTES de qualquer narração — é visual
- Frame 1 deve mostrar o resultado, a emoção, ou o dado surpreendente
- Exemplos de hooks visuais: pessoa surpresa, número em destaque, "antes e depois"

### Grab (1-3s) — Contexto
- Estabelece o que o espectador vai ganhar assistindo
- Cria a "promessa de valor" que mantém a atenção
- Pode ser narrado: "Você não vai acreditar nisso..."

### Delivery (3-55s) — Valor
- Entrega o conteúdo prometido no hook
- Corte rápido: nunca pausa >0.5s no meio de uma frase
- Uma ideia central, sem digressões
- Use dados, exemplos concretos, demonstrações visuais

### Loop/Punchline (últimos 2-5s)
- Fecha com o gancho que cria replay
- Opções: pergunta que remete ao início, dado que "relê" o hook, call-to-action de comentário
- "E você, já sabia disso? Comenta 👇"

## Fórmulas de Hook PT-BR de Alto Desempenho

```
"[Número]% das pessoas não sabem que..."
"O erro que [profissão] comete todo dia sobre..."
"Eu testei [coisa] por [tempo] e o resultado foi..."
"Ninguém te conta isso sobre [tema popular]..."
"Pare tudo e veja isso sobre [assunto urgente]"
"O [produto/hábito/estratégia] que [promessa exagerada mas verdadeira]"
"Em 30 segundos você vai aprender o que levou X anos para descobrir"
```

## Sound Strategy

- **Trending sound:** Use quando relevante para o tema — aumenta distribuição 20-40%
- **Voz original:** Constrói identidade de marca ao longo do tempo
- **Combo:** Voz original + trending instrumental de fundo (volume 15%)
- Para encontrar trending sounds: aba "Sons" no TikTok Creator Studio

## Writing Guidelines

### Roteiro TikTok
- **Velocidade de fala:** 160-180 palavras/minuto (mais rápido que YouTube)
- **Uma ideia central** — nunca tente cobrir dois temas em um vídeo
- **Linguagem direta:** "você" não "as pessoas"; "faça" não "é possível fazer"
- Cada frase deve ser independente (legendas de uma linha por fala)
- Evite advérbios e qualificadores: "muito", "bastante", "realmente" — corte tudo

### Legendas (obrigatório)
- **100% dos vídeos TikTok devem ter legendas** burn-in
- Estilo: fonte grande, centralizada, branca com sombra preta
- Uma linha por fala (máx. 6-7 palavras)
- Sincronizada perfeitamente com o áudio

### Cenas visuais
- Troca de cena a cada 2-4s (ritmo TikTok)
- Movimento ou mudança em todo frame (nunca imagem estática por >3s)
- Para vídeos narrados com imagens: adicione zoom lento (Ken Burns effect) nas cenas estáticas

## TikTok SEO

1. **Keyword na primeira linha da legenda** (caption)
2. **Diga a keyword em voz alta** no vídeo — TikTok indexa áudio
3. **3-5 hashtags de nicho** (evite #fyp, #viral, #foryou — genéricos demais)
   - 1-2 hashtags específicas do nicho (ex: #marketingdigital)
   - 1-2 hashtags da categoria (ex: #empreendedorismo)
   - 1 hashtag de tendência se relevante
4. **Texto on-screen** com a keyword — TikTok faz OCR nas imagens do vídeo

## Output Format

### Roteiro TikTok
```
[HOOK VISUAL — Frame 1: descreva o que aparece na tela]

[HOOK NARRADO — 0-3s]
Frase de gancho...

[DELIVERY — 3-55s]
Desenvolvimento em frases curtas...
Cada linha = uma legenda na tela...

[PUNCHLINE/LOOP — últimos 3s]
Fechamento que cria replay ou CTA...

[LEGENDA DO POST]
Primeira linha com keyword...
.
Segunda linha complementar...
.
#hashtag1 #hashtag2 #hashtag3
```

## Quality Criteria

Antes de finalizar o roteiro TikTok, verifique:

- [ ] Hook visual está definido (o que aparece no frame 1)
- [ ] Hook narrado começa em menos de 1 segundo
- [ ] Duração alvo: 21-60s (ideal: 34s)
- [ ] Uma única ideia central
- [ ] Cada frase tem no máximo 7 palavras (para legenda)
- [ ] Punchline ou CTA nos últimos 3s
- [ ] Keyword está na primera linha da legenda do post
- [ ] 3-5 hashtags (sem #fyp ou #viral)
- [ ] Legendas burn-in planejadas

## Anti-patterns

- ❌ **Vídeo horizontal** — nunca, sempre 9:16 vertical
- ❌ **Intro com logo/abertura** — o TikTok não tem intro
- ❌ **Mais de uma ideia central** — o usuário vai embora
- ❌ **Pausa >0.5s no meio do vídeo** — corte está errado
- ❌ **Sem legendas** — 40% dos usuários têm som desligado no início
- ❌ **Hook depois dos 3s** — tarde demais, o usuário já passou
- ❌ **Hashtags genéricas** (#fyp, #viral, #foryou) — não contribuem para SEO de nicho
- ❌ **Estilo "cinematográfico lento"** — não funciona no TikTok
- ❌ **CTA "Siga o canal"** no início — diz ao algoritmo que seu conteúdo não é suficiente sozinho
