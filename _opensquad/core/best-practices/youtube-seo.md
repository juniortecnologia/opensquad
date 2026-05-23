---
name: "YouTube SEO"
platform: "youtube"
content_type: "seo"
description: "Guia completo de otimização SEO para YouTube: pesquisa de palavras-chave, título, descrição, tags, capítulos e estratégia de thumbnail"
whenToUse: |
  Criando agentes que otimizam vídeos para busca orgânica no YouTube.
  Inclui pesquisa de concorrentes, geração de título, descrição, tags, capítulos e hashtags.
constraints:
  title_max_chars: 100
  title_optimal_chars: "50-70"
  description_max_chars: 5000
  description_visible_lines: 2
  tags_max: 500
  recommended_tags: "8-15"
  thumbnail_dimensions: "1280x720px"
  thumbnail_max_size: "2MB"
  chapters_min_videos: "3 minutos"
  chapters_min_count: 3
version: "1.0.0"
---

# YouTube SEO

## Como o YouTube SEO difere do Google SEO

| Fator | Google SEO | YouTube SEO |
|-------|-----------|-------------|
| Sinal principal | Backlinks + conteúdo | Watch time + CTR |
| Tráfego primário | Busca orgânica | Vídeos sugeridos (60-70%) |
| Velocidade de rankeamento | Meses | Dias a semanas |
| Retenção importa? | Não | Sim — AVD (Average View Duration) é crucial |
| Thumbnail | N/A | 50% do desempenho do vídeo |

**Fórmula do algoritmo do YouTube:**
```
Distribuição ∝ CTR × AVD × Engagement signals
```
- CTR (Click-Through Rate): percentual de quem clica na thumbnail
- AVD (Average View Duration): tempo médio assistido
- Engagement: likes, comentários, compartilhamentos, saves

## Processo de Pesquisa de Palavras-Chave

### 1. Validar demanda de busca
```
Pesquisar no YouTube: "{tema}"
Pesquisar no YouTube: "{tema} como"
Pesquisar no YouTube: "{tema} para iniciantes"
Pesquisar no YouTube: "{tema} 2025"
```
Observar: autocomplete do YouTube mostra o que as pessoas realmente buscam.

### 2. Analisar vídeos que rankeiam
Para cada vídeo no top 5 da busca:
- Quantos views tem? (validação de volume)
- Qual o título exato? (extrai keyword e estrutura)
- Qual a duração? (indica o que o algoritmo prefere para este tema)
- Quantos inscritos o canal tem? (para entender nível de competição)

### 3. Identificar ângulos não explorados
- Buscar brechas: "ninguém fez um vídeo sobre X ângulo"
- Verificar qual pergunta do Google relacionada não tem resposta boa no YouTube
- Analisar comentários dos vídeos concorrentes: o que as pessoas perguntam?

### 4. Escolher keyword principal
- Keyword primária: aparece nos primeiros 40 chars do título
- Keyword secundária: aparece na descrição e em 2-3 tags
- Long-tail: 3-4 palavras mais específicas — menos competição, mais intenção

## Otimização de Título

### Regras fundamentais
- **Limite:** 100 chars; **ideal:** 50-70 (evita truncamento na busca)
- **Keyword principal nos primeiros 40 chars** — o que aparece antes da reticências
- **Evite palavras de preenchimento** no início: "Um guia para..." → "Guia de..."
- **Não use CAIXA ALTA excessiva** — parece spam para o YouTube

### 3 fórmulas com alto CTR em PT-BR

**Fórmula 1 — Número + Resultado:**
```
[N] [Resultado] que [Audiência] Precisa Saber Sobre [Keyword]
"7 Estratégias de Marketing Digital que Todo Empreendedor Precisa Conhecer"
```

**Fórmula 2 — Como + Resultado (sem jargão):**
```
Como [Ação] em [Tempo/Contexto] (Sem [Objeção Principal])
"Como Aprender Inglês em 3 Meses (Sem Gastar Nada)"
```

**Fórmula 3 — Curiosity Gap:**
```
O [Erro/Segredo/Verdade] sobre [Keyword] que [Consequência Emocional]
"O Erro Que 90% das Pessoas Cometem ao Investir em Cripto"
```

### Sempre gerar 3 variações de título
O usuário deve poder escolher. Variante A = número, Variante B = como, Variante C = curiosity gap.

## Estrutura da Descrição

### Template completo
```
[LINHA 1 — Hook com keyword principal — visível sem "Mostrar mais"]
Aprenda como [keyword] em [tempo] sem precisar de [objeção].

[LINHA 2 — Complemento ainda visível]
Neste vídeo você vai descobrir [3 bullet points do conteúdo].

[ESPAÇO EM BRANCO]

[CORPO — 150-250 palavras com keywords secundárias]
Neste vídeo, vamos explorar [tema]. Você vai aprender [ponto 1],
como [ponto 2], e por que [ponto 3] é essencial para [benefício].

Se você quer [resultado desejado pela audiência], este é o vídeo certo.

[CAPÍTULOS]
📌 CAPÍTULOS:
0:00 Introdução
1:30 [Seção 1]
4:15 [Seção 2]
7:40 [Seção 3]
10:20 Conclusão

[LINKS DE RECURSOS]
🔗 [Links mencionados no vídeo]

[CTA]
✅ Inscreva-se no canal para não perder os próximos vídeos
👍 Deixa o like se esse conteúdo te ajudou

[HASHTAGS — últimas 3 aparecem acima do título]
#keyword1 #keyword2 #keyword3
```

**CRÍTICO:** As primeiras 2-3 linhas são exibidas na busca do YouTube e em Vídeos Sugeridos. Elas devem conter a keyword e criar desejo de clicar.

## Tags

**Estrutura de 8-15 tags:**
1. Keyword exata do título (`"marketing digital"`  — com aspas para exata)
2. Keyword sem aspas (`marketing digital`)
3. Variações (`marketing digital 2025`, `marketing digital para iniciantes`)
4. Long-tail (`como fazer marketing digital do zero`)
5. Keywords relacionadas (`tráfego orgânico`, `SEO para negócios`)
6. Categoria ampla (`marketing`, `empreendedorismo`)
7. Marca do canal (`Nome do Canal`)

**Nunca use mais de 15 tags** — YouTube não indexa tags excessivas e pode penalizar.

## Capítulos (Timestamps)

**Obrigatório para vídeos acima de 3 minutos.**

### Regras de formato
- Primeiro capítulo SEMPRE em `0:00` (ex: `0:00 Introdução`)
- Mínimo 3 capítulos para ativar o recurso
- Labels curtos e descritivos (ideal: 2-4 palavras)
- Espaço exato no formato: `M:SS Label` ou `MM:SS Label`

### Benefícios dos capítulos
- YouTube mostra capítulos como "rich snippet" nos resultados de busca
- Cada capítulo pode ser indexado separadamente para diferentes buscas
- Aumenta watch time (usuários saltam para a parte que querem e permanecem mais)

### Exemplo para vídeo de 12 minutos
```
0:00 Introdução
1:45 O Problema
4:20 A Solução
7:10 Resultados Reais
10:30 Como Aplicar
11:50 Próximos Passos
```

## SEO de Thumbnail

- **Nome do arquivo:** Use a keyword (`marketing-digital-para-iniciantes.jpg`, não `IMG_0042.jpg`)
- **A thumbnail afeta o CTR**, que afeta diretamente a distribuição
- Teste A/B com YouTube Studio Analytics após 48h
- Thumbnails com face humana + emoção exagerada + texto curto = maior CTR historicamente

## Engajamento como Sinal de SEO

- **Primeiros 15 minutos após publicação** são cruciais — compartilhe para audiência existente imediatamente
- **Comentário fixado** com link de recurso mencionado + CTA para comentários
- **Responder comentários** nas primeiras 2h aumenta o sinal de engajamento
- **Community post** anunciando o vídeo antes do lançamento

## Output Format

```yaml
seo_package:
  title_variants:
    - "Título Opção A — número + resultado"
    - "Título Opção B — como + resultado"
    - "Título Opção C — curiosity gap"
  recommended_title: "Título Opção A"
  keywords:
    primary: "keyword principal"
    secondary: ["variação 1", "variação 2"]
    long_tail: ["long-tail 1", "long-tail 2"]
  description: |
    [conteúdo completo da descrição]
  tags:
    - "keyword exata"
    - "variação"
    [...]
  chapters:
    - "0:00 Introdução"
    - "1:30 Seção 1"
  hashtags:
    - "#hashtag1"
    - "#hashtag2"
    - "#hashtag3"
  thumbnail_concept:
    emotion: "surpresa"
    text_overlay: "3-4 palavras"
    visual_element: "badge circular"
    colors: ["#cor1", "#cor2"]
  competitive_analysis:
    top_videos:
      - title: "título do concorrente"
        views: "X M views"
        duration: "X:XX"
```

## Quality Criteria

- [ ] Keyword principal nos primeiros 40 chars do título
- [ ] 3 variações de título geradas
- [ ] Primeiras 2 linhas da descrição são hook + keyword
- [ ] Capítulos com timestamp 0:00 como primeiro
- [ ] 8-15 tags (não mais)
- [ ] 3 hashtags no final da descrição
- [ ] Conceito de thumbnail definido com texto ≤4 palavras

## Anti-patterns

- ❌ Keyword stuffing no título ("marketing digital marketing digital 2025")
- ❌ Clickbait que não corresponde ao conteúdo real (mata o watch time)
- ❌ Descrição genérica ou vazia
- ❌ Mais de 15 tags
- ❌ Capítulos sem o 0:00 como primeiro (não ativa o recurso)
- ❌ Hashtags não relacionadas para "surfar em trending topics" (penaliza distribuição)
- ❌ Título com mais de 70 chars (truncado na maioria dos displays)
