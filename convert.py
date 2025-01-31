import json
import xml.etree.ElementTree as ET


# Função para converter um dicionário plano em um dicionário aninhado
def convert_to_nested_dict(flat_dict):
  result = {}

  # Iterar sobre as chaves e valores do dicionário plano
  for key, value in flat_dict.items():
    # Verificar se a chave contém um ponto
    if isinstance(value, dict):
      # Chamar a função recursivamente
      value = convert_to_nested_dict(value)

    # Dividir a chave em partes
    keys = key.split('.')

    # Inicializar o dicionário atual
    data = result

    # Iterar sobre as partes da chave, exceto a última
    for currentKey in keys[:-1]:
      # Verificar se a chave contém um índice
      if '[' in currentKey:
        # Dividir a chave em nome e índice
        currentKey, index = currentKey.replace(']', '').split('[')
        index = int(index)

        # Verificar se a chave não está no dicionário
        if currentKey not in data:
          data[currentKey] = []

        # Verificar se a lista não tem elementos suficientes
        while len(data[currentKey]) <= index:
          # Adicionar um novo dicionário à lista
          data[currentKey].append({})

        # Atualizar o dicionário atual
        data = data[currentKey][index]
      else:
        # Verificar se a chave não está no dicionário
        if currentKey not in data:
          # Adicionar um novo dicionário à chave
          data[currentKey] = {}

        # Atualizar o dicionário atual
        data = data[currentKey]

    # Adicionar o valor à última chave
    data[keys[-1]] = value

  # Retornar o dicionário aninhado
  return result

# Função para remover valores vazios de um dicionário
def remove_empty_values(data):
  # Iterar sobre as chaves e valores do dicionário
  for key, value in data.items():

    # Verificar se o valor é uma lista
    if isinstance(value, list):
      # Iterar sobre os elementos da lista
      for index in reversed(range(len(value))):
        # pega o valor atual
        currentValue = value[index]

        # Verificar se o valor é um dicionário
        if isinstance(currentValue, dict):
          # Verificar se o dicionário está vazio
          if not currentValue:
            # Remover o dicionário da lista
            value.pop(index)
          else:
            # Chamar a função recursivamente
            remove_empty_values(currentValue)
    
    # Verificar se o valor é um dicionário
    elif isinstance(value, dict):
      # Verificar se o dicionário está vazio
      if not value:
        # Remover a chave do dicionário
        del value
      else:
        # Chamar a função recursivamente
        remove_empty_values(value)

  # Retornar o dicionário
  return data

# Função para criar um elemento XSD
def create_xsd_element(name, type_="xs:string", minOccurs="0", maxOccurs="1"):
  # Criar um elemento XSD
  return ET.Element("xs:element", name=name, type=type_, minOccurs=minOccurs, maxOccurs=maxOccurs)

# Função para criar um tipo complexo XSD
def create_xsd_complex_type(name, elements):
  # Criar um tipo complexo XSD
  complex_type = ET.Element("xs:complexType", name=name)

  # Adicionar um elemento de sequência ao tipo complexo
  sequence = ET.SubElement(complex_type, "xs:sequence")

  # Iterar sobre os elementos e adiciona cada um deles à sequência
  for element in elements:
    # Adicionar o elemento à sequência
    sequence.append(element)

  # Retornar o tipo complexo
  return complex_type

# Função para converter um JSON em um XSD
def json_to_xsd(json_data, root_name="root"):
  elements = []

  # Iterar sobre as chaves e valores do JSON
  for key, value in json_data.items():
    # Substituir hífens por underscores
    key = key.replace("-", "_")

    # Verificar se o valor é um dicionário
    if isinstance(value, dict):
      # Chamar a função recursivamente
      sub_elements = json_to_xsd(value, root_name=key)

      # Criar um tipo complexo
      complex_type = create_xsd_complex_type(key, sub_elements)

      # Adicionar um elemento com o tipo complexo
      elements.append(create_xsd_element(key, type_="xs:complexType", minOccurs="0", maxOccurs="1"))
      elements.append(complex_type)

    # Verificar se o valor é uma lista
    elif isinstance(value, list):
      # Verificar se a lista está vazia
      if len(value) > 0 and isinstance(value[0], dict):
        # Chamar a função recursivamente
        sub_elements = json_to_xsd(value[0], root_name=key)

        # Criar um tipo complexo
        complex_type = create_xsd_complex_type(key, sub_elements)

        # Adicionar um elemento com o tipo complexo
        elements.append(create_xsd_element(key, type_="xs:complexType", minOccurs="0", maxOccurs="unbounded"))
        elements.append(complex_type)
      else:
        # Adicionar um elemento com o tipo string
        elements.append(create_xsd_element(key, type_="xs:string", minOccurs="0", maxOccurs="unbounded"))
    else:
      # Adicionar um elemento
      elements.append(create_xsd_element(key))

  # Criar um tipo complexo para o elemento raiz
  return elements



# Função principal
if __name__ == "__main__":
  # Carregar o conteúdo do arquivo
  with open('example.txt', 'r') as file:
    json_content = file.read()

  # Converta o conteúdo JSON em um dicionário
  original = json.loads(json_content)

  # Converta o dicionário plano dentro de 'data' em um dicionário aninhado
  nested_dict = convert_to_nested_dict(original)

  # Remova valores vazios do dicionário aninhado
  nested_dict = remove_empty_values(nested_dict)

  # Converta o dicionário aninhado para uma string JSON
  json_content = json.dumps(nested_dict, indent=4, ensure_ascii=False)

  # Salve a string JSON em um arquivo
  with open('output.json', 'w') as file:
    file.write(json_content)

  print("O arquivo TXT foi convertido com sucesso para um arquivo JSON com estrutura aninhada.")

  # Cria o elemento root do XSD
  xsd_root = ET.Element("xs:schema", xmlns_xs="http://www.w3.org/2001/XMLSchema")

  # # Atualiza o 'data' do dicionário original com o dicionário aninhado
  # original['data'] = nested_dict

  # Converte o JSON aninhado em elementos XSD
  xsd_elements = json_to_xsd(nested_dict)

  # Adiciona os elementos XSD ao root
  for elem in xsd_elements:
    xsd_root.append(elem)

  # Cria a árvore XSD
  xsd_tree = ET.ElementTree(xsd_root)

  # Salva a árvore XSD em um arquivo
  xsd_tree.write("output.xsd")

  print("O esquema XSD foi gerado com sucesso e salvo em output.xsd.")
