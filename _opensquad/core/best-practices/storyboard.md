---
name: "Storyboard & Shot List"
platform: "multi"
content_type: "storyboard"
description: "Guia de criação de storyboard cena a cena para vídeos de conteúdo: estrutura de shots, prompts de imagem para geração via IA, timings e notas de produção."
whenToUse: |
  Criando agentes que transformam roteiros em storyboards detalhados com descrições
  de cena prontas para geração de imagens via local-image-gen ou image-ai-generator.
  Leia também video-production.md para o contexto completo do pipeline.
version: "1.0.0"
---

# Storyboard & Shot List

## O que é um Storyboard neste contexto

Um storyboard para produção de vídeo com IA não é um esboço desenhado à mão. É um arquivo YAML estruturado que funciona como "script de produção" — conecta o roteiro com as imagens a serem geradas e com a montagem final.

Cada entrada no storyboard é uma instrução completa para:
1. Qual imagem deve ser gerada (prompt)
2. O que deve ser narrado naquele momento (trecho do roteiro)
3. Por quanto tempo a cena deve aparecer (em segundos)
4. Qual texto aparece na tela (text overlay / legenda visual)
5. Como transicionar para a próxima cena

## Regras de Divisão em Cenas

### Quantidade de cenas por duração de vídeo
| Duração do vídeo | Cenas recomendadas | Duração média por cena |
|------------------|--------------------|------------------------|
| 15-30s (TikTok curto) | 3-8 cenas | 3-5s |
| 30-60s (TikTok/Reels) | 8-15 cenas | 4-6s |
| 1-3 min (Shorts/Reels longos) | 15-30 cenas | 5-7s |
| 5-10 min (YouTube) | 40-80 cenas | 6-8s |
| 10-20 min (YouTube longo) | 60-120 cenas | 8-12s |

### Uma cena = um beat narrativo
- Um **beat narrativo** é uma unidade completa de informação
- Exemplos de beats: "um dado estatístico", "uma explicação de conceito", "uma etapa do processo", "uma transição de argumento"
- Quando o argumento muda → troca de cena
- Quando aparece um novo personagem ou localização → troca de cena

### Duração mínima e máxima
- **Mínimo:** 3 segundos — menos tempo e o espectador não processa a imagem
- **Máximo:** 12 segundos sem movimento — parece estático e gera drop off
- Para cenas longas: adicione zoom lento (Ken Burns) ao gerar o vídeo

## Estrutura do Image Prompt por Cena

### Template de prompt
```
[Sujeito + ação], [ambiente/cenário], [iluminação], [estilo fotográfico], [qualidade técnica], [formato/proporção]
```

### Exemplos de prompts bem estruturados

**Para TikTok/Reels (vertical 9:16):**
```
"Jovem empreendedor animado olhando para o celular, escritório moderno com plantas ao fundo, 
luz natural suave pela janela, fotografia editorial, 4K ultra-detalhado, 
proporção vertical 9:16, sem texto na imagem"
```

**Para YouTube (horizontal 16:9):**
```
"Gráfico de linha ascendente em tela de computador com mãos digitando ao fundo, 
setup tech moderno com monitores duplos, iluminação de estúdio azul, 
fotorrealismo profissional, 4K, proporção 16:9, sem texto na imagem"
```

### Regras de prompt para consistência visual

**Regra mais importante:** defina um `visual_style` no início do storyboard e copie-o em CADA prompt.

```yaml
visual_style: "fotorrealismo 4K, iluminação suave neutra, paleta azul e branca, câmera de 85mm com fundo desfocado"
```

Cada prompt deve terminar com este descriptor de estilo.

**Nunca inclua texto legível nas imagens** — IA não renderiza texto bem. Use `text_overlay` para isso.

### Elementos para evitar em prompts
- Nomes de marcas específicas (Nike, Apple, etc.) — pode causar erros
- Texto legível (letras, números em placas, telas) — IA distorce
- Multidões com muitas faces — geração de rostos múltiplos fica estranha
- Mãos segurando objetos pequenos — mãos são o ponto fraco de todos os modelos

## Formato YAML Completo do Storyboard

```yaml
storyboard:
  # Metadados
  video_title: "Título do Vídeo"
  squad: "nome-do-squad"
  run_id: "2026-05-02-120000"
  platform: "tiktok"                    # youtube | tiktok | reels | shorts
  total_duration_target: 45             # segundos alvo
  
  # DEFINA O ESTILO UMA VEZ E COPIE EM TODOS OS PROMPTS
  visual_style: "fotorrealismo 4K, iluminação suave de estúdio, paleta azul e branca, câmera 85mm, fundo desfocado"
  
  # Configuração de narração
  narrator:
    provider: edge-tts
    voice: pt-BR-FranciscaNeural
    
  scenes:
    - scene: 1
      narration: "71% dos profissionais usam IA sem contar para o chefe."
      duration_seconds: 6
      image_prompt: "Profissional discreto olhando tela de laptop em escritório moderno, expressão de surpresa, fotorrealismo 4K, iluminação suave de estúdio, paleta azul e branca, câmera 85mm, fundo desfocado, 9:16 vertical"
      text_overlay: "71% escondem o uso de IA"
      text_position: center          # top | center | bottom
      transition: crossfade
      notes: "Cena âncora do hook — mostrar o dado em destaque"
      
    - scene: 2
      narration: "E as empresas que adotam IA têm 40% mais produtividade."
      duration_seconds: 6
      image_prompt: "Dashboard moderno com gráficos de crescimento, mão apontando para tela com dados positivos, luz azul de tela refletindo no rosto, fotorrealismo 4K, iluminação suave de estúdio, paleta azul e branca, câmera 85mm, fundo desfocado, 9:16 vertical"
      text_overlay: "40% mais produtividade"
      text_position: center
      transition: crossfade
      notes: "Dado de impacto — reforça o hook"
      
    - scene: 3
      narration: "O problema? A maioria não sabe por onde começar."
      duration_seconds: 5
      image_prompt: "Pessoa confusa na frente de computador com múltiplas janelas abertas, expressão de frustração leve, iluminação quente de escritório em casa, fotorrealismo 4K, iluminação suave de estúdio, paleta azul e branca, câmera 85mm, fundo desfocado, 9:16 vertical"
      text_overlay: "O problema..."
      text_position: top
      transition: crossfade
      notes: "Virada de conflito — cria empatia"
```

## Calculando Duração por Narração

**Fórmula PT-BR:**
```
duração_segundos = (contagem_palavras / 150) × 60 × 1.1
```

| Palavras | Duração estimada |
|----------|------------------|
| 10 | 4.4s |
| 15 | 6.6s |
| 20 | 8.8s |
| 25 | 11.0s |
| 30 | 13.2s |

**Soma das durações** de todas as cenas deve igualar a duração total alvo do vídeo.

## Consistência Visual entre Cenas

### Técnicas para manter consistência
1. **Mesmo descriptor de estilo** em 100% dos prompts
2. **Mesma paleta de cores** (especifique as cores dominantes)
3. **Mesmo tipo de câmera/focal** (85mm, grande angular, etc.)
4. **Mesma iluminação** (natural, de estúdio, backlit, etc.)
5. Para personagens: descreva aparência detalhada na cena 1 e repita em cenas subsequentes

### Quando usar imagens geradas vs. stock
- Imagens geradas: cenas específicas do contexto do vídeo
- Stock/web (via image-fetcher): dados estatísticos, infográficos, mapas, produtos reais

## Verificação do Storyboard

Antes de passar para a geração de imagens, verifique:
- [ ] Total de cenas cobre a duração alvo do vídeo
- [ ] Cada cena tem narration, duration_seconds, image_prompt e transition
- [ ] visual_style está presente e é consistente em todos os image_prompts
- [ ] Nenhum prompt pede texto legível na imagem
- [ ] Proporção correta está no prompt (9:16 para vertical, 16:9 para horizontal)
- [ ] text_overlay definido para cenas com dados ou pontos-chave

## Output Format

O agente deve salvar o storyboard como:
```
squads/{squad-code}/output/{run_id}/storyboard.yaml
```

E gerar um resumo legível:
```markdown
# Storyboard — {video_title}
**Plataforma:** {platform}
**Duração total:** {X}s ({N} cenas)

| # | Narração | Duração | Overlay |
|---|---------|---------|---------|
| 1 | "71% dos profissionais..." | 6s | "71% escondem..." |
| 2 | "E as empresas..." | 6s | "40% mais produtividade" |
[...]
```

## Quality Criteria

- [ ] Pelo menos 1 cena por beat narrativo principal do roteiro
- [ ] Duração total das cenas = duração alvo ±5%
- [ ] visual_style idêntico em todos os prompts
- [ ] Cenas com dados têm text_overlay definido
- [ ] Nenhuma cena com duração < 3s ou > 12s (sem motion)
- [ ] Prompts sem pedido de texto legível nas imagens

## Anti-patterns

- ❌ Prompts vagos ("pessoa trabalhando") — gera imagens genéricas e inconsistentes
- ❌ Estilo diferente em cada cena — vídeo parece colagem aleatória
- ❌ Cenas muito longas sem movimento (>10s de imagem estática)
- ❌ Pedir texto em imagens via prompt — IA não renderiza texto bem
- ❌ Não usar text_overlay para dados importantes — espectador pode não ouvir o áudio
- ❌ Duração das cenas sem verificar que a soma ≈ duração do áudio de narração
- ❌ Cenas com imagens sem proporção correta definida no prompt
