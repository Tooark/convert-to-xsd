import json
import xml.dom.minidom
import xml.etree.ElementTree as ET
from lxml import etree
from lxml.etree import QName
import re
import argparse
import os


def convert_to_nested_dict(flat_dict):
  """Convert a 'flat' dictionary into a 'nested' dictionary.

  Supports dotted keys and indexes in square brackets (e.g., 'a.b[1].c').
  Creates dictionaries and lists as needed to represent the nested structure.

  Args:
    flat_dict (dict): flat dictionary with dotted keys.

  Returns:
    dict: nested dictionary.
  """

  # Inicializar o dicionário aninhado
  result = {}

  # Iterar sobre as chaves e valores do dicionário plano
  for key, value in flat_dict.items():
    # Verificar se a chave contém um ponto
    if isinstance(value, dict):
      # Chamar a função recursivamente
      value = convert_to_nested_dict(value)

    keys = key.split('.')
    data = result

    # Iterar sobre as partes da chave, exceto a última
    for currentKey in keys[:-1]:
      # Verificar se a chave contém um índice
      if '[' in currentKey:
        currentKey, index = currentKey.replace(']', '').split('[')
        index = int(index)

        # Verificar se a chave não está no dicionário
        if currentKey not in data:
          data[currentKey] = []

        # Verificar se a lista não tem elementos suficientes
        while len(data[currentKey]) <= index:
          data[currentKey].append({})

        data = data[currentKey][index]
      else:
        # Verificar se a chave não está no dicionário
        if currentKey not in data:
          data[currentKey] = {}

        data = data[currentKey]

    # Verificar se a última chave contém um índice
    if '[' in keys[-1]:
      currentKey, index = keys[-1].replace(']', '').split('[')

      # Verificar se a chave não está no dicionário
      if currentKey not in data:
        data[currentKey] = [value]
      else:
        data[currentKey].append(value)
    else:
      data[keys[-1]] = value

  # Retornar o dicionário aninhado
  return result


def remove_empty_values(data):
  """Recursively remove empty dictionaries and empty elements from lists.

  Traverses dictionaries and lists, removing empty dictionaries and elements
  that are empty dictionaries. Returns the same (mutable) object cleaned.

  Args:
    data (dict): dictionary to be cleaned.

  Returns:
    dict: cleaned dictionary.
  """

  # Iterar sobre as chaves e valores do dicionário
  for key, value in data.items():
    # Verificar se o valor é uma lista
    if isinstance(value, list):
      # Iterar sobre os elementos da lista
      for index in reversed(range(len(value))):
        currentValue = value[index]

        # Verificar se o valor é um dicionário
        if isinstance(currentValue, dict):
          # Verificar se o dicionário está vazio
          if not currentValue:
            value.pop(index)
          else:
            # Chamar a função recursivamente
            remove_empty_values(currentValue)

    # Verificar se o valor é um dicionário
    elif isinstance(value, dict):
      # Verificar se o dicionário está vazio
      if not value:
        del value
      else:
        # Chamar a função recursivamente
        remove_empty_values(value)

  return data


def generate_xsd_element(name, value, fileName, root='root'):
  """Generates an XSD element (`xs:element` or `xs:complexType`) for a name/value pair.

  - If `value` is a `dict`, creates a `complexType` with a `sequence` containing
    elements for each key.
  - If `value` is a `list` and the first item is a `dict`, constructs a
    `complexType` for the item; otherwise, defines `type` based on the type of the
    first item and applies `minOccurs=0 maxOccurs=unbounded`.
  - If `value` is a primitive, defines `type`, `minOccurs=0`, and `maxOccurs=1`.

  Args:
    name (str): name of the element or type.
    value: associated value (dict, list, or primitive).
    fileName (str): file used to write sanitization mappings.
    root (str): name of the root element (treated as a named complex type).

  Returns:
    lxml.etree.Element: generated XSD element.
  """

  # Verificar se o nome é igual ao nome da raiz
  if name == root:
    # Criar um tipo complexo com o nome da raiz
    xsd_root = etree.Element(QName("http://www.w3.org/2001/XMLSchema", 'complexType'), name=root)
    xsd_element = xsd_root
  else:
    # Criar um elemento XSD com o nome fornecido
    xsd_element = etree.Element(QName("http://www.w3.org/2001/XMLSchema", 'element'), name=name)

  # Verificar se o valor é um dicionário
  if isinstance(value, dict):
    # Verificar se o nome é igual ao nome da raiz
    if name == root:
      complex_type = xsd_root
    else:
      # Criar um tipo complexo e uma sequência
      complex_type = etree.SubElement(xsd_element, QName("http://www.w3.org/2001/XMLSchema", 'complexType'))

    # Adicionar a sequência ao tipo complexo
    sequence = etree.SubElement(complex_type, QName("http://www.w3.org/2001/XMLSchema", 'sequence'))

    # Iterar sobre as chaves e valores do dicionário
    for key, val in value.items():
      # Chamar a função recursivamente para cada chave e valor
      child_element = generate_xsd_element(sanitize_element_name(key, fileName), val, fileName, root)

      sequence.append(child_element)

  # Verificar se o valor é uma lista
  elif isinstance(value, list):
    # Verifica se a lista não está vazia
    if value:
      # Verifica se o primeiro item da lista é um dicionário
      if (isinstance(value[0], dict)):
        # Criar um tipo complexo e uma sequência
        complex_type = etree.SubElement(xsd_element, QName("http://www.w3.org/2001/XMLSchema", 'complexType'))
        sequence = etree.SubElement(complex_type, QName("http://www.w3.org/2001/XMLSchema", 'sequence'))

        # Iterar sobre as chaves e valores do dicionário
        for key, val in value[0].items():
          # Chamar a função recursivamente para cada chave e valor
          child_element = generate_xsd_element(sanitize_element_name(key, fileName), val, fileName, root)

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

  return xsd_element


def get_xsd_type(value):
  """Returns the appropriate XSD annotation for a Python value.

  Simple mappings are applied:
  - int -> xs:integer
  - float -> xs:decimal
  - bool -> xs:boolean
  - str -> xs:string
  - None/other -> xs:string

  Args:
    value: Python value to inspect.

  Returns:
    str: XSD type (e.g., 'xs:string').
  """

  # Verificar o tipo do valor e retornar a anotação XSD correspondente
  if isinstance(value, int):
    return 'xs:integer'
  elif isinstance(value, float):
    return 'xs:decimal'
  elif isinstance(value, bool):
    return 'xs:boolean'
  elif isinstance(value, str):
    return 'xs:string'
  elif value is None:
    return 'xs:string'
  else:
    return 'xs:string'


def sanitize_element_name(name, fileName='change_name.json'):
  """Sanitizes an XML element name and logs changes in JSON.

  Replaces invalid characters with '_' and ensures the name does not start
  with a digit (prefixing with '_'). If the name is changed, logs the
  mapping in `fileName` (JSON), creating/updating the entry.

  Args:
    name (str): original name.
    fileName (str): JSON file to record mappings (default: change_name.json).

  Returns:
    str: sanitized name.
  """

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
    change_name[name] = new_name
    json_content = json.dumps(change_name, indent=2, ensure_ascii=False, sort_keys=True)

    # Salve a string JSON em um arquivo
    with open(fileName, 'w') as file:
      file.write(json_content)

  return new_name


def replace_prefix_xsd(content):
  """Replaces `xs:` prefixes with `xsd:` in the content of an XSD.

  Some tools/consumers expect `xsd:` instead of `xs:`; this function
  applies simple keyword replacements.

  Args:
    content (str): XSD content.

  Returns:
    str: content with prefixes replaced.
  """

  # Substitui xs: por xsd:
  content = re.sub(r'\bxs:', 'xsd:', content)

  # Substitui :xs= por :xsd=
  content = re.sub(r'\b:xs=', ':xsd=', content)

  return content


def json_to_xsd(data, fileName, root='root'):
  """Builds an XSD tree from a nested JSON dictionary.

  Args:
    data (dict): nested JSON dictionary.
    fileName (str): file used to log changed names.
    root (str): name of the root element.

  Returns:
    lxml.etree.Element: `<schema>` element containing the XSD.
  """

  # Cria o elemento raiz do esquema XSD
  xsd_schema = etree.Element(QName("http://www.w3.org/2001/XMLSchema", 'schema'))

  # Gera o elemento XSD para o dicionário de dados
  root_element = generate_xsd_element(root, data, fileName, root)

  # Adiciona o elemento raiz ao esquema XSD
  xsd_schema.append(root_element)

  return xsd_schema


def json_to_xml(element_name, data, fileName):
  """Converts a nested dictionary into an XML element.

  Iterates over nested keys/values creating sub-elements. Lists are
  represented by multiple child elements with the same name.

  Args:
    element_name (str): name of the root element.
    data: dictionary, list, or primitive value to convert.
    fileName (str): file to log sanitized names.

  Returns:
    xml.etree.ElementTree.Element: generated XML element.
  """

  # Cria um elemento XML com o nome fornecido
  xml_element = ET.Element(sanitize_element_name(element_name, fileName))

  # Verifica se o dado é um dicionário
  if isinstance(data, dict):
    # Itera sobre as chaves e valores do dicionário
    for key, val in data.items():
      # Verifica se o valor é uma lista
      if (isinstance(val, list)):
        # Itera sobre os itens da lista
        for item in val:
          # Chama a função recursivamente para cada chave e valor
          child = json_to_xml(key, item, fileName)

          xml_element.append(child)
      else:
        # Chama a função recursivamente para cada chave e valor
        child = json_to_xml(key, val, fileName)

        xml_element.append(child)

  # É um valor simples
  else:
    # Define o texto do elemento como o valor
    xml_element.text = str(data) if data is not None else ''

  return xml_element


def convert(fileName, root='root', outputs=None, output_dir=None):
  """Converts a 'flat' JSON file into nested JSON, XML, and XSD.

  Steps:
  1. Creates a `*_change_name.json` mapping file for sanitized names.
  2. Reads the input JSON and converts it to a nested dictionary.
  3. Removes empty entries.
  4. Generates and saves selected outputs (`*.json`, `*.xml`, `*.xsd`, `*_SAP.xsd`).

  Args:
    fileName (str): path to the input JSON file (can have .txt extension).
    root (str): name of the root element to use for XML/XSD.
    outputs (dict|None): output flags with keys `json`, `xml`, `xsd`, `sap`.
      If None, generates all outputs.
    output_dir (str|None): destination directory for generated files.
      If None, files are generated next to the input file.
  """

  # Verificar se o parâmetro outputs é None e definir os valores padrão
  if outputs is None:
    outputs = {'json': True, 'xml': True, 'xsd': True, 'sap': True}

  # Definir o nome base de saída
  if output_dir:
    os.makedirs(output_dir, exist_ok=True)
    output = os.path.join(output_dir, os.path.splitext(os.path.basename(fileName))[0])
  else:
    output = os.path.splitext(fileName)[0]

  # Definir o nome do arquivo de alteração de nome
  changeFileName = output + '_change_name.json'

  # Cria o arquivo de alteração de nome
  with open(changeFileName, 'w') as file:
    file.write('{}')  # Inicializa com um JSON vazio

  # Sanitize root element name
  root = sanitize_element_name(root, changeFileName)

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

  # Salvar JSON somente quando solicitado
  if outputs.get('json'):
    with open(output + '.json', 'w') as file:
      file.write(json_content)

    print('O ' + fileName + ' foi convertido com sucesso para ' + output + '.json')

  # Gerar XSD/SAP somente quando solicitado
  if outputs.get('xsd') or outputs.get('sap'):
    xsd_tree = json_to_xsd(json.loads(json_content), changeFileName, root)
    xsd_str = etree.tostring(xsd_tree, pretty_print=True, encoding='utf-8', xml_declaration=True).decode('utf-8')

    if outputs.get('xsd'):
      with open(output + '.xsd', 'w', encoding='utf-8') as f:
        f.write(xsd_str)

      print('O ' + fileName + ' foi convertido com sucesso para ' + output + '.xsd')

    if outputs.get('sap'):
      # Substituir xs: por xsd:
      xsd_str_sap = replace_prefix_xsd(xsd_str)

      # Salvar o XSD em um arquivo com substituição de prefixo para o SAP
      with open(output + '_SAP.xsd', 'w', encoding='utf-8') as f:
        f.write(xsd_str_sap)

      print('O ' + fileName + ' foi convertido com sucesso para ' + output + '_SAP.xsd')

  # Gerar XML somente quando solicitado
  if outputs.get('xml'):
    xml_root = json_to_xml(root, json.loads(json_content), changeFileName)

    xml_str = ET.tostring(xml_root, encoding='utf-8', xml_declaration=True)
    xml_pretty_str = xml.dom.minidom.parseString(xml_str).toprettyxml(indent="  ")

    with open(output + '.xml', 'w', encoding='utf-8') as f:
      f.write(xml_pretty_str)

    print('O ' + fileName + ' foi convertido com sucesso para ' + output + '.xml')

  print('O ' + fileName + ' gerou um arquivo indicando as chaves alteradas ' + changeFileName)


def validate_xml_xsd(file, output_dir=None):
  """Validates the generated XML against the corresponding XSD.

  Loads `<name>.xsd` and `<name>.xml` and performs validation, printing
  the result and error details if any.

  Args:
    file (str): path to the file (with extension) to validate (e.g., 'foo.txt' or 'files/foo.txt').
    output_dir (str|None): destination directory where .xml/.xsd were generated.
  """

  # Obter o nome do arquivo sem a extensão
  if output_dir:
    fileName = os.path.join(output_dir, os.path.splitext(os.path.basename(file))[0])
  else:
    fileName = os.path.splitext(file)[0]

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
    # Verificar se há apenas um erro e se é o erro de declaração do elemento raiz
    if len(xmlschema.error_log) == 1 and xmlschema.error_log[0].line == 2:
      print('O arquivo ' + xml_file + ' foi validado com sucesso contra o arquivo ' + xsd_file)
    else:
      print('O arquivo ' + xml_file + ' não foi validado com sucesso contra o arquivo ' + xsd_file + '. Erros encontrados:')

    # Exibir os erros
    for error in xmlschema.error_log:
      # Ignorar o erro de declaração do elemento raiz
      if error.line != 2:
        print("ERROR ON LINE %s: %s" % (error.line, error.message.encode("utf-8")))
        print()


def main(argv=None):  # Main function
  """Entry point for the CLI.

  Supports running for a single file (passed as an argument), all files in a directory,
  or for processing all files in the `files/` folder when executed without parameters 
  """

  epilog = (
    "Exemplos:\n"
    "  python convert.py\n"
    "  python convert.py files/\n"
    "  python convert.py dados/input.json\n"
    "  python convert.py dir1/ dir2/ arquivo.txt\n"
  )

  parser = argparse.ArgumentParser(
    description='Converte JSON/flat para XML/XSD. Forneça caminhos (arquivos ou diretórios).',
    epilog=epilog,
    formatter_class=argparse.RawDescriptionHelpFormatter)

  parser.add_argument(
    'paths',
    nargs='*',
    help='Caminhos opcionais (arquivos ou diretórios).')

  parser.add_argument(
    '--root',
    '-r',
    help='Nome do elemento raiz a usar (substitui o nome padrão que é o basename do arquivo)')

  parser.add_argument(
    '--json',
    '-j',
    action='store_true',
    dest='out_json',
    help='Salvar saída .json')

  parser.add_argument(
    '--xml',
    '-x',
    action='store_true',
    dest='out_xml',
    help='Salvar saída .xml')

  parser.add_argument(
    '--xsd',
    '-d',
    action='store_true',
    dest='out_xsd',
    help='Salvar saída .xsd')

  parser.add_argument(
    '--sap',
    '-s',
    action='store_true',
    dest='out_sap',
    help='Salvar saída _SAP.xsd')

  parser.add_argument(
    '--output',
    '-o',
    help='Diretório de saída dos arquivos gerados. Se não existir, será criado.')

  args = parser.parse_args(argv)

  any_output_flag = args.out_json or args.out_xml or args.out_xsd or args.out_sap
  outputs = {
    'json': args.out_json if any_output_flag else True,
    'xml': args.out_xml if any_output_flag else True,
    'xsd': args.out_xsd if any_output_flag else True,
    'sap': args.out_sap if any_output_flag else True,
  }

  if args.output:
    os.makedirs(args.output, exist_ok=True)

  # Se nenhum caminho informado, exibe a ajuda e sai
  if not args.paths:
    parser.print_help()
    return

  # Se foram informados caminhos, processa cada um (arquivo ou diretório)
  for path in args.paths:
    if os.path.isdir(path):
      entries = [e for e in os.listdir(path)
                 if os.path.isfile(os.path.join(path, e))
                 and not e.startswith('.')
                 and os.path.splitext(e)[1].lower() in ('.json', '.txt')]

      if not entries:
        print('Nenhum arquivo .json ou .txt encontrado em ' + path)
        continue

      for entry in entries:
        file_path = os.path.join(path, entry)
        root_name = args.root if args.root else os.path.splitext(entry)[0]

        convert(file_path, root_name, outputs, args.output)
        if outputs.get('xml') and outputs.get('xsd'):
          validate_xml_xsd(file_path, args.output)
        print()

    else:
      # arquivo único
      if not os.path.isfile(path):
        print('Arquivo não encontrado: ' + path)
        continue

      ext = os.path.splitext(path)[1].lower()
      
      if ext not in ('.json', '.txt'):
        print('Ignorando arquivo com extensão não suportada: ' + path)
        continue

      root_name = args.root if args.root else os.path.splitext(os.path.basename(path))[0]
      convert(path, root_name, outputs, args.output)

      if outputs.get('xml') and outputs.get('xsd'):
        validate_xml_xsd(path, args.output)
      
      print()


if __name__ == '__main__':
  main()
