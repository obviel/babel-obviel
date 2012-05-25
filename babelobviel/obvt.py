from lxml import html

TEXT_TOKEN = 0
NAME_TOKEN = 1

def extractor(fileobj, keywords, comment_tags, options):
    """Extract messages from Obviel Template (.obvt) source code.

    :param fileobj: the seekable, file-like object the messages should be
                    extracted from
    :param keywords: a list of keywords (i.e. function names) that should be
                     recognized as translation functions
    :param comment_tags: a list of translator tags to search for and include
                         in the results
    :param options: a dictionary of additional options (optional)
    :return: an iterator over ``(lineno, funcname, message, comments)`` tuples
    :rtype: ``iterator``
    """
    tree = html.parse(fileobj)
    for el in tree.xpath('//*[@data-trans]'):
        for message_id in trans_message_ids(el):
            yield (el.sourceline, None, message_id, [])
    for el in tree.xpath('//*[@data-tvar]'):
        message_id  = tvar_message_id(el)
        if message_id is not None:
            yield (el.sourceline, None, message_id, [])
            
class TransInfo(object):
    def __init__(self, content_id, message_id):
        self.content_id = content_id
        self.message_id = message_id

class ExtractionError(Exception):
    def __init__(self, el, message):
        self.el = el
        self.message = message
        
def parse_trans(el, text):
    text = text.strip()
    if text == '':
        return [TransInfo('.', None)]

    result = []
    parts = text.split()
    for part in parts:
        sub_parts = part.split(':')
        if len(sub_parts) == 1:
            result.append(TransInfo(sub_parts[0], None))
            continue
        elif len(sub_parts) > 2 or len(sub_parts) == 0:
            raise ExtractionError(el, "illegal data-trans")
        result.append(TransInfo(sub_parts[0], sub_parts[1]))
    return result

def trans_message_ids(el):
    trans = el.get('data-trans')

    for transinfo in parse_trans(el, trans):
        if transinfo.message_id is not None:
            yield transinfo.message_id
        elif transinfo.content_id == '.':
            yield text_message_id(el)
        else:
            yield el.get(transinfo.content_id)

def parse_tvar(el, tvar):
    tvar = tvar.strip()
    parts = tvar.split(':')
    if len(parts) == 1:
        return parts[0], None
    if len(parts) > 2 or len(parts) == 0:
        raise ExtractionError(el, "illegal data-tvar")
    return parts[0], parts[1]

def parse_variable(el, variable):
    view = variable.strip()
    parts = variable.split('|')
    if len(parts) == 1:
        return parts[0], None
    if len(parts) > 2 or len(parts) == 0:
        raise ExtractionError(el, "illegal variable")
    return parts[0], parts[1]

def parse_view(el, view):
    view = view.strip()
    parts = view.split('|')
    if len(parts) == 1:
        return parts[0], None
    if len(parts) > 2 or len(parts) == 0:
        raise ExtractionError(el, "illegal data-view")
    return parts[0], parts[1]
    
def tvar_message_id(el):
    # don't want to extract tvar if there's no actual content to translate
    # (no text, or single variable by itself)
    message_id = text_message_id(el)
    tokens = tokenize(message_id)
    if len(tokens) == 0:
        return None
    if len(tokens) == 1 and tokens[0]['type'] == NAME_TOKEN:
        return None

    # now extract tvar
    tvar = el.get('data-tvar')
    tvar, tvar_message_id = parse_tvar(el, tvar)
    if tvar_message_id is not None:
        return tvar_message_id
    return message_id

def clean_text(el, text):
    result = []
    for token in tokenize(text):
        if token['type'] == NAME_TOKEN:
            name, formatter = parse_variable(el, token['value'])
            result.append('{%s}' % name)
        else:
            result.append(token['value'])
    return ''.join(result)

def text_message_id(el):
    parts = []
    if el.text is not None:
        parts.append(el.text)
    for sub_el in el:
        tvar = get_tvar(sub_el)
        parts.append('{' + tvar + '}')
        if sub_el.tail is not None:
            parts.append(sub_el.tail)
    return ''.join(parts)

def get_tvar(el):
    tvar = el.get('data-tvar')
    if tvar is None:
        view = el.get('data-view')
        if view is not None:
            return view
        tokens = tokenize(text_message_id(el))
        if len(tokens) == 1 and tokens[0]['type'] == NAME_TOKEN:
            return tokens[0]['value']
    tvar, tvar_message_id = parse_tvar(el, tvar)
    return tvar

def tokenize(text):
    if text == '':
        return []
    result = []
    index = 0
    last_index = 0
    text_token = ''
    while True:
        open_index = text.find('{', index)
        if open_index == -1:
            text_token = text[last_index:]
            if text_token != '':
                result.append(dict(type=TEXT_TOKEN, value=text_token))
            break
        next_char = text[open_index + 1]
        if next_char in ['', ' ', '\t', '\n']:
            index = open_index + 1
            continue
        index = open_index + 1
        close_index = text.find('}', index)
        if close_index == -1:
            text_token = text[last_index:]
            if text_token != '':
                result.append(dict(type=TEXT_TOKEN, value=text_token))
            break
        text_token = text[last_index:open_index]
        if text_token != '':
            result.append(dict(type=TEXT_TOKEN, value=text_token))
        name_token = text[index:close_index]
        stripped_name_token = name_token.strip()
        if stripped_name_token == '':
            result.append(dict(type=TEXT_TOKEN,
                               value='{' + name_token + '}'))
        else:
            result.append(dict(type=NAME_TOKEN,
                               value=stripped_name_token))
        index = close_index + 1
        last_index = index
    return result

