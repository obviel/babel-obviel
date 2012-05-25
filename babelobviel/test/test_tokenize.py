from babelobviel.obvt import tokenize, NAME_TOKEN, TEXT_TOKEN

def test_tokenize_single_variable():
    assert tokenize("{foo}") == [{'type': NAME_TOKEN,
                                  'value': 'foo'}]
    
def test_tokenize_variable_in_text():
    assert tokenize('the {foo} is great') == [
        {'type': TEXT_TOKEN,
         'value': 'the '},
        {'type': NAME_TOKEN,
         'value': 'foo'},
        {'type': TEXT_TOKEN,
         'value': ' is great'}]
    
def test_variable_starts_text():
    assert tokenize('{foo} is great') == [
        {'type': NAME_TOKEN,
         'value': 'foo'},
        {'type': TEXT_TOKEN,
         'value': ' is great'}]

def test_variable_ends_text():
    assert tokenize('great is {foo}') == [
        {'type': TEXT_TOKEN,
         'value': 'great is '},
        {'type': NAME_TOKEN,
         'value': 'foo'}]

def test_two_variables_follow():
    assert tokenize('{foo}{bar}') == [
        {'type': NAME_TOKEN,
         'value': 'foo'},
        {'type': NAME_TOKEN,
         'value': 'bar'}
        ]

def test_two_variables_with_text():
    assert tokenize('a{foo}b{bar}c') == [
        {'type': TEXT_TOKEN,
         'value': 'a'},
        {'type': NAME_TOKEN,
         'value': 'foo'},
        {'type': TEXT_TOKEN,
         'value': 'b'},
        {'type': NAME_TOKEN,
         'value': 'bar'},
        {'type': TEXT_TOKEN,
         'value': 'c'}
        ]

def test_no_variables():
    assert tokenize('Hello world!') == [
        {'type': TEXT_TOKEN,
         'value': 'Hello world!'}]
    
def test_open_but_no_close():
    assert tokenize('{foo') == [
        {'type': TEXT_TOKEN,
         'value': '{foo'}]

def test_open_but_no_close_after_text():
    assert tokenize('after {foo') == [
        {'type': TEXT_TOKEN,
         'value': 'after {foo'}]

def test_open_but_no_close_after_variable():
    assert tokenize('{bar} after {foo') == [
        {'type': NAME_TOKEN,
         'value': 'bar'},
        {'type': TEXT_TOKEN,
         'value': ' after {foo'}]

def test_just_close():
    assert tokenize('foo } bar') == [
        {'type': TEXT_TOKEN,
         'value': 'foo } bar'}      
        ]

def test_empty_variable():
    assert tokenize('{}') == [
        {'type': TEXT_TOKEN,
         'value': '{}'}
        ]

def test_whitespace_variable():
    assert tokenize('{ }') == [
        {'type': TEXT_TOKEN,
         'value': '{ }'}
        ]
    
def test_non_stripped_variable():
    assert tokenize('{foo }') == [
        {'type': NAME_TOKEN,
         'value': 'foo'}
        ]

def test_whitespace_after_open():
    assert tokenize('{ foo}') == [
        {'type': TEXT_TOKEN,
         'value': '{ foo}'}
        ]

def test_whitespace_after_open_with_variable():
    assert tokenize('{ foo}{bar}') == [
        {'type': TEXT_TOKEN,
         'value': '{ foo}'},
        {'type': NAME_TOKEN,
         'value': 'bar'}]


        
