# Repositório de Wheels Pré-compilados para Windows

Este repositório fornece **wheels pré-compilados de bibliotecas Python** para Windows (64-bit), especialmente otimizados para ambientes com **PyTorch + CUDA**.  
As builds incluem suporte a diferentes versões de **Python**, **PyTorch** e **CUDA**, facilitando a instalação em ambientes onde compilar do zero é inviável.

Os arquivos seguem a convenção:

biblioteca-versao+cu[versao_cuda]torch[versao_torch]-cp[py]-cp[py]-win_amd64.whl

Exemplo:  
`minhabib-1.0.0+cu121torch2.10.0-cp313-cp313-win_amd64.whl`

---

## 🚀 Como usar

### Passo 1: Baixe os scripts auxiliares
Baixe os seguintes arquivos para seu ambiente local:
- [`find_wheel.py`](./find_wheel.py) — encontra a wheel compatível com seu sistema.
- [`wheels.json`](./wheels.json) — índice atualizado de todas as wheels disponíveis.

> 💡 Você também pode clonar este repositório inteiro.

### Passo 2: Execute o buscador
Com PyTorch instalado e CUDA configurado, execute:

```bash
python find_wheel.py nome_da_biblioteca

biblioteca-versao+cu[versao_cuda]torch[versao_torch]-cp[py]-cp[py]-win_amd64.whl

12345678910111213141516171819
Exemplo:  
`minhabib-1.0.0+cu121torch2.10.0-cp313-cp313-win_amd64.whl`

---

## 🚀 Como usar

### Passo 1: Baixe os scripts auxiliares
Baixe os seguintes arquivos para seu ambiente local:
- [`find_wheel.py`](./find_wheel.py) — encontra a wheel compatível com seu sistema.

O script irá:

Detectar automaticamente sua versão do Python, PyTorch e CUDA do sistema (via nvcc ou variáveis de ambiente).
Comparar com as builds disponíveis.
Exibir o link direto para download da wheel compatível.
Use --use-torch-cuda se quiser priorizar a versão do CUDA usada pelo PyTorch em vez da instalada no sistema.

Passo 3: Instale a wheel
Copie o link exibido e instale com pip:

bash
1
pip install "https://github.com/seu-usuario/seu-repo/raw/main/..."
🔁 Substitua seu-usuario/seu-repo pela URL real do seu repositório antes de publicar!

📥 Wheels Disponíveis
<!-- BEGIN_WHEELS_SECTION -->
| Biblioteca | Python | PyTorch | CUDA | Download |
|-----------|--------|---------|------|----------|
| `sageattention` | 3.13.0 | 2.10.0 | 13.1 | [📥 sageattention-2.2.0+cu131torch2.10.0-cp313-cp313-win_amd64.whl](https://github.com/djavan-ryuuzaki/win-py-whls/raw/main/SageAttention/2.2.0/sageattention-2.2.0+cu131torch2.10.0-cp313-cp313-win_amd64.whl) |
<!-- END_WHEELS_SECTION -->

🛠️ Atualizando o Índice (para mantenedores)
Adicione novas wheels na estrutura de pastas (biblioteca/versão/arquivo.whl).
Execute:
bash
1
python build_index.py . --repo-url https://github.com/seu-usuario/seu-repo
Atualize o README:
bash
1
python update_readme.py
Faça commit das mudanças (wheels.json, README.md, e os novos .whl).
