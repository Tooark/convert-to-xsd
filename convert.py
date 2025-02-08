import json
import xml.dom.minidom
import xml.etree.ElementTree as ET
from lxml import etree
from lxml.etree import QName
import re


# Função para converter um dicionário plano em um dicionário aninhado
def convert_to_nested_dict(flat_dict):
  # Inicializar o dicionário aninhado
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

        # Converter o índice para inteiro
        index = int(index)

        # Verificar se a chave não está no dicionário
        if currentKey not in data:
          # Adicionar uma nova lista
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

    # Verificar se a última chave contém um índice
    if '[' in keys[-1]:
      # Dividir a chave em nome e índice
      currentKey, index = keys[-1].replace(']', '').split('[')

      # Verificar se a chave não está no dicionário
      if currentKey not in data:
        # Adicionar uma nova lista
        data[currentKey] = [value]
      else:
        # Adicionar o valor à lista
        data[currentKey].append(value)
    else:
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

# Função para gerar um elemento XSD a partir de um dicionário
def generate_xsd_element(name, value, fileName):
  xsd_element = etree.Element(QName("http://www.w3.org/2001/XMLSchema", 'element'), name=name)

  # Verificar se o valor é um dicionário
  if isinstance(value, dict):
    # Criar um tipo complexo e uma sequência
    complex_type = etree.SubElement(xsd_element, QName("http://www.w3.org/2001/XMLSchema", 'complexType'))
    sequence = etree.SubElement(complex_type, QName("http://www.w3.org/2001/XMLSchema", 'sequence'))
    
    # Iterar sobre as chaves e valores do dicionário
    for key, val in value.items():
      # Chamar a função recursivamente para cada chave e valor
      child_element = generate_xsd_element(sanitize_element_name(key, fileName), val, fileName)

      # Adicionar o elemento à sequência
      sequence.append(child_element)

  # Verificar se o valor é uma lista
  elif isinstance(value, list):
    # Verifica se a lista não está vazia
    if value:
      # Verifica se o primeiro item da lista é um dicionário
      if(isinstance(value[0], dict)):
        # Criar um tipo complexo e uma sequência
        complex_type = etree.SubElement(xsd_element, QName("http://www.w3.org/2001/XMLSchema", 'complexType'))
        sequence = etree.SubElement(complex_type, QName("http://www.w3.org/2001/XMLSchema", 'sequence'))

        # Iterar sobre as chaves e valores do dicionário
        for key, val in value[0].items():
          # Chamar a função recursivamente para cada chave e valor
          child_element = generate_xsd_element(sanitize_element_name(key, fileName), val, fileName)

          # Adicionar o elemento à sequência
          sequence.append(child_element)

      else:
        # Define o tipo do elemento com base no tipo do primeiro item da lista
        xsd_element.set('type', get_xsd_type(value[0]))

      # Define minOccurs como 0 e maxOccurs como unbounded
      xsd_element.set('minOccurs', '0')
      xsd_element.set('maxOccurs', 'unbounded')

  # É um valor simples
  else:
    # Define o tipo do elemento com base no tipo do valor
    xsd_element.set('type', get_xsd_type(value))

    # Define minOccurs e maxOccurs para 0 e 1
    xsd_element.set('minOccurs', '0')
    xsd_element.set('maxOccurs', '1')

  # Retorna o elemento XSD
  return xsd_element

# Função para obter o tipo XSD com base no tipo do valor
def get_xsd_type(value):
  if isinstance(value, int):
    return 'xs:integer'
  elif isinstance(value, float):
    return 'xs:decimal'
  elif isinstance(value, bool):
    return 'xs:boolean'
  elif isinstance(value, str):
    return 'xs:string'
  elif value is None:
    return 'xs:string'  # Ou xs:nil
  else:
    return 'xs:string'

# Função para substituir caracteres inválidos em nomes de elementos XML
def sanitize_element_name(name, fileName='change_name.json'):
  # Substitui caracteres inválidos em nomes de elementos XML
  new_name = re.sub(r'[^a-zA-Z0-9_]', '_', name)

  # Verifica se o nome começa com um número
  if re.match(r'^\d', new_name):
    new_name = '_' + new_name

  # Verifica se o nome foi alterado
  if name != new_name:
    # Carregar o conteúdo do arquivo
    with open(fileName, 'r') as file:
      json_content = file.read()

    # Converta o conteúdo JSON em um dicionário
    change_name = json.loads(json_content)

    # Adicione o nome original e o novo nome ao dicionário
    change_name[name] = new_name

    # Converta o dicionário aninhado para uma string JSON
    json_content = json.dumps(change_name, indent=2, ensure_ascii=False, sort_keys=True)

    # Salve a string JSON em um arquivo
    with open(fileName, 'w') as file:
      file.write(json_content)

    # print('O nome do elemento foi alterado de ' + name + ' para ' + new_name)

  # Retorna o novo nome
  return new_name

# Função para substituir xs: por xsd:
def replace_prefix_xsd(content):
  return re.sub(r'\bxs:', 'xsd:', content)

# Função para construir o esquema XSD
def json_to_xsd(data, fileName):
  # Cria o elemento raiz do esquema XSD
  xsd_schema = etree.Element(QName("http://www.w3.org/2001/XMLSchema", 'schema'))

  # Gera o elemento XSD para o dicionário de dados
  root_element = generate_xsd_element('root', data, fileName)

  # Adiciona o elemento raiz ao esquema XSD
  xsd_schema.append(root_element)

  # Retorna o esquema XSD
  return xsd_schema

# Função para converter um dicionário em um elemento XML
def json_to_xml(element_name, data, fileName):
  # Cria um elemento XML com o nome fornecido
  xml_element = ET.Element(sanitize_element_name(element_name, fileName))

 # Verifica se o dado é um dicionário
  if isinstance(data, dict):
    # Itera sobre as chaves e valores do dicionário
    for key, val in data.items():
      # Verifica se o valor é uma lista
      if(isinstance(val, list)):
        # Itera sobre os itens da lista
        for item in val:
          # Chama a função recursivamente para cada chave e valor
          child = json_to_xml(key, item, fileName)
          # Adiciona o elemento filho ao elemento pai
          xml_element.append(child)
      else:
        # Chama a função recursivamente para cada chave e valor
        child = json_to_xml(key, val, fileName)
        
        # Adiciona o elemento filho ao elemento pai
        xml_element.append(child)

  # É um valor simples
  else:
    # Define o texto do elemento como o valor
    xml_element.text = str(data) if data is not None else ''

  # Retorna o elemento XML
  return xml_element

# Função para converter um arquivo JSON flat em um arquivo JSON aninhada, gerar um arquivo XSD e um arquivo XML
def convert(fileName):
  # Definir o nome do arquivo de saída
  output = fileName.split('.')[0]

  # Definir o nome do arquivo de alteração de nome
  changeFileName = 'change_name_' + output + '.json'

  # Cria o arquivo de alteração de nome
  with open(changeFileName, 'w') as file:
    file.write('{}')  # Inicializa com um JSON vazio

  # Carregar o conteúdo do arquivo
  with open(fileName, 'r') as file:
    json_content = file.read()

  # Converta o conteúdo JSON em um dicionário
  original = json.loads(json_content)

  # Converta o dicionário plano dentro de 'data' em um dicionário aninhado
  nested_dict = convert_to_nested_dict(original)

  # Remova valores vazios do dicionário aninhado
  nested_dict = remove_empty_values(nested_dict)

  # Converta o dicionário aninhado para uma string JSON
  json_content = json.dumps(nested_dict, indent=4, ensure_ascii=False, sort_keys=True)

  # Salve a string JSON em um arquivo
  with open(output + '.json', 'w') as file:
    file.write(json_content)

  print('O ' + fileName + ' foi convertido com sucesso para ' + output + '.json')

  # Gerar o XSD
  xsd_tree = json_to_xsd(json.loads(json_content), changeFileName)
  xsd_str = etree.tostring(xsd_tree, pretty_print=True,encoding='utf-8', xml_declaration=True).decode('utf-8')

  # Salvar o XSD em um arquivo
  with open(output + '.xsd', 'w', encoding='utf-8') as f:
    f.write(xsd_str)

  print('O ' + fileName + ' foi convertido com sucesso para ' + output + '.xsd')

  # Substituir xs: por xsd:
  xsd_str = replace_prefix_xsd(xsd_str)

  # Salvar o XSD em um arquivo com substituição de prefixo para o SAP
  with open(output + '_SAP.xsd', 'w', encoding='utf-8') as f:
    f.write(xsd_str)

  print('O ' + fileName + ' foi convertido com sucesso para ' + output + '_SAP.xsd')

  # Converter o JSON em XML
  xml_root = json_to_xml('root', json.loads(json_content), changeFileName)

   # Salvar o XML em um arquivo com indentação
  xml_str = ET.tostring(xml_root, encoding='utf-8', xml_declaration=True)
  xml_pretty_str = xml.dom.minidom.parseString(xml_str).toprettyxml(indent="  ")  
  
  # Salvar o XML em um arquivo
  # xml_tree.write(output + '.xml', encoding='utf-8', xml_declaration=True)
  with open(output + '.xml', 'w', encoding='utf-8') as f:
    f.write(xml_pretty_str)

  print('O ' + fileName + ' foi convertido com sucesso para ' + output + '.xml')

# Função para validar um arquivo XML contra um arquivo XSD
def validate_xml_xsd(file):
  # Obter o nome do arquivo sem a extensão
  fileName = file.split('.')[0]

  # Definir o nome dos arquivos XSD e XML
  xsd_file = fileName + '.xsd'
  xml_file = fileName + '.xml'

  # Validar o XML contra o XSD
  xmlschema_doc = etree.parse(xsd_file)
  xmlschema = etree.XMLSchema(xmlschema_doc)
  xml_doc = etree.parse(xml_file)

  # Verificar se o XML é válido
  if xmlschema.validate(xml_doc):
    print('O arquivo ' + xml_file + ' foi validado com sucesso contra o arquivo ' + xsd_file)
  else:
    print('O arquivo ' + xml_file + ' não foi validado com sucesso contra o arquivo ' + xsd_file + '. Erros encontrados:')

    # Exibir os erros
    for error in xmlschema.error_log:
      print("ERROR ON LINE %s: %s" % (error.line, error.message.encode("utf-8")))
      # print(error.message)
      print()


# Função principal
if __name__ == '__main__':
  # Lista de arquivos a serem convertidos
  listFiles = ['example.txt']

  # Iterar sobre os arquivos
  for file in listFiles:
    # Converter o arquivo
    convert(file)

    # Validar o arquivo XML contra o arquivo XSD
    validate_xml_xsd(file)

    print()
