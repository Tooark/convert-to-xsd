# Conversor de JSON Plano para JSON Aninhado, XML e XSD

Este projeto contém um script Python que converte um arquivo JSON plano em um JSON com estrutura aninhada, um arquivo XML, um esquema XSD e um esquema XSD para SAP a partir do JSON aninhado.

## Estrutura do Projeto

- `example.txt`: Arquivo de entrada contendo o JSON plano.
- `convert.py`: Script Python que realiza a conversão.
- `requirements.txt`: Arquivo de configuração das dependências do projeto.
- `example.json`: Arquivo de saída contendo o JSON aninhado.
- `example.xml`: Arquivo de saída contendo o XML gerado.
- `example.xsd`: Arquivo de saída contendo o esquema XSD gerado.
- `example_SAP.xsd`: Arquivo de saída contendo o esquema XSD com substituição de prefixo para `xsd:` gerado.
- `change_name_example.json`: Arquivo de mapeamento de chaves que foram alteradas.

## Funcionalidades

### Função `convert_to_nested_dict`

Esta função converte um dicionário plano em um dicionário aninhado.

- **Parâmetros**:
  - `flat_dict` (dict): Dicionário plano a ser convertido.
- **Retorno**:
  - `result` (dict): Dicionário aninhado.

### Função `remove_empty_values`

Esta função remove valores vazios de um dicionário.

- **Parâmetros**:
  - `data` (dict): Dicionário a ser limpo.
- **Retorno**:
  - `data` (dict): Dicionário limpo.

### Função `generate_xsd_element`

Esta função gera um elemento XSD a partir de um dicionário.

- **Parâmetros**:
  - `name` (str): Nome do elemento.
  - `value` (any): Valor do elemento.
  - `fileName` (str): Nome do arquivo com as chaves que foram alteradas.
- **Retorno**:
  - `xsd_element` (Element): Elemento XSD gerado.

### Função `get_xsd_type`

Esta função obtém o tipo XSD com base no tipo do valor.

- **Parâmetros**:
  - `value` (any): Valor para determinar o tipo XSD.
- **Retorno**:
  - `type` (str): Tipo XSD correspondente.

### Função `sanitize_element_name`

Esta função substitui caracteres inválidos em nomes de elementos XML.

- **Parâmetros**:
  - `name` (str): Nome do elemento.
  - `fileName` (str): Nome do arquivo com as chaves que foram alteradas. Parâmetro padrão é `change_name.json`.
- **Retorno**:
  - `new_name` (str): Nome do elemento sanitizado.

### Função `json_to_xsd`

Esta função converte um dicionário JSON em um esquema XSD.

- **Parâmetros**:
  - `data` (dict): Dicionário JSON a ser convertido.
  - `fileName` (str): Nome do arquivo com as chaves que foram alteradas.
- **Retorno**:
  - `xsd_schema` (Element): Esquema XSD gerado.

### Função `json_to_xml`

Esta função converte um dicionário JSON em um XML.

- **Parâmetros**:
  - `element_name` (str): Nome do elemento raiz.
  - `data` (dict): Dicionário JSON a ser convertido.
  - `fileName` (str): Nome do arquivo com as chaves que foram alteradas.
- **Retorno**:
  - `xml_element` (Element): Elemento XML gerado.

### Função `convert`

A função `convert` do script realiza as seguintes etapas:

1. Captura o nome do arquivo.
2. Carrega o conteúdo do arquivo JSON flat ou aninhado.
3. Converte o conteúdo JSON em um dicionário.
4. Converte o dicionário plano em um dicionário aninhado.
5. Remove valores vazios do dicionário aninhado.
6. Salva o JSON aninhado com o nome do arquivo original.
7. Gera o esquema XSD a partir do JSON aninhado.
8. Salva o esquema XSD com o nome do arquivo original.
9. Altera o prefixo de `xs:` para `xsd:`.
10. Salva o esquema XSD com o nome do arquivo original com adicional de `_SAP`.
11. Converte o JSON aninhado em XML.
12. Salva o XML com o nome do arquivo original.

- **Parâmetros**:
  - `fileName` (str): Nome do arquivo JSON flat ou aninhado.

### Função `validate_xml_xsd`

Esta função valida um arquivo XML contra um arquivo XSD.

1. Carrega o arquivo XML.
2. Carrega o arquivo XSD.
3. Valida o arquivo XML contra o arquivo XSD.

- **Parâmetros**:
  - `file` (str): Nome do arquivo XML e XSD a ser validado.

### Função Principal

Chama as funções `convert` e `validate_xml_xsd` passando um arquivo da lista de arquivos a serem validados.

## Como Executar

1. Coloque os arquivos que queira converter na mesma pasta que o script `convert.py`.
2. Adicione os nomes dos arquivos com as extensões na variável `listFiles` dentro da função principal.
3. Instale as dependências listadas no `requirements.txt`:

   ```sh
   pip install -r requirements.txt
   ```

4. Execute o script `convert.py`:

   ```sh
   python convert.py
   ```

5. Verifique os arquivos de saída `*.json`, `*.xml`, `*.xsd` e `*_SAP.xsd` gerados na mesma pasta.

## Exemplo

### Arquivo de Entrada (`example.txt`)

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
    "Key.A-set.Value[1]" : "IIIIII",
    "Key.A-set.Value[2]" : "JJJJJJ",
    "Key.A-set.Value[3]" : "KKKKKK",
    "Key.A-set.Value[4]" : "LLLLLL",
    "Key.A-set.Value[5]" : "MMMMMM"
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
                "Model": [
                  "CCCCCC",
                  "DDDDDD"
                ]
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
                "Model": [
                  "GGGGGG",
                  "HHHHHH"
                ]
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
        "Value": [
          "IIIIII",
          "JJJJJJ",
          "KKKKKK",
          "LLLLLL",
          "MMMMMM"
        ]
      }
    }
  },
  "serviceContextId": "123a654b-a1b2-c3d4-e5f6-12345f65f98e"
}
```

### Arquivo de Saída (`example.xml`)

```xml
<?xml version="1.0"?>
<root>
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
</root>
```

### Arquivo de Saída (`example.xsd`)

```xml
<?xml version='1.0' encoding='utf-8'?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:element name="root">
    <xs:complexType>
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
                          <xs:element name="IdMessage" type="xs:string" minOccurs="0" maxOccurs="1" />
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
                                            <xs:element name="Name" type="xs:string" minOccurs="0" maxOccurs="1" />
                                          </xs:sequence>
                                        </xs:complexType>
                                      </xs:element>
                                      <xs:element name="Score">
                                        <xs:complexType>
                                          <xs:sequence>
                                            <xs:element name="Value" type="xs:string" minOccurs="0" maxOccurs="1" />
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
                                            <xs:element name="Model" type="xs:string" minOccurs="0" maxOccurs="unbounded" />
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
                          <xs:element name="Name" type="xs:string" minOccurs="0" maxOccurs="1" />
                        </xs:sequence>
                      </xs:complexType>
                    </xs:element>
                    <xs:element name="Id" type="xs:string" minOccurs="0" maxOccurs="1" />
                    <xs:element name="Order" type="xs:string" minOccurs="0" maxOccurs="1" />
                  </xs:sequence>
                </xs:complexType>
              </xs:element>
              <xs:element name="Key">
                <xs:complexType>
                  <xs:sequence>
                    <xs:element name="A_set">
                      <xs:complexType>
                        <xs:sequence>
                          <xs:element name="Value" type="xs:string" minOccurs="0"
                            maxOccurs="unbounded" />
                        </xs:sequence>
                      </xs:complexType>
                    </xs:element>
                  </xs:sequence>
                </xs:complexType>
              </xs:element>
            </xs:sequence>
          </xs:complexType>
        </xs:element>
        <xs:element name="serviceContextId" type="xs:string" minOccurs="0" maxOccurs="1" />
      </xs:sequence>
    </xs:complexType>
  </xs:element>
</xs:schema>
```

### Arquivo de Saída (`example_SAP.xsd`)

```xml
<?xml version='1.0' encoding='utf-8'?>
<xsd:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xsd:element name="root">
    <xsd:complexType>
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
  </xsd:element>
</xsd:schema>
```

### Arquivo de Saída (`change_name_example.json`)

```json
{
  "A-set": "A_set",
  "K-Application": "K_Application"
}
```

## Requisitos

- Python 3.x
- Biblioteca `lxml`

## Autor

Este projeto foi desenvolvido por [Paulo Freitas](https://github.com/paulofreitas91).
