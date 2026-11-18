# ColetaAI — Módulo de Inteligência Artificial

Módulo de inteligência artificial do projeto **Coleta Certa**, responsável por analisar imagens e auxiliar na validação de solicitações de coleta de resíduos.

O objetivo é identificar se uma imagem apresenta resíduos descartados em ambientes externos, contribuindo para a identificação de locais que necessitam de coleta.

---

## Tecnologias utilizadas

| Tecnologia   | Finalidade                                        |
| ------------ | ------------------------------------------------- |
| Python 3.12+ | Linguagem principal                               |
| PyTorch      | Treinamento e execução do modelo                  |
| Torchvision  | Modelos pré-treinados e transformações de imagens |
| OpenCV       | Processamento de imagens                          |
| Pillow       | Manipulação de imagens                            |
| NumPy        | Operações numéricas                               |
| Matplotlib   | Visualização de dados                             |
| Scikit-learn | Métricas e avaliação do modelo                    |
| FastAPI      | API de inferência                                 |
| Uvicorn      | Servidor da API                                   |
| Jupyter      | Experimentação e desenvolvimento                  |

---

## Modelo de inteligência artificial

O projeto utiliza **MobileNetV3 Small** com **Transfer Learning**, aproveitando pesos pré-treinados para adaptar a rede à classificação de imagens de resíduos.

O modelo atual realiza uma classificação binária:

- `valida`: imagem considerada adequada para uma solicitação de coleta.
- `invalida`: imagem considerada inadequada para uma solicitação de coleta.

> **Importante:** a classificação atual ainda não possui uma terceira categoria para imagens inconclusivas. Além disso, o modelo é um protótipo e pode apresentar erros, especialmente em imagens fora dos padrões utilizados no treinamento.

---

## Bases de dados

Foram utilizadas duas bases públicas:

- **TACO (Trash Annotations in Context):** imagens de resíduos em diferentes contextos, com anotações de objetos.
- **WasteInsight:** imagens relacionadas a sacolas plásticas e resíduos.

As imagens foram analisadas e classificadas manualmente conforme sua adequação ao objetivo do projeto.

### Classificação das imagens

| Base de dados | Válidas | Inválidas | Inconclusivas |     Total |
| ------------- | ------: | --------: | ------------: | --------: |
| TACO          |     400 |       278 |           822 |     1.500 |
| WasteInsight  |      45 |         0 |           402 |       447 |
| **Total**     | **445** |   **278** |     **1.224** | **1.947** |

As imagens inconclusivas foram excluídas do treinamento binário.

O arquivo `classificacoes_final.csv` contém os registros das classificações realizadas e é utilizado durante a preparação do conjunto de treinamento.

---

## Resultados do modelo

O treinamento foi realizado durante 10 épocas, utilizando CPU.

| Métrica                                  | Resultado |
| ---------------------------------------- | --------: |
| Acurácia na validação (melhor resultado) |    92,16% |
| Acurácia no teste                        |    95,05% |
| Imagens corretas no teste                | 96 de 101 |

A avaliação utiliza um conjunto de teste separado dos dados de treinamento.

> **Observação:** os resultados representam o desempenho sobre o conjunto de teste utilizado. Eles não garantem a mesma precisão em situações reais, pois o conjunto é relativamente pequeno e possui limitações de variedade.

---

## Estrutura do projeto

```text
ColetaAI/
│
├── api/
│   ├── __init__.py
│   ├── imagem.py         # validação da imagem e transformações
│   ├── main.py           # rotas da API (FastAPI)
│   └── modelo.py         # carregamento do modelo e inferência
│
├── data/                 # não vai para o Git
│   ├── TACO/
│   ├── TACO_previews/
│   ├── WasteInsight/
│   └── processado/
│
├── models/
│
├── src/
│   ├── inspect_dataset.py
│   ├── inspect_wasteinsight.py
│   ├── preview_dataset.py
│   └── preview_wasteinsight.py
│
├── mobilenetv3_coletacerta.pth   # modelo treinado (não vai para o Git)
│
├── avaliar.py
├── classificacoes_final.csv
├── preparar_dataset.py
├── testar_imagem.py
├── treinar.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

### Principais arquivos

| Arquivo                       | Responsabilidade                                                                           |
| ----------------------------- | ------------------------------------------------------------------------------------------ |
| `api/main.py`                 | Define as rotas da API (`/`, `/health` e `/validar-foto`).                                 |
| `api/imagem.py`               | Valida a imagem recebida (formato, tamanho, integridade) e a converte em tensor.           |
| `api/modelo.py`               | Carrega o modelo treinado na inicialização da API e executa a inferência.                  |
| `classificacoes_final.csv`    | Registra a classificação das imagens utilizadas no projeto.                                |
| `preparar_dataset.py`         | Organiza as imagens classificadas e separa os conjuntos de treinamento, validação e teste. |
| `treinar.py`                  | Executa o treinamento da MobileNetV3 Small.                                                |
| `avaliar.py`                  | Avalia o modelo utilizando o conjunto de teste e apresenta as métricas.                    |
| `testar_imagem.py`            | Permite testar a classificação de uma imagem individual, sem a API.                        |
| `src/inspect_dataset.py`      | Script auxiliar para inspeção do dataset TACO.                                             |
| `src/inspect_wasteinsight.py` | Script auxiliar para inspeção do WasteInsight.                                             |
| `src/preview_dataset.py`      | Gera prévias visuais do TACO.                                                              |
| `src/preview_wasteinsight.py` | Gera prévias visuais do WasteInsight.                                                      |

---

## Configuração do ambiente

### 1. Pré-requisitos

- **Python 3.12 ou superior.** Em versões mais antigas (como 3.11), o `pip install` falha, porque o `requirements.txt` usa pacotes que exigem Python 3.12+.
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

No Windows, se houver mais de uma versão do Python instalada, escolha a 3.12 ou superior:

```powershell
py -3.12 -m venv venv
```

> Crie o ambiente dentro da pasta `ColetaAI`. Se a pasta estiver dentro de outro projeto, desative o ambiente virtual do outro projeto antes (`deactivate`), para não misturar as dependências.

### 4. Ativar o ambiente virtual

Windows:

```powershell
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

Após a ativação, o terminal deverá mostrar `(venv)`. Confira a versão do Python com:

```bash
python --version
```

### 5. Instalar as dependências

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

A instalação do PyTorch pode demorar alguns minutos.

---

## Executar a API de inferência

A API recebe uma imagem, valida o arquivo, aplica as mesmas transformações usadas no treinamento, executa o modelo MobileNetV3 Small e retorna a classificação com as probabilidades.

### 1. Coloque o modelo treinado na raiz do projeto

O arquivo do modelo **não vem pelo Git** (arquivos `.pth` são ignorados). Ele precisa estar **na raiz de `ColetaAI`**, ao lado de `treinar.py` e `avaliar.py`, com este nome exato:

```text
ColetaAI/mobilenetv3_coletacerta.pth
```

Há duas formas de obtê-lo:

- Pedir o arquivo para quem já treinou o modelo e copiá-lo para a raiz do projeto.
- Gerar com `python treinar.py` (veja a seção de treinamento). O script salva o modelo em `models/mobilenetv3_coletacerta.pth`, então copie o arquivo gerado para a raiz do projeto.

Sem esse arquivo, a API **não inicia** e mostra `FileNotFoundError: ... mobilenetv3_coletacerta.pth`, porque o modelo é carregado durante a inicialização.

### 2. Suba a API

Na pasta `ColetaAI`, com o ambiente virtual ativo:

```bash
python -m uvicorn api.main:app --reload
```

Também é possível rodar `python api/main.py`.

Quando aparecer `Application startup complete.`, a API está no ar em `http://localhost:8000`. Deixe o terminal aberto. Para parar, use `Ctrl+C`.

### 3. Teste pelo Swagger

1. Abra `http://localhost:8000/docs` no navegador.
2. Clique em **POST /validar-foto** e depois em **Try it out**.
3. Em **imagem**, clique em **Escolher arquivo** e selecione uma foto (JPEG, PNG ou WebP, até 10 MB).
4. Clique em **Execute**.
5. O resultado aparece em **Response body**.

Pelo terminal (no PowerShell use `curl.exe`):

```bash
curl -X POST http://localhost:8000/validar-foto -F "imagem=@caminho/da/foto.jpg"
```

### Rotas

| Método | Rota            | Descrição                                                                               |
| ------ | --------------- | --------------------------------------------------------------------------------------- |
| GET    | `/`             | Status da API.                                                                          |
| GET    | `/health`       | Verificação de integridade.                                                             |
| POST   | `/validar-foto` | Recebe uma imagem (campo multipart `imagem`), valida, classifica e retorna o resultado. |

A rota `/validar-foto` só aceita `POST`. Abrir o endereço direto no navegador mostra `Method Not Allowed`, o que é esperado.

### Exemplo de resposta (200)

```json
{
  "status": "recebida",
  "arquivo": "foto.jpg",
  "formato": "JPEG",
  "largura": 1280,
  "altura": 720,
  "tamanho_bytes": 123775,
  "tensor": [1, 3, 224, 224],
  "classificacao": "valida",
  "probabilidades": {
    "invalida": 0.0123,
    "valida": 0.9877
  }
}
```

- `classificacao`: classe com maior probabilidade (`valida` ou `invalida`).
- `probabilidades`: probabilidade de cada classe, entre 0 e 1.

### Respostas de erro

| Situação                        | Código | Resposta                                                     |
| ------------------------------- | -----: | ------------------------------------------------------------ |
| Arquivo vazio                   |    400 | `Arquivo vazio.`                                             |
| Imagem corrompida ou incompleta |    400 | `Imagem corrompida ou incompleta.`                           |
| Acima de 10 MB                  |    413 | `Arquivo excede o tamanho máximo de 10 MB.`                  |
| Formato não suportado           |    415 | `Formato não suportado. Envie uma imagem JPEG, PNG ou WebP.` |
| Requisição sem arquivo          |    422 | Validação padrão do FastAPI.                                 |

### Problemas comuns

| Erro                                                | Causa provável                                                              |
| --------------------------------------------------- | --------------------------------------------------------------------------- |
| `FileNotFoundError ... mobilenetv3_coletacerta.pth` | O modelo não está na raiz de `ColetaAI`.                                    |
| `ModuleNotFoundError: No module named 'api'`        | O comando não foi executado dentro da pasta `ColetaAI`.                     |
| `No module named 'torch'` (ou `fastapi`)            | O ambiente virtual não está ativo ou as dependências não foram instaladas.  |
| `pip install` falha com `numpy==2.5.4`              | O Python é anterior ao 3.12. Recrie o ambiente com Python 3.12 ou superior. |
| A página `/docs` não abre                           | A API não está rodando. Veja o terminal onde o `uvicorn` foi iniciado.      |

---

## Preparação dos dados

Os conjuntos de imagens não são armazenados no Git. Portanto, antes de executar o treinamento, é necessário obter as bases de dados e organizá-las dentro da pasta `data/`.

Estrutura esperada:

- `data/TACO/`: imagens e arquivo de anotações do TACO.
- `data/WasteInsight/`: imagens separadas nos diretórios `train`, `valid` e `test`.
- `classificacoes_final.csv`: arquivo de classificações presente na raiz do projeto.

Com os dados organizados, execute:

```bash
python preparar_dataset.py
```

O script utiliza as classificações para selecionar as imagens válidas e inválidas, excluindo as inconclusivas, e cria os conjuntos necessários em `data/processado/`.

### Distribuição preparada

| Conjunto    | Imagens |
| ----------- | ------: |
| Treinamento |     509 |
| Validação   |     102 |
| Teste       |     101 |
| **Total**   | **712** |

---

## Treinamento do modelo

Com o conjunto de dados preparado, execute:

```bash
python treinar.py
```

O script realiza o treinamento da MobileNetV3 Small utilizando Transfer Learning.

Ao final, o modelo treinado é salvo em:

```text
models/mobilenetv3_coletacerta.pth
```

O treinamento utiliza o melhor resultado de validação para salvar o checkpoint do modelo.

> Para usar o modelo na API, copie o arquivo gerado para a raiz do projeto (`ColetaAI/mobilenetv3_coletacerta.pth`).

---

## Avaliação do modelo

Para avaliar o desempenho do modelo utilizando o conjunto de teste:

```bash
python avaliar.py
```

O script apresenta métricas como:

- Acurácia.
- Precisão.
- Recall.
- F1-score.
- Matriz de confusão.

A avaliação deve ser executada após o treinamento e a geração do arquivo do modelo.

---

## Testar uma imagem individual

Para testar uma imagem utilizando o modelo treinado, sem usar a API:

```bash
python testar_imagem.py
```

O programa solicitará o caminho da imagem. Informe o caminho completo, por exemplo:

```text
C:\Users\Usuario\Pictures\imagem.jpg
```

O resultado apresenta a classe prevista pelo modelo e as probabilidades correspondentes.

> Este script e o `avaliar.py` procuram o modelo em `models/mobilenetv3_coletacerta.pth`, enquanto a API procura na raiz do projeto. Se for usar os dois, mantenha uma cópia do arquivo em cada lugar.

---

## Observações importantes

- A pasta `data/` é ignorada pelo Git para evitar o envio das bases de imagens e dos conjuntos processados.
- Os arquivos de pesos `.pth` também são ignorados pelo Git. **Não faça commit do modelo.**
- O modelo treinado precisa ser gerado localmente por meio do script `treinar.py` ou disponibilizado separadamente.
- Para executar o treinamento em uma nova instalação, é necessário obter as bases de dados e preparar o conjunto processado.
- A API carrega o modelo uma única vez, na inicialização. Se o arquivo do modelo for trocado, reinicie a API.

---

## Próximas etapas

- Integrar a API ao back-end principal do Coleta Certa.
- Realizar testes de comunicação entre os serviços.
- Avaliar a inclusão de uma terceira categoria para imagens inconclusivas.

---

**ColetaAI — Módulo de Inteligência Artificial do Coleta Certa.**
