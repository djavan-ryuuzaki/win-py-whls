#!/usr/bin/env python3
# update_readme.py
import json
import re
import argparse
from pathlib import Path
from collections import defaultdict

def load_wheels(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def group_wheels_by_library(wheels):
    """Agrupa wheels por biblioteca (inferida do link)."""
    groups = defaultdict(list)
    for wheel in wheels:
        parts = wheel["download-link"].split('/')
        filename = parts[-1]
        lib_name = filename.split('-')[0]
        groups[lib_name].append(wheel)
    return groups

def generate_wheels_section(wheels_json_path):
    wheels = load_wheels(wheels_json_path)
    if not wheels:
        return "Nenhuma wheel disponível no momento."

    groups = group_wheels_by_library(wheels)

    lines = []
    lines.append("| Biblioteca | Python | PyTorch | CUDA | Download |\n")
    lines.append("|-----------|--------|---------|------|----------|\n")

    for lib in sorted(groups.keys()):
        for entry in sorted(groups[lib], key=lambda x: (x["python-version"], x["torch-version"], x["cuda-version"])):
            link = entry["download-link"]
            filename = link.split('/')[-1]
            py = entry["python-version"]
            torch = entry["torch-version"]
            cuda = entry["cuda-version"]
            lines.append(f"| `{lib}` | {py} | {torch} | {cuda} | [📥 {filename}]({link}) |\n")

    return ''.join(lines)

def update_readme(readme_path, wheels_json_path):
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()

    new_section = generate_wheels_section(wheels_json_path)

    pattern = r"(<!-- BEGIN_WHEELS_SECTION -->).*?(<!-- END_WHEELS_SECTION -->)"
    replacement = f"<!-- BEGIN_WHEELS_SECTION -->\n{new_section}<!-- END_WHEELS_SECTION -->"
    
    updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    print(f"✅ README atualizado com base em {wheels_json_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Atualiza a seção de wheels no README.md")
    parser.add_argument("--readme", default="README.md", help="Caminho para o README.md")
    parser.add_argument("--wheels", default="wheels.json", help="Caminho para wheels.json")
    args = parser.parse_args()

    update_readme(args.readme, args.wheels)