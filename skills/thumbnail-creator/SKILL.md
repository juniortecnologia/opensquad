---
name: thumbnail-creator
description: >
  Cria thumbnails para plataformas de vídeo via HTML/CSS renderizado pelo Playwright.
  Formatos: YouTube (1280×720), TikTok capa (1080×1920), Instagram Reel capa (1080×1920).
  Templates prontos com alta legibilidade e contraste. Estende image-creator com
  templates otimizados para cada plataforma de vídeo.
description_pt-BR: >
  Cria thumbnails de vídeo via HTML/CSS + Playwright. Templates para YouTube (1280×720),
  TikTok e Reel (1080×1920). Alta legibilidade e contraste por design.
type: prompt
version: "1.0.0"
categories: [thumbnails, video, design, youtube, tiktok, reels]
---

# Thumbnail Creator

## When to use

Use thumbnail-creator para criar:
- **YouTube thumbnail** (1280×720) — influencia 50% do CTR do vídeo
- **TikTok capa** (1080×1920) — frame exibido antes do play
- **Instagram Reel cover** (1080×1920) — capa exibida no perfil

**Regra de ouro:** A thumbnail deve ser compreensível em 200ms a 100px de largura (tamanho de card no YouTube). Se precisar apertar o olho para ler, redesenhe.

Esta skill usa o mesmo workflow de `image-creator` (HTML/CSS → Playwright → PNG), mas com templates especializados para cada plataforma de vídeo.

## Workflow de criação

1. **Leia os templates** em `skills/thumbnail-creator/templates/` para entender a estrutura base
2. **Personalize o HTML** para o tema do vídeo específico (título, cores, imagem de fundo)
3. **Renderize com Playwright** usando as dimensões corretas:
   - YouTube: `viewport: {width: 1280, height: 720}`
   - TikTok/Reel: `viewport: {width: 1080, height: 1920}`
4. **Verifique** a legibilidade a tamanho reduzido
5. **Salve** o PNG no caminho de output

## Regras de design para thumbnails de alto CTR

### Elementos obrigatórios
- **Face/emoção:** Thumbnails com rosto humano expressivo geram 38% mais cliques
- **Texto:** Máximo 4 palavras, fonte ≥120px no YouTube, ≥80px no TikTok
- **Contraste:** Mínimo 4.5:1 entre texto e fundo (WCAG AA)
- **Elemento de destaque:** Badge circular, seta, círculo de destaque — algo que chame o olho

### Paleta de cores
- YouTube funciona bem com: vermelho (#FF0000), amarelo (#FFD700), laranja (#FF6B35)
- Evite: cinza, verde musgo, marrom — baixo CTR historicamente
- Use no máximo 3 cores por thumbnail

### Composição
- **Regra dos terços:** Coloque o elemento principal em uma das 4 intersecções da grade 3×3
- **Espaço negativo:** Deixe área clara para o texto respirar
- **Profundidade:** Elemento frontal (rosto/produto) + texto + fundo — 3 planos

## Thumbnails prontos para personalizar

### YouTube (1280×720)
Template em `skills/thumbnail-creator/templates/youtube-thumbnail.html`

Variáveis para personalizar:
```html
<!-- Substitua estas partes: -->
<div class="label">TUTORIAL</div>          <!-- Ex: DICA, GUIA, 2025 -->
<div class="headline">Como Fazer <span class="accent">Isso</span></div>  <!-- Título -->
<div class="badge-number">5</div>          <!-- Número destaque -->
<div class="badge-label">PASSOS</div>      <!-- Label do badge -->
```

Para mudar o fundo, adicione uma `<img class="bg-image" src="path/to/image.jpg">` dentro do body.

### TikTok / Reel (1080×1920)
Template em `skills/thumbnail-creator/templates/tiktok-cover.html`

### Reel cover (1080×1920)
Template em `skills/thumbnail-creator/templates/reel-cover.html`

## Renderização com Playwright (image-creator workflow)

Para renderizar, use o mesmo processo do `image-creator`:
1. Escreva o HTML completo com CSS inline
2. Use o MCP do Playwright para:
   - Navegar para a URL do arquivo HTML local (`file:///path/to/thumb.html`)
   - Definir viewport com as dimensões corretas
   - Tirar screenshot e salvar como PNG

## Verificação de qualidade

Após gerar a thumbnail, verifique:
- [ ] Texto legível quando a imagem é reduzida a 200×112px (YouTube card)
- [ ] Pelo menos 3 cores distintas com bom contraste
- [ ] Máximo 4 palavras no texto principal
- [ ] Elemento visual de destaque presente (badge, seta, expressão)
- [ ] Sem fontes muito finas (use Bold/Black)
- [ ] Arquivo PNG salvo (não JPEG para evitar artefatos de compressão)

## Integração com SEO

O `seo-specialist` gera um `thumbnail_concept` no pacote de SEO:
```yaml
thumbnail_concept:
  emotion: "surpresa"
  text_overlay: "3 Palavras Aqui"
  visual_element: "badge circular vermelho"
  colors: ["#FF4136", "#FFFFFF", "#000000"]
```

Use este conceito como briefing para criar a thumbnail.

## Anti-patterns

- ❌ Texto com mais de 5 palavras (ilegível em thumbnail pequena)
- ❌ Fonte sem Bold (muito fina para thumbnail)
- ❌ Mais de 3 cores principais (confuso visualmente)
- ❌ Fundo branco ou cinza claro (baixo contraste, se perde no feed)
- ❌ Thumbnail criada sem verificar a 200px de largura
- ❌ Usar JPEG em vez de PNG (artefatos de compressão no texto)
