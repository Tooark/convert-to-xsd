# Conversor de JSON Plano para JSON Aninhado, XML e XSD

Ferramenta simples para converter JSON "plano" (flat) em `JSON` aninhado, gerar
um arquivo `XML` correspondente e produzir esquemas `XSD` (incluindo uma versão
com prefixo `xsd:` compatível com sistemas como o SAP).

## Visão geral

O script principal é `convert.py`. Ele pode ser executado diretamente com
`python convert.py` ou instalado como um comando (entry-point) chamado
`convert-to-xsd` (veja seção de instalação).

Principais comportamentos:

- Converte chaves no formato pontuado (ex: `a.b[1].c`) para estrutura `JSON` aninhada.
- Gera arquivos de saída ao lado do arquivo de entrada: `JSON` aninhado, `XML`, `XSD`, `XSD` para SAP (`*_SAP.xsd`) e um arquivo de mapeamento de nomes alterados (`*_change_name.json`).
- Quando executado sem parâmetros, processa todos os arquivos presentes na pasta `files/` (cria essa pasta se não existir e tenta mover `example.txt` para dentro).

## Requisitos

- Python 3.8 ou superior
- Biblioteca `lxml` (instalada via `requirements.txt`)

## Instalação

Uso rápido (ambiente virtual):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1   # PowerShell (Windows)
# ou (CMD): .venv\Scripts\activate.bat
# ou (Linux/macOS): source .venv/bin/activate
pip install -r requirements.txt
```

Instalar como pacote (para obter o comando `convert-to-xsd`):

```bash
pip install .     # instalação local
pip install -e .  # ou para desenvolvimento com edição ao vivo
```

> O entry-point CLI é definido em `setup.cfg` como `convert-to-xsd = convert:main`.

## Uso

Sintaxe:

```text
python convert.py [--root ROOT_NAME] [--json] [--xml] [--xsd] [--sap] [paths...]
# ou, se instalado
convert-to-xsd [--root ROOT_NAME] [--json] [--xml] [--xsd] [--sap] [paths...]
```

| Argumento      | Descrição                                                                                                                                                  |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `paths`        | Arquivo(s) ou diretório(s) a converter. Quando um diretório é informado, todos os `.json` e `.txt` dentro dele são processados. Aceita múltiplos caminhos. |
| `--root`, `-r` | Nome do elemento raiz (padrão: nome do arquivo sem extensão).                                                                                              |
| `--json`, `-j` | Salva somente o arquivo `.json` aninhado.                                                                                                                  |
| `--xml`, `-x`  | Salva somente o arquivo `.xml`.                                                                                                                            |
| `--xsd`, `-d`  | Salva somente o arquivo `.xsd`.                                                                                                                            |
| `--sap`, `-s`  | Salva somente o arquivo `_SAP.xsd` (prefixo `xsd:`).                                                                                                       |

> **Padrão:** quando nenhuma flag de saída (`--json`, `--xml`, `--xsd`, `--sap`) é informada, **todos** os formatos são gerados. Ao passar uma ou mais flags, apenas os formatos selecionados são salvos.

Exemplos:

- Converter um arquivo específico (gera todos os formatos):

```bash
python convert.py example.txt
```

- Gerar apenas XSD e SAP:

```bash
python convert.py --xsd --sap example.txt
```

- Especificar o nome do elemento raiz:

```bash
python convert.py --root MeuRoot example.txt
```

- Processar um diretório inteiro (apenas `.json` e `.txt`):

```bash
python convert.py files/
```

- Processar múltiplos caminhos ao mesmo tempo:

```bash
python convert.py files/ dados/input.json
```

- Exibir a ajuda (sem parâmetros):

```bash
python convert.py
```

## Formato de entrada

O arquivo de entrada deve conter JSON válido (o projeto usa `json.loads`), mesmo que o arquivo esteja com extensão `.txt`. As chaves podem usar o formato "pontuado" para indicar aninhamento e índices de arrays, por exemplo:

```json
{
  "serviceContextId": "123a654b-a1b2-c3d4-e5f6-12345f65f98e",
  "data": {
    "K-Application.Id": "ABCD001122334455",
    "K-Application.Decision.Name": "TesteNome",
    "K-Application.Order": "08",
    "K-Application.Client.DataClient[1].Concentrate.RegistrationData.Name": "AAAAAA",
    "K-Application.Client.DataClient[1].Concentrate.Score.Value": "BBBBBB",
    "K-Application.Client.DataClient[1].Dist.Score.Model[1]": "CCCCCC",
    "K-Application.Client.DataClient[1].Dist.Score.Model[2]": "DDDDDD",
    "K-Application.Client.DataClient[2].Concentrate.RegistrationData.Name": "EEEEEE",
    "K-Application.Client.DataClient[2].Concentrate.Score.Value": "FFFFFF",
    "K-Application.Client.DataClient[2].Dist.Score.Model[1]": "GGGGGG",
    "K-Application.Client.DataClient[2].Dist.Score.Model[2]": "HHHHHH",
    "Error.Message[1].IdMessage": "HHHHHH",
    "Key.A-set.Value[1]": "IIIIII",
    "Key.A-set.Value[2]": "JJJJJJ",
    "Key.A-set.Value[3]": "KKKKKK",
    "Key.A-set.Value[4]": "LLLLLL",
    "Key.A-set.Value[5]": "MMMMMM"
  }
}
```

### Arquivo de Saída (`example.json`)

```json
{
  "data": {
    "Error": {
      "Message": [
        {
          "IdMessage": "HHHHHH"
        }
      ]
    },
    "K-Application": {
      "Client": {
        "DataClient": [
          {
            "Concentrate": {
              "RegistrationData": {
                "Name": "AAAAAA"
              },
              "Score": {
                "Value": "BBBBBB"
              }
            },
            "Dist": {
              "Score": {
                "Model": ["CCCCCC", "DDDDDD"]
              }
            }
          },
          {
            "Concentrate": {
              "RegistrationData": {
                "Name": "EEEEEE"
              },
              "Score": {
                "Value": "FFFFFF"
              }
            },
            "Dist": {
              "Score": {
                "Model": ["GGGGGG", "HHHHHH"]
              }
            }
          }
        ]
      },
      "Decision": {
        "Name": "TesteNome"
      },
      "Id": "ABCD001122334455",
      "Order": "08"
    },
    "Key": {
      "A-set": {
        "Value": ["IIIIII", "JJJJJJ", "KKKKKK", "LLLLLL", "MMMMMM"]
      }
    }
  },
  "serviceContextId": "123a654b-a1b2-c3d4-e5f6-12345f65f98e"
}
```

### Arquivo de Saída (`example.xml`)

```xml
<?xml version="1.0"?>
<example>
  <data>
    <Error>
      <Message>
        <IdMessage>HHHHHH</IdMessage>
      </Message>
    </Error>
    <K_Application>
      <Client>
        <DataClient>
          <Concentrate>
            <RegistrationData>
              <Name>AAAAAA</Name>
            </RegistrationData>
            <Score>
              <Value>BBBBBB</Value>
            </Score>
          </Concentrate>
          <Dist>
            <Score>
              <Model>CCCCCC</Model>
              <Model>DDDDDD</Model>
            </Score>
          </Dist>
        </DataClient>
        <DataClient>
          <Concentrate>
            <RegistrationData>
              <Name>EEEEEE</Name>
            </RegistrationData>
            <Score>
              <Value>FFFFFF</Value>
            </Score>
          </Concentrate>
          <Dist>
            <Score>
              <Model>GGGGGG</Model>
              <Model>HHHHHH</Model>
            </Score>
          </Dist>
        </DataClient>
      </Client>
      <Decision>
        <Name>TesteNome</Name>
      </Decision>
      <Id>ABCD001122334455</Id>
      <Order>08</Order>
    </K_Application>
    <Key>
      <A_set>
        <Value>IIIIII</Value>
        <Value>JJJJJJ</Value>
        <Value>KKKKKK</Value>
        <Value>LLLLLL</Value>
        <Value>MMMMMM</Value>
      </A_set>
    </Key>
  </data>
  <serviceContextId>123a654b-a1b2-c3d4-e5f6-12345f65f98e</serviceContextId>
</example>
```

### Arquivo de Saída (`example.xsd`)

```xml
<?xml version='1.0' encoding='utf-8'?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:complexType name="example">
    <xs:sequence>
      <xs:element name="data">
        <xs:complexType>
          <xs:sequence>
            <xs:element name="Error">
              <xs:complexType>
                <xs:sequence>
                  <xs:element name="Message" minOccurs="0" maxOccurs="unbounded">
                    <xs:complexType>
                      <xs:sequence>
                        <xs:element name="IdMessage" type="xs:string" minOccurs="0" maxOccurs="1"/>
                      </xs:sequence>
                    </xs:complexType>
                  </xs:element>
                </xs:sequence>
              </xs:complexType>
            </xs:element>
            <xs:element name="K_Application">
              <xs:complexType>
                <xs:sequence>
                  <xs:element name="Client">
                    <xs:complexType>
                      <xs:sequence>
                        <xs:element name="DataClient" minOccurs="0" maxOccurs="unbounded">
                          <xs:complexType>
                            <xs:sequence>
                              <xs:element name="Concentrate">
                                <xs:complexType>
                                  <xs:sequence>
                                    <xs:element name="RegistrationData">
                                      <xs:complexType>
                                        <xs:sequence>
                                          <xs:element name="Name" type="xs:string" minOccurs="0" maxOccurs="1"/>
                                        </xs:sequence>
                                      </xs:complexType>
                                    </xs:element>
                                    <xs:element name="Score">
                                      <xs:complexType>
                                        <xs:sequence>
                                          <xs:element name="Value" type="xs:string" minOccurs="0" maxOccurs="1"/>
                                        </xs:sequence>
                                      </xs:complexType>
                                    </xs:element>
                                  </xs:sequence>
                                </xs:complexType>
                              </xs:element>
                              <xs:element name="Dist">
                                <xs:complexType>
                                  <xs:sequence>
                                    <xs:element name="Score">
                                      <xs:complexType>
                                        <xs:sequence>
                                          <xs:element name="Model" type="xs:string" minOccurs="0" maxOccurs="unbounded"/>
                                        </xs:sequence>
                                      </xs:complexType>
                                    </xs:element>
                                  </xs:sequence>
                                </xs:complexType>
                              </xs:element>
                            </xs:sequence>
                          </xs:complexType>
                        </xs:element>
                      </xs:sequence>
                    </xs:complexType>
                  </xs:element>
                  <xs:element name="Decision">
                    <xs:complexType>
                      <xs:sequence>
                        <xs:element name="Name" type="xs:string" minOccurs="0" maxOccurs="1"/>
                      </xs:sequence>
                    </xs:complexType>
                  </xs:element>
                  <xs:element name="Id" type="xs:string" minOccurs="0" maxOccurs="1"/>
                  <xs:element name="Order" type="xs:string" minOccurs="0" maxOccurs="1"/>
                </xs:sequence>
              </xs:complexType>
            </xs:element>
            <xs:element name="Key">
              <xs:complexType>
                <xs:sequence>
                  <xs:element name="A_set">
                    <xs:complexType>
                      <xs:sequence>
                        <xs:element name="Value" type="xs:string" minOccurs="0" maxOccurs="unbounded"/>
                      </xs:sequence>
                    </xs:complexType>
                  </xs:element>
                </xs:sequence>
              </xs:complexType>
            </xs:element>
          </xs:sequence>
        </xs:complexType>
      </xs:element>
      <xs:element name="serviceContextId" type="xs:string" minOccurs="0" maxOccurs="1"/>
    </xs:sequence>
  </xs:complexType>
</xs:schema>
```

### Arquivo de Saída (`example_SAP.xsd`)

```xml
<?xml version='1.0' encoding='utf-8'?>
<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema">
  <xsd:complexType name="example">
    <xsd:sequence>
      <xsd:element name="data">
        <xsd:complexType>
          <xsd:sequence>
            <xsd:element name="Error">
              <xsd:complexType>
                <xsd:sequence>
                  <xsd:element name="Message" minOccurs="0" maxOccurs="unbounded">
                    <xsd:complexType>
                      <xsd:sequence>
                        <xsd:element name="IdMessage" type="xsd:string" minOccurs="0" maxOccurs="1"/>
                      </xsd:sequence>
                    </xsd:complexType>
                  </xsd:element>
                </xsd:sequence>
              </xsd:complexType>
            </xsd:element>
            <xsd:element name="K_Application">
              <xsd:complexType>
                <xsd:sequence>
                  <xsd:element name="Client">
                    <xsd:complexType>
                      <xsd:sequence>
                        <xsd:element name="DataClient" minOccurs="0" maxOccurs="unbounded">
                          <xsd:complexType>
                            <xsd:sequence>
                              <xsd:element name="Concentrate">
                                <xsd:complexType>
                                  <xsd:sequence>
                                    <xsd:element name="RegistrationData">
                                      <xsd:complexType>
                                        <xsd:sequence>
                                          <xsd:element name="Name" type="xsd:string" minOccurs="0" maxOccurs="1"/>
                                        </xsd:sequence>
                                      </xsd:complexType>
                                    </xsd:element>
                                    <xsd:element name="Score">
                                      <xsd:complexType>
                                        <xsd:sequence>
                                          <xsd:element name="Value" type="xsd:string" minOccurs="0" maxOccurs="1"/>
                                        </xsd:sequence>
                                      </xsd:complexType>
                                    </xsd:element>
                                  </xsd:sequence>
                                </xsd:complexType>
                              </xsd:element>
                              <xsd:element name="Dist">
                                <xsd:complexType>
                                  <xsd:sequence>
                                    <xsd:element name="Score">
                                      <xsd:complexType>
                                        <xsd:sequence>
                                          <xsd:element name="Model" type="xsd:string" minOccurs="0" maxOccurs="unbounded"/>
                                        </xsd:sequence>
                                      </xsd:complexType>
                                    </xsd:element>
                                  </xsd:sequence>
                                </xsd:complexType>
                              </xsd:element>
                            </xsd:sequence>
                          </xsd:complexType>
                        </xsd:element>
                      </xsd:sequence>
                    </xsd:complexType>
                  </xsd:element>
                  <xsd:element name="Decision">
                    <xsd:complexType>
                      <xsd:sequence>
                        <xsd:element name="Name" type="xsd:string" minOccurs="0" maxOccurs="1"/>
                      </xsd:sequence>
                    </xsd:complexType>
                  </xsd:element>
                  <xsd:element name="Id" type="xsd:string" minOccurs="0" maxOccurs="1"/>
                  <xsd:element name="Order" type="xsd:string" minOccurs="0" maxOccurs="1"/>
                </xsd:sequence>
              </xsd:complexType>
            </xsd:element>
            <xsd:element name="Key">
              <xsd:complexType>
                <xsd:sequence>
                  <xsd:element name="A_set">
                    <xsd:complexType>
                      <xsd:sequence>
                        <xsd:element name="Value" type="xsd:string" minOccurs="0" maxOccurs="unbounded"/>
                      </xsd:sequence>
                    </xsd:complexType>
                  </xsd:element>
                </xsd:sequence>
              </xsd:complexType>
            </xsd:element>
          </xsd:sequence>
        </xsd:complexType>
      </xsd:element>
      <xsd:element name="serviceContextId" type="xsd:string" minOccurs="0" maxOccurs="1"/>
    </xsd:sequence>
  </xsd:complexType>
</xsd:schema>
```

### Arquivo de Saída (`example_change_name.json`)

```json
{
  "A-set": "A_set",
  "K-Application": "K_Application"
}
```

## 📄 Arquivos do Projeto

```plaintext
convert-to-xsd/
├── .gitignore        # Arquivo de configuração do Git
├── convert.py        # Script Python
├── example.txt       # Arquivo de exemplo
├── LICENSE           # Licença do projeto
├── README.md         # Este arquivo
└── requirements.txt  # Dependências do projeto
```

## Saídas geradas

Para cada arquivo de entrada `nome.ext` serão gerados (no mesmo diretório do arquivo de entrada):

| Arquivo                 | Condição                                 |
| ----------------------- | ---------------------------------------- |
| `nome.json`             | Sempre (ou quando `--json` informado)    |
| `nome.xml`              | Sempre (ou quando `--xml` informado)     |
| `nome.xsd`              | Sempre (ou quando `--xsd` informado)     |
| `nome_SAP.xsd`          | Sempre (ou quando `--sap` informado)     |
| `nome_change_name.json` | Sempre — mapeamento de nomes sanitizados |

> Quando **nenhuma** flag de saída é informada, todos os formatos acima são gerados.
> Quando **uma ou mais** flags são informadas, apenas os formatos correspondentes são salvos.

Obs.: o arquivo `*_change_name.json` registra substituições feitas em nomes de elementos XML inválidos (caracteres trocados por `_`).

## Validação

O script tenta validar o XML gerado contra o XSD correspondente e imprime o
resultado. Caso a validação falhe, o log de erros será mostrado no console.

## Desenvolvimento

- Faça fork e crie uma branch para sua feature/bugfix.
- Abra um pull request descrevendo a mudança.
- Mantenha commits pequenos e com mensagens claras.

Recomendações locais:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]         # se houver extras de desenvolvimento
python convert.py example.txt # Execute o script diretamente para testes rápidos
```

Este projeto está licenciado sob a Licença MIT — veja o arquivo [LICENSE](LICENSE) para detalhes.

## CI/CD — Publicação no PyPI

Este repositório inclui um workflow do GitHub Actions que constrói o pacote e publica no PyPI.

- Arquivo do workflow: `.github/workflows/publish-pypi.yml`.
- O workflow roda automaticamente quando você cria uma _tag_ no formato `vX.Y.Z` (push de tag), quando uma _release_ é publicada no GitHub, ou manualmente via _workflow_dispatch_.

Requisitos e passos para habilitar publicação automática:

1. Crie um token de API no PyPI: [https://pypi.org/manage/account/token/](https://pypi.org/manage/account/token/)
   - Nomeie o token (ex.: `github-actions-tooark`).
   - Dê permissão para publicar o(s) pacote(s) desejados (escopo apropriado).

2. No repositório GitHub (ou em `Organization > Settings > Secrets` se quiser compartilhar em vários repositórios), adicione um _secret_ chamado `PYPI_API_TOKEN` com o valor do token criado.

3. Para publicar, crie e envie uma tag seguindo semântica de versão, por exemplo:

```bash
git tag v1.2.3
git push origin v1.2.3
```

O workflow irá:

- instalar as dependências de build (`build`, `twine`)
- executar `python -m build` para gerar `dist/*`
- executar `twine upload dist/*` usando o secret `PYPI_API_TOKEN`

Observações:

- O token deve ter permissão para publicar o pacote no PyPI; se o pacote pertence à organização `tooark` no PyPI, o token precisa ter escopo/permissão apropriada para esse projeto (adicione a conta/organização como owner/maintainer no PyPI, se necessário).
- Para testes, você pode usar o Test PyPI e um secret separado apontando para `https://test.pypi.org/legacy/` (ajustes no workflow necessários).
- Se preferir, podemos estender o workflow para publicar apenas em eventos `release` ou adicionar uma etapa de testes antes do build.

## Contribuição

Contribuições são bem-vindas. Para contribuir:

1. Abra uma issue descrevendo o problema ou a feature desejada.
2. Faça um fork do repositório e crie uma branch com um nome descritivo.
3. Abra um PR apontando para a branch `main` do repositório original.

Sugestões de conteúdo do PR:

- Testes (quando aplicável)
- Documentação atualizada
- Descrição clara das mudanças e impacto

## 📜 Licença
