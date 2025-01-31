# Conversor de JSON Plano para JSON Aninhado e XSD

Este projeto contém um script Python que converte um arquivo JSON plano em um JSON com estrutura aninhada e, em seguida, gera um esquema XSD a partir do JSON aninhado.

## Estrutura do Projeto

- `example.txt`: Arquivo de entrada contendo o JSON plano.
- `convert.py`: Script Python que realiza a conversão.
- `output.json`: Arquivo de saída contendo o JSON aninhado.
- `output.xsd`: Arquivo de saída contendo o esquema XSD gerado.

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

### Função `create_xsd_element`

Esta função cria um elemento XSD.

- **Parâmetros**:
  - `name` (str): Nome do elemento.
  - `type_` (str): Tipo do elemento (padrão: "xs:string").
  - `minOccurs` (str): Número mínimo de ocorrências (padrão: "0").
  - `maxOccurs` (str): Número máximo de ocorrências (padrão: "1").
- **Retorno**:
  - `element` (Element): Elemento XSD criado.

### Função `create_xsd_complex_type`

Esta função cria um tipo complexo XSD.

- **Parâmetros**:
  - `name` (str): Nome do tipo complexo.
  - `elements` (list): Lista de elementos a serem incluídos no tipo complexo.
- **Retorno**:
  - `complex_type` (Element): Tipo complexo XSD criado.

### Função `json_to_xsd`

Esta função converte um JSON em um esquema XSD.

- **Parâmetros**:
  - `json_data` (dict): Dicionário JSON a ser convertido.
  - `root_name` (str): Nome do elemento raiz (padrão: "root").
- **Retorno**:
  - `elements` (list): Lista de elementos XSD gerados.

### Função Principal

A função principal do script realiza as seguintes etapas:

1. Carrega o conteúdo do arquivo `example.txt`.
2. Converte o conteúdo JSON em um dicionário.
3. Converte o dicionário plano em um dicionário aninhado.
4. Remove valores vazios do dicionário aninhado.
5. Salva o JSON aninhado em `output.json`.
6. Cria o elemento raiz do XSD.
7. Converte o JSON aninhado em elementos XSD.
8. Adiciona os elementos XSD ao elemento raiz.
9. Salva o esquema XSD em `output.xsd`.

## Como Executar

1. Coloque o arquivo `example.txt` na mesma pasta que o script `convert.py`.
2. Execute o script `convert.py`:

   ```sh
   python convert.py
   ```

3. Verifique os arquivos `output.json` e `output.xsd` gerados na mesma pasta.

## Exemplo

### Arquivo de Entrada (`example.txt`)

```json
{
  "serviceContextId": "123a654b-a1b2-c3d4-e5f6-12345f65f98e",
  "data": {
    "Application.Id": "ABCD001122334455",
    "Application.Decision.Name": "TesteNome",
    "Application.Order": "08",
    "Application.Client.DataClient[1].Concentrate.RegistrationData.Name": "AAAAAA",
    "Application.Client.DataClient[1].Concentrate.Score.Value": "BBBBBB",
    "Application.Client.DataClient[1].Concentrate.Score.Model": "CCCCCC",
    "Application.Client.DataClient[2].Concentrate.RegistrationData.Name": "EEEEEE",
    "Application.Client.DataClient[2].Concentrate.Score.Value": "FFFFFF",
    "Application.Client.DataClient[2].Concentrate.Score.Model": "GGGGGG",
    "Error.Message[1].IdMessage": "IIIIII"
  }
}
```

### Arquivo de Saída (`output.json`)

```json
{
  "serviceContextId": "123a654b-a1b2-c3d4-e5f6-12345f65f98e",
  "data": {
    "Application": {
      "Id": "ABCD001122334455",
      "Decision": {
        "Name": "TesteNome"
      },
      "Order": "08",
      "Client": {
        "DataClient": [
          {
            "Concentrate": {
              "RegistrationData": {
                "Name": "AAAAAA"
              },
              "Score": {
                "Value": "BBBBBB",
                "Model": "CCCCCC"
              }
            }
          },
          {
            "Concentrate": {
              "RegistrationData": {
                "Name": "EEEEEE"
              },
              "Score": {
                "Value": "FFFFFF",
                "Model": "GGGGGG"
              }
            }
          }
        ]
      }
    },
    "Error": {
      "Message": [
        {
          "IdMessage": "IIIIII"
        }
      ]
    }
  }
}
```

### Arquivo de Saída (`output.xsd`)

```xml
<xs:schema xmlns_xs="http://www.w3.org/2001/XMLSchema">
  <xs:element name="serviceContextId" type="xs:string" minOccurs="0" maxOccurs="1" />
  <xs:element name="data" type="xs:complexType" minOccurs="0" maxOccurs="1" />
  <xs:complexType name="data">
    <xs:sequence>
      <xs:element name="Application" type="xs:complexType" minOccurs="0" maxOccurs="1" />
      <xs:complexType name="Application">
        <xs:sequence>
          <xs:element name="Id" type="xs:string" minOccurs="0" maxOccurs="1" />
          <xs:element name="Decision" type="xs:complexType" minOccurs="0" maxOccurs="1" />
          <xs:complexType name="Decision">
            <xs:sequence>
              <xs:element name="Name" type="xs:string" minOccurs="0" maxOccurs="1" />
            </xs:sequence>
          </xs:complexType>
          <xs:element name="Order" type="xs:string" minOccurs="0" maxOccurs="1" />
          <xs:element name="Client" type="xs:complexType" minOccurs="0" maxOccurs="1" />
          <xs:complexType name="Client">
            <xs:sequence>
              <xs:element name="DataClient" type="xs:complexType" minOccurs="0"
                maxOccurs="unbounded" />
              <xs:complexType name="DataClient">
                <xs:sequence>
                  <xs:element name="Concentrate" type="xs:complexType" minOccurs="0" maxOccurs="1" />
                  <xs:complexType name="Concentrate">
                    <xs:sequence>
                      <xs:element name="RegistrationData" type="xs:complexType" minOccurs="0"
                        maxOccurs="1" />
                      <xs:complexType name="RegistrationData">
                        <xs:sequence>
                          <xs:element name="Name" type="xs:string" minOccurs="0" maxOccurs="1" />
                        </xs:sequence>
                      </xs:complexType>
                      <xs:element name="Score" type="xs:complexType" minOccurs="0" maxOccurs="1" />
                      <xs:complexType name="Score">
                        <xs:sequence>
                          <xs:element name="Value" type="xs:string" minOccurs="0" maxOccurs="1" />
                          <xs:element name="Model" type="xs:string" minOccurs="0" maxOccurs="1" />
                        </xs:sequence>
                      </xs:complexType>
                    </xs:sequence>
                  </xs:complexType>
                </xs:sequence>
              </xs:complexType>
            </xs:sequence>
          </xs:complexType>
        </xs:sequence>
      </xs:complexType>
      <xs:element name="Error" type="xs:complexType" minOccurs="0" maxOccurs="1" />
      <xs:complexType name="Error">
        <xs:sequence>
          <xs:element name="Message" type="xs:complexType" minOccurs="0" maxOccurs="unbounded" />
          <xs:complexType name="Message">
            <xs:sequence>
              <xs:element name="IdMessage" type="xs:string" minOccurs="0" maxOccurs="1" />
            </xs:sequence>
          </xs:complexType>
        </xs:sequence>
      </xs:complexType>
    </xs:sequence>
  </xs:complexType>
</xs:schema>

```

## Requisitos

- Python 3.x
- Biblioteca `xml.etree.ElementTree` (inclusa na biblioteca padrão do Python)

## Autor

Este projeto foi desenvolvido por [Paulo Freitas](https://github.com/paulofreitas91).
