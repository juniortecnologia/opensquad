#!/usr/bin/env bash
# Opensquad — Setup: Ferramentas de IA Local para Pipeline de Vídeo
# Compatível com macOS (Homebrew) e Linux (apt)
# Testado no MacBook Air M1 8GB
#
# Uso: bash setup/setup-local-ai.sh

set -e

BOLD='\033[1m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

info()    { echo -e "${BOLD}[INFO]${NC} $1"; }
success() { echo -e "${GREEN}[OK]${NC}   $1"; }
warn()    { echo -e "${YELLOW}[WARN]${NC} $1"; }
error()   { echo -e "${RED}[ERRO]${NC} $1"; }

echo ""
echo -e "${BOLD}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}║     Opensquad — Setup de IA Local para Vídeo            ║${NC}"
echo -e "${BOLD}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""

# ── Detectar OS ───────────────────────────────────────────────────────────────
OS="$(uname -s)"
ARCH="$(uname -m)"
info "Sistema: $OS / $ARCH"

if [[ "$ARCH" == "arm64" && "$OS" == "Darwin" ]]; then
  info "Apple Silicon M1/M2/M3 detectado — MPS (Metal) será usado para IA local"
fi

# ── Verificar Python 3.9+ ─────────────────────────────────────────────────────
info "Verificando Python..."
if command -v python3 &>/dev/null; then
  PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
  PYTHON_MAJOR=$(echo "$PYTHON_VERSION" | cut -d. -f1)
  PYTHON_MINOR=$(echo "$PYTHON_VERSION" | cut -d. -f2)
  if [[ "$PYTHON_MAJOR" -ge 3 && "$PYTHON_MINOR" -ge 9 ]]; then
    success "Python $PYTHON_VERSION encontrado"
  else
    error "Python $PYTHON_VERSION é muito antigo. Instale Python 3.9+ e tente novamente."
    exit 1
  fi
else
  error "Python 3 não encontrado. Instale de https://python.org e tente novamente."
  exit 1
fi

# ── Instalar FFmpeg ───────────────────────────────────────────────────────────
info "Verificando FFmpeg..."
if command -v ffmpeg &>/dev/null; then
  success "FFmpeg já instalado: $(ffmpeg -version 2>&1 | head -1 | cut -d' ' -f3)"
else
  warn "FFmpeg não encontrado. Instalando..."
  if [[ "$OS" == "Darwin" ]]; then
    if command -v brew &>/dev/null; then
      brew install ffmpeg
      success "FFmpeg instalado via Homebrew"
    else
      error "Homebrew não encontrado. Instale de https://brew.sh primeiro."
      exit 1
    fi
  elif [[ "$OS" == "Linux" ]]; then
    sudo apt-get update -qq && sudo apt-get install -y ffmpeg
    success "FFmpeg instalado via apt"
  else
    error "Sistema não suportado. Instale FFmpeg manualmente de https://ffmpeg.org"
    exit 1
  fi
fi

# ── Instalar pip packages ─────────────────────────────────────────────────────
info "Instalando pacotes Python para o pipeline de vídeo..."
echo ""

# yt-dlp
info "Instalando yt-dlp (download de vídeos)..."
pip3 install -q "yt-dlp>=2024.1.1" && success "yt-dlp instalado"

# edge-tts
info "Instalando edge-tts (narração gratuita Microsoft)..."
pip3 install -q "edge-tts>=6.1.10" && success "edge-tts instalado"

# faster-whisper
info "Instalando faster-whisper (transcrição/legendas)..."
pip3 install -q "faster-whisper>=1.0.0" && success "faster-whisper instalado"

# moviepy + ffmpeg-python
info "Instalando moviepy + ffmpeg-python (montagem de vídeo)..."
pip3 install -q "moviepy>=1.0.3" "ffmpeg-python>=0.2.0" && success "moviepy + ffmpeg-python instalados"

# python-dotenv + requests
info "Instalando utilitários (dotenv, requests)..."
pip3 install -q "python-dotenv>=1.0.0" "requests>=2.31.0" && success "Utilitários instalados"

echo ""

# ── PyTorch + diffusers (opcional) ───────────────────────────────────────────
echo -e "${BOLD}Deseja instalar PyTorch + diffusers para geração de imagens LOCAL?${NC}"
echo "  - Tamanho: ~2-4 GB de download"
echo "  - No M1: usa Metal (MPS) automaticamente"
echo "  - Sem isso: use 'image-ai-generator' (pago) ou AUTOMATIC1111/ComfyUI separado"
echo ""
read -p "Instalar PyTorch + diffusers? [s/N] " INSTALL_TORCH
echo ""

if [[ "$INSTALL_TORCH" =~ ^[Ss]$ ]]; then
  info "Instalando PyTorch (pode demorar vários minutos)..."
  if [[ "$OS" == "Darwin" ]]; then
    # macOS — instala versão padrão (M1 usa MPS automaticamente)
    pip3 install -q torch torchvision && success "PyTorch instalado (MPS ativo no M1)"
  else
    # Linux — instala CPU build (GPU build requer configuração manual)
    pip3 install -q torch torchvision --index-url https://download.pytorch.org/whl/cpu
    success "PyTorch instalado (CPU build — configure CUDA manualmente se tiver GPU NVIDIA)"
  fi

  info "Instalando diffusers + transformers + accelerate..."
  pip3 install -q "diffusers>=0.27.0" "transformers>=4.38.0" "accelerate>=0.27.0"
  success "diffusers + transformers + accelerate instalados"
else
  warn "PyTorch não instalado. Use --provider auto1111 ou --provider comfyui no local-image-gen."
fi

echo ""

# ── Ollama (opcional) ─────────────────────────────────────────────────────────
echo -e "${BOLD}Deseja instalar Ollama para análise de imagens com llava?${NC}"
echo "  - Permite usar modelos de visão localmente (llava, llama3.2-vision)"
echo "  - Tamanho do modelo: ~4-7 GB"
echo ""
read -p "Instalar Ollama? [s/N] " INSTALL_OLLAMA
echo ""

if [[ "$INSTALL_OLLAMA" =~ ^[Ss]$ ]]; then
  if command -v ollama &>/dev/null; then
    success "Ollama já instalado: $(ollama --version 2>/dev/null || echo 'versão desconhecida')"
  else
    info "Instalando Ollama..."
    if [[ "$OS" == "Darwin" ]]; then
      if command -v brew &>/dev/null; then
        brew install ollama && success "Ollama instalado via Homebrew"
      else
        curl -fsSL https://ollama.ai/install.sh | sh && success "Ollama instalado"
      fi
    else
      curl -fsSL https://ollama.ai/install.sh | sh && success "Ollama instalado"
    fi
  fi

  echo ""
  info "Baixando modelo llava (~4GB)..."
  read -p "Baixar llava agora? [s/N] " PULL_LLAVA
  if [[ "$PULL_LLAVA" =~ ^[Ss]$ ]]; then
    ollama pull llava && success "llava baixado e pronto"
  else
    warn "Execute 'ollama pull llava' quando quiser usar o modelo."
  fi
fi

echo ""

# ── Criar .env se não existir ─────────────────────────────────────────────────
if [[ ! -f ".env" ]]; then
  info "Criando .env a partir de .env.example..."
  cp .env.example .env
  success ".env criado — edite as variáveis antes de usar os squads"
else
  success ".env já existe — mantendo configuração atual"
fi

# ── Download do modelo Whisper base ──────────────────────────────────────────
echo ""
echo -e "${BOLD}Deseja pré-baixar o modelo Whisper 'base' agora?${NC}"
echo "  - Tamanho: ~145 MB"
echo "  - Sem isso: o modelo é baixado na primeira transcrição (pode demorar)"
echo ""
read -p "Pré-baixar Whisper base? [s/N] " PRELOAD_WHISPER
if [[ "$PRELOAD_WHISPER" =~ ^[Ss]$ ]]; then
  python3 -c "
from faster_whisper import WhisperModel
print('Baixando modelo Whisper base...')
WhisperModel('base', device='auto', compute_type='int8')
print('Modelo baixado com sucesso!')
"
  success "Whisper base pronto para uso offline"
fi

# ── Resumo ────────────────────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}║                    Setup concluído!                     ║${NC}"
echo -e "${BOLD}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "Ferramentas instaladas:"
command -v ffmpeg    &>/dev/null && echo -e "  ${GREEN}✓${NC} FFmpeg" || echo -e "  ${RED}✗${NC} FFmpeg"
command -v yt-dlp    &>/dev/null && echo -e "  ${GREEN}✓${NC} yt-dlp" || echo -e "  ${RED}✗${NC} yt-dlp"
python3 -c "import edge_tts"       2>/dev/null && echo -e "  ${GREEN}✓${NC} edge-tts" || echo -e "  ${RED}✗${NC} edge-tts"
python3 -c "import faster_whisper" 2>/dev/null && echo -e "  ${GREEN}✓${NC} faster-whisper" || echo -e "  ${RED}✗${NC} faster-whisper"
python3 -c "import moviepy"        2>/dev/null && echo -e "  ${GREEN}✓${NC} moviepy" || echo -e "  ${RED}✗${NC} moviepy"
python3 -c "import diffusers"      2>/dev/null && echo -e "  ${GREEN}✓${NC} diffusers" || echo -e "  ${YELLOW}~${NC} diffusers (não instalado)"
command -v ollama    &>/dev/null && echo -e "  ${GREEN}✓${NC} ollama" || echo -e "  ${YELLOW}~${NC} ollama (não instalado)"
echo ""
echo "Próximos passos:"
echo "  1. Edite .env com suas chaves de API (BLOTATO_API_KEY, etc.)"
echo "  2. Execute '/opensquad run shorts-repurposer' para testar"
echo "  3. Consulte skills/local-tts/SKILL.md para opções de voz"
echo ""
