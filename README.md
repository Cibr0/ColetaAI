# Coleta Certa — Módulo de Inteligência Artificial

Módulo responsável pelo processamento e pela classificação de imagens do projeto **Coleta Certa**.

O objetivo é desenvolver um sistema de visão computacional capaz de analisar imagens e identificar se elas representam resíduos (lixo) ou não, auxiliando na validação de pontos de coleta.

## Tecnologias utilizadas

| Tecnologia   | Finalidade                             |
| ------------ | -------------------------------------- |
| Python 3.12+ | Linguagem principal                    |
| PyTorch      | Treinamento e execução do modelo de IA |
| Torchvision  | Modelos e transformações de imagens    |
| OpenCV       | Processamento de imagens               |
| Pillow       | Manipulação de imagens                 |
| NumPy        | Operações numéricas                    |
| Matplotlib   | Visualização de dados                  |
| Scikit-learn | Métricas e avaliação do modelo         |
| FastAPI      | API de inferência                      |
| Uvicorn      | Servidor da API                        |
| Jupyter      | Experimentação e desenvolvimento       |

### Modelo de IA planejado

A abordagem inicial será utilizar **MobileNetV3 com Transfer Learning**, aproveitando pesos pré-treinados para adaptar o modelo à classificação de resíduos.

## Estrutura do projeto

```text
ColetaAI/
│
├── data/                  # Conjunto de imagens para treinamento
│
├── models/                # Modelos treinados e pesos
│
├── src/                   # Código-fonte da aplicação
│
├── .gitignore
├── README.md
└── requirements.txt       # Dependências do projeto
```

**Observações:**

- A pasta `data/` é ignorada pelo Git para evitar o envio de grandes conjuntos de imagens.
- Os arquivos de pesos dos modelos (`.pth` e `.h5`) também são ignorados.
- As pastas `src/` e `models/` possuem arquivos `.gitkeep` para permanecerem no repositório enquanto estiverem vazias.

## Como configurar o ambiente

### 1. Pré-requisitos

- Python 3.12 ou superior.
- Git.
- Um editor de código, como Visual Studio Code.

### 2. Clonar o repositório

```bash
git clone URL_DO_REPOSITORIO
```

Entre na pasta do projeto:

```bash
cd ColetaAI
```

### 3. Criar o ambiente virtual

```bash
python -m venv venv
```

### 4. Ativar o ambiente virtual

**Windows:**

```bash
venv\Scripts\activate
```

**Linux/macOS:**

```bash
source venv/bin/activate
```

Após a ativação, o terminal deverá mostrar `(venv)`.

### 5. Instalar as dependências

Com o ambiente virtual ativado, execute:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 6. Verificar a instalação

Execute o comando:

```bash
python -c "import torch, torchvision, numpy, cv2, PIL, matplotlib, sklearn, fastapi, uvicorn, multipart; print('Ambiente configurado com sucesso!')"
```

Se a mensagem aparecer sem erros, as principais bibliotecas foram instaladas corretamente.

## Como executar

**Estado atual do projeto:** o ambiente Python e as dependências já estão configurados. O código de treinamento, o modelo de classificação e a API ainda estão em desenvolvimento.

Quando os arquivos de desenvolvimento forem implementados, as instruções específicas para executar o treinamento e iniciar a API serão adicionadas aqui.

Para iniciar o Jupyter Lab, caso necessário:

```bash
jupyter lab
```

## Arquitetura planejada

O módulo de IA será responsável por receber imagens, processá-las e retornar uma classificação para o back-end principal.

Fluxo previsto:

1. O aplicativo envia uma imagem.
2. O back-end principal encaminha a imagem para a API de IA.
3. A API utiliza o modelo treinado para analisar a imagem.
4. O modelo retorna a classificação e sua probabilidade.
5. O resultado é enviado ao back-end principal.


**Importante:** sempre que novas dependências forem adicionadas ao projeto, atualize o `requirements.txt` para manter o ambiente de desenvolvimento compartilhado entre os integrantes.
