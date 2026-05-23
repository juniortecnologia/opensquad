---
name: youtube-seo
description: >
  Otimização de SEO para YouTube: títulos, descrição, tags, capítulos, hashtags
  e conceito de thumbnail. Usa web_search para analisar concorrentes e identificar
  palavras-chave de alto CTR. Gera 3 variações de título testáveis e descrição
  otimizada para busca orgânica e sugestão de vídeos.
description_pt-BR: >
  SEO para YouTube: títulos, descrição, tags, capítulos e hashtags.
  Pesquisa concorrentes via web_search. Gera 3 variações de título e descrição completa.
type: prompt
version: "1.0.0"
categories: [seo, youtube, optimization, content, titles, tags]
---

# YouTube SEO

## When to use

Use youtube-seo após o roteiro ser aprovado e antes do upload. O especialista de SEO:
1. Pesquisa concorrentes para identificar padrões de título que rankeiam bem
2. Identifica palavras-chave de alto volume para o tema
3. Gera título, descrição, tags, capítulos e hashtags otimizados
4. Propõe conceito visual de thumbnail baseado nos títulos que geram maior CTR

## Como o YouTube SEO funciona (diferente do Google)

- **Watch time** é o sinal mais importante, não backlinks
- **CTR × AVD** (Click-Through Rate × Average View Duration) = distribuição pelo algoritmo
- **Suggested Videos** (vídeos sugeridos, não busca) é a principal fonte de tráfego — 60-70%
- **A thumbnail é 50% do trabalho** — influencia diretamente o CTR
- **Primeiros 30 segundos** determinam retenção e watch time

## Processo de pesquisa de palavras-chave

1. Buscar no YouTube pelo tema com `web_search site:youtube.com "{tema}"`
2. Analisar os 5 primeiros resultados: padrões de título, palavras-chave frequentes
3. Identificar o "curiosity gap" usado nos títulos de maior engajamento
4. Mapear palavras-chave long-tail (mais específicas e menos competitivas)
5. Verificar duração dos vídeos que rankeiam (indica o que o algoritmo prefere)

## Regras de otimização de título

- **Limite:** 100 chars; **ideal:** 50-70 chars (para não truncar na busca)
- **Keyword front-loading:** palavra-chave principal nos primeiros 40 chars
- **3 fórmulas que funcionam bem em PT-BR:**
  - `"[Número] [Resultado]: O Guia Definitivo de [Keyword]"`
  - `"Como [Fazer X] em [Tempo/Número de Passos] (Sem [Objeção])"`
  - `"[Dado surpreendente] sobre [Keyword] que Ninguém Te Conta"`
- Sempre gerar **3 variações** para o usuário escolher

## Estrutura da descrição

```
[Primeiras 2 linhas VISÍVEIS sem "Mostrar mais" — hook + keyword principal]

[Corpo: resumo do conteúdo com palavras-chave secundárias, 100-200 palavras]

📌 CAPÍTULOS:
0:00 Introdução
1:23 Seção 1
3:45 Seção 2

🔗 LINKS:
[Links de recursos mencionados no vídeo]

👉 [CTA para inscrição no canal]
📱 Redes sociais: [links]

#hashtag1 #hashtag2 #hashtag3
```

**CRÍTICO:** As primeiras 2-3 linhas da descrição são exibidas antes do "Mostrar mais" na busca do YouTube. Devem conter o hook e a keyword principal.

## Tags (8-15 tags)

Estrutura recomendada:
1. Keyword exata do título (ex: "inteligência artificial trabalho")
2. Variações da keyword (ex: "IA no trabalho", "AI no trabalho")
3. Long-tail relacionado (ex: "como usar IA para ser mais produtivo")
4. Categoria ampla (ex: "tecnologia 2025", "produtividade")
5. Marca do canal (ex: "Nome do Canal")

## Capítulos (timestamps)

**Obrigatório para vídeos acima de 3 minutos.**

Regras:
- Primeiro capítulo DEVE começar em 0:00 (ex: "0:00 Introdução")
- Mínimo 3 capítulos para ativar o recurso
- Labels curtos e descritivos (ideal: 2-4 palavras)
- Capítulos ajudam vídeos a ranquear em buscas específicas de seção

Exemplo:
```
0:00 Introdução
1:15 O Problema
3:40 A Solução
7:22 Resultados
10:05 Próximos Passos
```

## Conceito de thumbnail

O SEO specialist deve propor o conceito visual da thumbnail junto com o SEO:
- Qual emoção/expressão (surpresa? urgência? satisfação?)
- Quais palavras aparecer na thumbnail (máximo 4)
- Qual elemento de contraste visual (círculo, seta, badge)
- Paleta de cores principal (2-3 cores, alto contraste)

## Formato de output

Gerar arquivo YAML estruturado:
```yaml
seo_package:
  title_variants:
    - "Título Opção 1 — com keyword em destaque"
    - "Título Opção 2 — curiosity gap"
    - "Título Opção 3 — número + resultado"
  recommended_title: "Título Opção 1"
  description: |
    Primeira linha do hook com keyword principal.
    Segunda linha complementar ainda visível.

    Corpo da descrição aqui...

    📌 CAPÍTULOS:
    0:00 Introdução
    [...]

    #hashtag1 #hashtag2 #hashtag3
  tags:
    - "keyword exata"
    - "variação 1"
    - "variação 2"
    - "long-tail"
    - "categoria"
  chapters:
    - "0:00 Introdução"
    - "1:15 Seção 1"
  hashtags:
    - "#hashtag1"
    - "#hashtag2"
    - "#hashtag3"
  thumbnail_concept:
    emotion: "surpresa"
    text_overlay: "3 Palavras Aqui"
    visual_element: "badge circular vermelho"
    colors: ["#FF4136", "#FFFFFF", "#000000"]
```

## Anti-patterns

- ❌ Keyword stuffing no título ("Como usar IA IA Inteligência Artificial IA 2025")
- ❌ Clickbait que não corresponde ao conteúdo (penaliza watch time)
- ❌ Descrição genérica ou vazia
- ❌ Mais de 15 tags (YouTube não valoriza listas longas de tags)
- ❌ Capítulos sem timestamp 0:00 (não ativa o recurso)
- ❌ Hashtags não relacionadas ao conteúdo
