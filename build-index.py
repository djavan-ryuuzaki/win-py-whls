# build_index.py
import os
import re
import json
import argparse
from pathlib import Path

def parse_wheel_filename(filename: str):
    """
    Extrai informações do nome do arquivo .whl.
    Exemplo: biblioteca-1.2.3+cu121torch2.10.0-cp313-cp313-win_amd64.whl
    """
    pattern = r'^(?P<libname>[a-zA-Z0-9_\-]+)-(?P<version>[^+]+)\+cu(?P<cuda>\d+)torch(?P<torch>[\d\.]+)-cp(?P<py>\d+)-cp\d+-win_amd64\.whl$'
    match = re.match(pattern, filename)
    if not match:
        return None

    cuda_version_str = match.group('cuda')
    # Formata para X.Y (ex: '121' -> '12.1')
    if len(cuda_version_str) >= 3:
        cuda_major = cuda_version_str[:-1]
        cuda_minor = cuda_version_str[-1]
        cuda_version = f"{cuda_major}.{cuda_minor}"        
    else:
        # fallback simples
        cuda_version = cuda_version_str

    py_version = f"{match.group('py')[:1]}.{match.group('py')[1:]}.0"

    return {
        "cuda-version": cuda_version,
        "torch-version": match.group('torch'),
        "python-version": py_version,
        "filename": filename,
        "library": match.group('libname'),
        "wheel-version": match.group('version')
    }

def build_index(root_dir: str, output_file: str = "wheels.json", github_repo_url: str = ""):
    root_path = Path(root_dir)
    index = []

    for lib_dir in root_path.iterdir():
        if not lib_dir.is_dir():
            continue
        library_name = lib_dir.name

        for version_dir in lib_dir.iterdir():
            if not version_dir.is_dir():
                continue

            for whl_file in version_dir.glob("*.whl"):
                parsed = parse_wheel_filename(whl_file.name)
                if not parsed or parsed["library"] != library_name.lower().replace(" ", "-"):
                    continue

                rel_path = whl_file.relative_to(root_path)
                download_link = f"{github_repo_url.rstrip('/')}/raw/main/{rel_path.as_posix()}"

                index.append({
                    "cuda-version": parsed["cuda-version"],
                    "torch-version": parsed["torch-version"],
                    "python-version": parsed["python-version"],
                    "download-link": download_link
                })

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)

    print(f"Índice salvo em {output_file} com {len(index)} entradas.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gera wheels.json a partir da estrutura de pastas.")
    parser.add_argument("root", help="Diretório raiz do repositório local")
    parser.add_argument("--output", default="wheels.json", help="Arquivo JSON de saída")
    parser.add_argument("--repo-url", required=True, help="URL pública do repositório GitHub (ex: https://github.com/user/repo)")

    args = parser.parse_args()
    build_index(args.root, args.output, args.repo_url)