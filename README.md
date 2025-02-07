# Conversor de JSON Plano para JSON Aninhado, XML e XSD

Este projeto contém um script Python que converte um arquivo JSON plano em um JSON com estrutura aninhada, gera um esquema XSD e um arquivo XML a partir do JSON aninhado.

## Estrutura do Projeto

- `example.txt`: Arquivo de entrada contendo o JSON plano.
- `convert.py`: Script Python que realiza a conversão.
- `requirements.txt`: Arquivo de configuração das dependências do projeto.
- `output.json`: Arquivo de saída contendo o JSON aninhado.
- `output.xsd`: Arquivo de saída contendo o esquema XSD gerado.
- `output.xml`: Arquivo de saída contendo o XML gerado.

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

### Função `generate_xsd_element`

Esta função gera um elemento XSD a partir de um dicionário.

- **Parâmetros**:
  - `name` (str): Nome do elemento.
  - `value` (any): Valor do elemento.
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
- **Retorno**:
  - `sanitized_name` (str): Nome do elemento sanitizado.

### Função `json_to_xsd`

Esta função converte um dicionário JSON em um esquema XSD.

- **Parâmetros**:
  - `data` (dict): Dicionário JSON a ser convertido.
- **Retorno**:
  - `xsd_schema` (Element): Esquema XSD gerado.

### Função `json_to_xml`

Esta função converte um dicionário JSON em um XML.

- **Parâmetros**:
  - `element_name` (str): Nome do elemento raiz.
  - `data` (dict): Dicionário JSON a ser convertido.
- **Retorno**:
  - `xml_element` (Element): Elemento XML gerado.

### Função `convert`

A função `convert` do script realiza as seguintes etapas:

1. Captura o nome do arquivo.
2. Carrega o conteúdo do arquivo JSON.
3. Converte o conteúdo JSON em um dicionário.
4. Converte o dicionário plano em um dicionário aninhado.
5. Remove valores vazios do dicionário aninhado.
6. Salva o JSON aninhado com o nome do arquivo original.
7. Gera o esquema XSD a partir do JSON aninhado.
8. Salva o esquema XSD com o nome do arquivo original.
9. Converte o JSON aninhado em XML.
10. Salva o XML com o nome do arquivo original.

### Função `validate_xml_xsd`

Esta função valida um arquivo XML contra um arquivo XSD.

- **Parâmetros**:
  - `file` (str): Nome do arquivo XML a ser validado.

## Como Executar

1. Coloque o arquivo `example.txt` na mesma pasta que o script `convert.py`.
2. Verifique se a lista de arquivos dentro da função principal está com o `example.txt`.
3. Instale as dependências listadas no `requirements.txt`:

   ```sh
   pip install -r requirements.txt
   ```

4. Execute o script `convert.py`:

   ```sh
   python convert.py
   ```

5. Verifique os arquivos `example.json`, `example.xsd` e `example.xml` gerados na mesma pasta.

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

### Arquivo de Saída (`example.json`)

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

### Arquivo de Saída (`example.xsd`)

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

### Arquivo de Saída (`example.xmd`)

```xml
<?xml version='1.0' encoding='utf-8'?>
<root>
  <serviceContextId>123a654b-a1b2-c3d4-e5f6-12345f65f98e</serviceContextId>
  <data>
    <K_Application>
      <Id>ABCD001122334455</Id>
      <Decision>
        <Name>TesteNome</Name>
      </Decision>
      <Order>08</Order>
      <Client>
        <DataClient>
          <DataClient_Item>
            <Concentrate>
              <RegistrationData>
                <Name>AAAAAA</Name>
              </RegistrationData>
              <Score>
                <Value>BBBBBB</Value>
                <Model>CCCCCC</Model>
              </Score>
            </Concentrate>
          </DataClient_Item>
          <DataClient_Item>
            <Concentrate>
              <RegistrationData>
                <Name>EEEEEE</Name>
              </RegistrationData>
              <Score>
                <Value>FFFFFF</Value>
                <Model>GGGGGG</Model>
              </Score>
            </Concentrate>
          </DataClient_Item>
        </DataClient>
      </Client>
    </K_Application>
    <Error>
      <Message>
        <Message_Item>
          <IdMessage>HHHHHH</IdMessage>
        </Message_Item>
      </Message>
    </Error>
    <Key>
      <A_set>
        <Value>
          <Value_Item>IIIIII</Value_Item>
          <Value_Item>JJJJJJ</Value_Item>
          <Value_Item>KKKKKK</Value_Item>
          <Value_Item>LLLLLL</Value_Item>
          <Value_Item>MMMMMM</Value_Item>
        </Value>
      </A_set>
    </Key>
  </data>
</root>
```

## Requisitos

- Python 3.x
- Biblioteca `lxml`

## Autor

Este projeto foi desenvolvido por [Paulo Freitas](https://github.com/paulofreitas91).
