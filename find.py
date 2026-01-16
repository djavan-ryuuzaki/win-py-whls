# find_wheel.py
import json
import sys
import subprocess
import argparse
import os
import re

def get_cuda_version_from_system():
    """Tenta obter a versão do CUDA instalada no sistema."""
    cuda_version = None

    # Método 1: nvcc
    try:
        result = subprocess.run(["nvcc", "--version"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            match = re.search(r"release (\d+)\.(\d+)", result.stdout)
            if match:
                cuda_version = f"{match.group(1)}.{match.group(2)}"
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    # Método 2: variável de ambiente CUDA_PATH ou CUDA_HOME
    if not cuda_version:
        cuda_path = os.environ.get("CUDA_PATH") or os.environ.get("CUDA_HOME")
        if cuda_path:
            version_file = os.path.join(cuda_path, "version.txt")
            if os.path.isfile(version_file):
                try:
                    with open(version_file, "r") as f:
                        content = f.read()
                        match = re.search(r"(\d+)\.(\d+)", content)
                        if match:
                            cuda_version = f"{match.group(1)}.{match.group(2)}"
                except Exception:
                    pass
            # Também tenta extrair da pasta (ex: C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.1)
            elif "CUDA" in cuda_path:
                match = re.search(r"[\\/vV]?(\d+)\.(\d+)", cuda_path)
                if match:
                    cuda_version = f"{match.group(1)}.{match.group(2)}"

    return cuda_version

def get_torch_cuda_version():
    """Obtém a versão do CUDA com a qual o PyTorch foi compilado."""
    try:
        import torch
        return torch.version.cuda  # ex: '12.1'
    except ImportError:
        return None

def get_python_version():
    return f"{sys.version_info.major}.{sys.version_info.minor}.0"

def get_torch_version():
    try:
        import torch
        return torch.__version__.split('+')[0]
    except ImportError:
        return None

def normalize_cuda_for_matching(cuda_str):
    """Converte '12.1' → '12.1' (já ok), mas garante string limpa."""
    if cuda_str is None:
        return None
    # Remove qualquer coisa além de dígitos e ponto
    clean = re.sub(r'[^\d.]', '', str(cuda_str))
    return clean

def find_matching_wheel(wheels, py_ver, torch_ver, cuda_ver):
    """Busca uma roda compatível com as versões fornecidas."""
    for entry in wheels:
        if (
            entry["python-version"] == py_ver and
            entry["torch-version"] == torch_ver and
            entry["cuda-version"] == cuda_ver
        ):
            return entry["download-link"]
    return None

def main():
    parser = argparse.ArgumentParser(description="Encontra wheel compatível usando CUDA do sistema.")
    parser.add_argument("library", help="Nome da biblioteca desejada")
    parser.add_argument("--index", default="wheels.json", help="Arquivo JSON com índice das wheels")
    parser.add_argument("--use-torch-cuda", action="store_true", help="Usar versão CUDA do PyTorch em vez da do sistema")
    args = parser.parse_args()

    # Carrega índice
    try:
        with open(args.index, "r", encoding="utf-8") as f:
            wheels = json.load(f)
    except FileNotFoundError:
        print(f"Erro: {args.index} não encontrado. Execute build_index.py primeiro.")
        sys.exit(1)

    # Detecta versões
    py_ver = get_python_version()
    torch_ver = get_torch_version()
    system_cuda = get_cuda_version_from_system()
    torch_cuda = get_torch_cuda_version()

    if torch_ver is None:
        print("PyTorch não está instalado. Não é possível determinar a versão do Torch.")
        sys.exit(1)

    print(f"🔍 Detectado:")
    print(f"   Python: {py_ver}")
    print(f"   PyTorch: {torch_ver}")
    print(f"   CUDA do sistema: {system_cuda or 'Não detectada'}")
    print(f"   CUDA do PyTorch:  {torch_cuda or 'Não disponível'}")

    # Verifica divergência
    if system_cuda and torch_cuda and system_cuda != torch_cuda:
        print("\n⚠️  Aviso: A versão do CUDA do sistema é diferente da usada pelo PyTorch!")
        if not args.use_torch_cuda:
            print("   Usando a versão do CUDA do sistema para busca.")
        else:
            print("   Opção --use-torch-cuda ativada: usando CUDA do PyTorch.")

    # Decide qual CUDA usar
    if args.use_torch_cuda and torch_cuda:
        cuda_to_use = torch_cuda
        print(f"\n⚙️  Usando CUDA do PyTorch: {cuda_to_use}")
    elif system_cuda:
        cuda_to_use = system_cuda
        print(f"\n⚙️  Usando CUDA do sistema: {cuda_to_use}")
    elif torch_cuda:
        print("\nℹ️  CUDA do sistema não encontrada. Usando CUDA do PyTorch por fallback.")
        cuda_to_use = torch_cuda
    else:
        print("\n❌ Nenhuma versão de CUDA detectada (nem no sistema nem no PyTorch).")
        sys.exit(1)

    # Normaliza para comparação exata (o JSON espera formato X.Y)
    cuda_to_use = normalize_cuda_for_matching(cuda_to_use)

    # Busca a wheel
    link = find_matching_wheel(wheels, py_ver, torch_ver, cuda_to_use)
    if link:
        print(f"\n✅ Wheel compatível encontrada!\n🔗 {link}")
    else:
        print(f"\n❌ Nenhuma wheel encontrada para:")
        print(f"   Python={py_ver}, Torch={torch_ver}, CUDA={cuda_to_use}")
        print("Verifique se há builds disponíveis para essa combinação no repositório.")

if __name__ == "__main__":
    main()