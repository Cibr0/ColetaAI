# ColetaAI — Módulo de Inteligência Artificial

Módulo de inteligência artificial do projeto **Coleta Certa**, responsável por analisar imagens e auxiliar na validação de solicitações de coleta de resíduos.

O objetivo é identificar se uma imagem apresenta resíduos descartados em ambientes externos, contribuindo para a identificação de locais que necessitam de coleta.

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
| FastAPI      | Tecnologia prevista para a API de inferência      |
| Uvicorn      | Servidor previsto para a API                      |
| Jupyter      | Experimentação e desenvolvimento                  |

## Modelo de inteligência artificial

O projeto utiliza **MobileNetV3 Small com Transfer Learning**, aproveitando pesos pré-treinados para adaptar a rede à classificação de imagens de resíduos.

O modelo atual realiza uma classificação binária:

- `valida`: imagem considerada adequada para uma solicitação de coleta.
- `invalida`: imagem considerada inadequada para uma solicitação de coleta.

**Importante:** a classificação atual ainda não possui uma terceira categoria para imagens inconclusivas. Além disso, o modelo é um protótipo e pode apresentar erros, especialmente em imagens fora dos padrões utilizados no treinamento.

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

## Resultados do modelo

O treinamento foi realizado durante 10 épocas, utilizando CPU.

| Métrica                                  | Resultado |
| ---------------------------------------- | --------: |
| Acurácia na validação (melhor resultado) |    92,16% |
| Acurácia no teste                        |    95,05% |
| Imagens corretas no teste                | 96 de 101 |

A avaliação utiliza um conjunto de teste separado dos dados de treinamento.

**Observação:** os resultados representam o desempenho sobre o conjunto de teste utilizado. Eles não garantem a mesma precisão em situações reais, pois o conjunto é relativamente pequeno e possui limitações de variedade.

## Estrutura do projeto

```text
ColetaAI/
│
├── data/
│   ├── TACO/
│   ├── TACO_previews/
│   ├── WasteInsight/
│   └── processado/
│
├── models/
│   └── mobilenetv3_coletacerta.pth
│
├── src/
│   ├── inspect_dataset.py
│   ├── inspect_wasteinsight.py
│   ├── preview_dataset.py
│   └── preview_wasteinsight.py
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
| `classificacoes_final.csv`    | Registra a classificação das imagens utilizadas no projeto.                                |
| `preparar_dataset.py`         | Organiza as imagens classificadas e separa os conjuntos de treinamento, validação e teste. |
| `treinar.py`                  | Executa o treinamento da MobileNetV3 Small.                                                |
| `avaliar.py`                  | Avalia o modelo utilizando o conjunto de teste e apresenta as métricas.                    |
| `testar_imagem.py`            | Permite testar a classificação de uma imagem individual.                                   |
| `src/inspect_dataset.py`      | Script auxiliar para inspeção do dataset TACO.                                             |
| `src/inspect_wasteinsight.py` | Script auxiliar para inspeção do WasteInsight.                                             |
| `src/preview_dataset.py`      | Gera prévias visuais do TACO.                                                              |
| `src/preview_wasteinsight.py` | Gera prévias visuais do WasteInsight.                                                      |

## Configuração do ambiente

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

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

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

Distribuição preparada:

| Conjunto    | Imagens |
| ----------- | ------: |
| Treinamento |     509 |
| Validação   |     102 |
| Teste       |     101 |
| **Total**   | **712** |

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

## Testar uma imagem individual

Para testar uma imagem utilizando o modelo treinado:

```bash
python testar_imagem.py
```

O programa solicitará o caminho da imagem. Informe o caminho completo, por exemplo:

```text
C:\Users\Usuario\Pictures\imagem.jpg
```

O resultado apresenta a classe prevista pelo modelo e as probabilidades correspondentes.

## Observações importantes

- A pasta `data/` é ignorada pelo Git para evitar o envio das bases de imagens e dos conjuntos processados.
- Os arquivos de pesos `.pth` também são ignorados pelo Git.
- O modelo treinado precisa ser gerado localmente por meio do script `treinar.py` ou disponibilizado separadamente.
- Para executar o treinamento em uma nova instalação, é necessário obter as bases de dados e preparar o conjunto processado.
- O projeto ainda não possui uma API de inferência implementada. A integração com o back-end principal será realizada em uma etapa posterior.

## Próximas etapas

1. Implementar uma API de inferência utilizando FastAPI.
2. Criar um endpoint para receber imagens e retornar a classificação do modelo.
3. Integrar a API ao back-end principal do Coleta Certa.
4. Realizar testes de comunicação entre os serviços.

---

**ColetaAI — Módulo de Inteligência Artificial do Coleta Certa.**
