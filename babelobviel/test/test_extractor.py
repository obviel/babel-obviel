from babelobviel.obvt import extractor, html_extractor
import os

def datafile(name):
    return os.path.join(os.path.dirname(__file__), 'testdata', name)

def test_text():
    with open(datafile('test1.obvt')) as f:
        r = list(extractor(f, [], [], []))
        assert len(r) == 1
        lineno, funcname, message, comments = r[0]
        assert lineno == 1
        assert message == 'Hello world!'
        assert funcname is None

def test_text_explicit():
    with open(datafile('test2.obvt')) as f:
        r = list(extractor(f, [], [], []))
        assert len(r) == 1
        lineno, funcname, message, comments = r[0]
        assert lineno == 1
        assert message == 'Hello world!'

def test_text_message_id():
    with open(datafile('test3.obvt')) as f:
        r = list(extractor(f, [], [], []))
        assert len(r) == 1
        lineno, funcname, message, comments = r[0]
        assert lineno == 1
        assert message == 'message'

def test_text_message_id_explicit():
    with open(datafile('test4.obvt')) as f:
        r = list(extractor(f, [], [], []))
        assert len(r) == 1
        lineno, funcname, message, comments = r[0]
        assert lineno == 1
        assert message == 'message'

def test_attribute():
    with open(datafile('test5.obvt')) as f:
        r = list(extractor(f, [], [], []))
        assert len(r) == 1
        lineno, funcname, message, comments = r[0]
        assert lineno == 1
        assert message == 'Bye world'
    
def test_attribute_message_id():
    with open(datafile('test6.obvt')) as f:
        r = list(extractor(f, [], [], []))
        assert len(r) == 1
        lineno, funcname, message, comments = r[0]
        assert lineno == 1
        assert message == 'message'

def test_text_and_attribute():
    with open(datafile('test7.obvt')) as f:
        r = list(extractor(f, [], [], []))
        assert len(r) == 2
        r.sort()
        lineno, funcname, message, comments = r[0]
        assert lineno == 1
        assert message == 'Bye world'
        lineno, funcname, message, comments = r[1]
        assert message == 'Hello world!'

def test_text_variable():
    with open(datafile('test8.obvt')) as f:
        r = list(extractor(f, [], [], []))
        assert len(r) == 1
        lineno, funcname, message, comments = r[0]
        assert lineno == 1
        assert message == 'Hello {who}!'

def test_text_tvar():
    with open(datafile('test9.obvt')) as f:
        r = list(extractor(f, [], [], []))
        assert len(r) == 1
        lineno, funcname, message, comments = r[0]
        assert lineno == 1
        assert message == 'Hello {who}!'

def test_text_tvar_with_text():
    with open(datafile('test10.obvt')) as f:
        r = list(extractor(f, [], [], []))
        assert len(r) == 2
        r.sort()
        lineno, funcname, message, comments = r[0]
        assert lineno == 1
        assert message == 'Hello {who}!'
        lineno, funcname, message, comments = r[1]
        assert lineno == 1
        assert message == 'great {who}'

def test_text_tvar_message_id():
    with open(datafile('test11.obvt')) as f:
        r = list(extractor(f, [], [], []))
        assert len(r) == 2
        r.sort()
        lineno, funcname, message, comments = r[0]
        assert lineno == 1
        assert message == 'Hello {who}!'
        lineno, funcname, message, comments = r[1]
        assert lineno == 1
        assert message == 'who_message'

def test_implicit_tvar_due_to_variable():
    with open(datafile('test12.obvt')) as f:
        r = list(extractor(f, [], [], []))
        assert len(r) == 1
        lineno, funcname, message, comments = r[0]
        assert lineno == 1
        assert message == 'Hello {who}!'

def test_implicit_tvar_due_to_view():
    with open(datafile('test13.obvt')) as f:
        r = list(extractor(f, [], [], []))
        assert len(r) == 1
        lineno, funcname, message, comments = r[0]
        assert lineno == 1
        assert message == 'Hello {who}!'

def test_implicit_tvar_due_to_view_with_view_name():
    with open(datafile('test14.obvt')) as f:
        r = list(extractor(f, [], [], []))
        assert len(r) == 1
        lineno, funcname, message, comments = r[0]
        assert lineno == 1
        assert message == 'Hello {who}!'

def test_implicit_tvar_due_to_variable_with_formatter():
    with open(datafile('test15.obvt')) as f:
        r = list(extractor(f, [], [], []))
        assert len(r) == 1
        lineno, funcname, message, comments = r[0]
        assert lineno == 1
        assert message == 'Hello {who}!'

def test_variable_with_formatter():
    with open(datafile('test16.obvt')) as f:
        r = list(extractor(f, [], [], []))
        assert len(r) == 1
        lineno, funcname, message, comments = r[0]
        assert lineno == 1
        assert message == 'Hello {who}!'
    

def test_plural():
    with open(datafile('test17.obvt')) as f:
        r = list(extractor(f, [], [], []))
        assert len(r) == 1
        lineno, funcname, message, comments = r[0]
        assert lineno == 1
        assert message == ('{count} cow', '{count} cows')
        assert funcname == 'ngettext'
        
def test_plural_explicit():
    with open(datafile('test18.obvt')) as f:
        r = list(extractor(f, [], [], []))
        assert len(r) == 1
        lineno, funcname, message, comments = r[0]
        assert lineno == 1
        assert message == ('{count} cow', '{count} cows')

def test_plural_attribute():
    with open(datafile('test19.obvt')) as f:
        r = list(extractor(f, [], [], []))
        assert len(r) == 1
        lineno, funcname, message, comments = r[0]
        assert lineno == 1
        assert message == ('{count} cow', '{count} cows')

def test_plural_tvar():
    with open(datafile('test20.obvt')) as f:
        r = list(extractor(f, [], [], []))
        assert len(r) == 2
        lineno, funcname, message, comments = r[0]
        assert lineno == 1
        assert message == "I count {something}"
        lineno, funcname, message, comments = r[1]
        assert lineno == 1
        assert message == ('{count} cow', '{count} cows')

def test_html_extractor():
    with open(datafile('test1.html')) as f:
        r = list(html_extractor(f, [], [], []))
        assert len(r) == 1
        lineno, funcname, message, comments = r[0]
        assert lineno == 4
        assert message == 'Hello {who}!'

def test_html_extractor_multi_line():
    with open(datafile('test2.html')) as f:
        r = list(html_extractor(f, [], [], []))
        assert len(r) == 1
        lineno, funcname, message, comments = r[0]
        assert lineno == 5
        assert message == 'Hello {who}!'

def test_whitespace():
    with open(datafile('test21.obvt')) as f:
        r = list(extractor(f, [], [], []))
        assert len(r) == 1
        lineno, funcname, message, comments = r[0]
        assert message == "This has whitespace."
                 

def test_tvar_whitespace():
    with open(datafile('test22.obvt')) as f:
        r = list(extractor(f, [], [], []))
        assert len(r) == 2
        lineno, funcname, message, comments = r[0]
        assert message == "{something} is up."
        lineno, funcname, message, comments = r[1]
        assert message == "This has whitespace."

def test_internal_whitespace():
    with open(datafile('test23.obvt')) as f:
        r = list(extractor(f, [], [], []))
        assert len(r) == 1
        lineno, funcname, message, comments = r[0]
        assert message == "This has internal whitespace."

def test_attr_whitespace():
    with open(datafile('test24.obvt')) as f:
        r = list(extractor(f, [], [], []))
        assert len(r) == 1
        lineno, funcname, message, comments = r[0]
        assert message == " We do want this  whitespace.  "

