#See the docs at:
#https://ply.readthedocs.io/_/downloads/en/latest/pdf/

import ply.lex as lex
import re

class DotLexer(object):
    states = (
      ('htmlstring','exclusive'),
      ('htmlstyle','exclusive'),
    )

    reserved = {
                'arrowhead'   : 'ARROWHEAD',
                'arrowsize'   : 'ARROWSIZE',
                'center'      : 'CENTER',
                'color'       : 'COLOR',
                'digraph'     : 'DIGRAPH',
                'edge'        : 'EDGESTYLE',
                'fillcolor'   : 'FILLCOLOR',
                'fontname'    : 'FONTNAME',
                'height'      : 'HEIGHT',
                'label'       : 'LABEL',
                'labelloc'    : 'LABELLOC',
                'node'        : 'NODESTYLE',
                'rankdir'     : 'RANKDIR',
                'size'        : 'SIZE',
                'shape'       : 'SHAPE',
                'style'       : 'STYLE',
                'peripheries' : 'PERIPHERIES',
                'tooltip'     : 'TOOLTIP',
                'width'       : 'WIDTH',
               }
    
    literals = ['(',')','=',',','{','}']
        
    tokens = [ 
                'CONNECTOR',
                'EOL',
                'HTML_START',
                'HTML_END',
                'ID',
                'NUMBER',
                'STRING',
                'LBRACKET',
                'RBRACKET',
              ]  + list(reserved.values())
    
    t_CONNECTOR = r'->'
    t_NUMBER    = r'(\.|[0-9])[0-9]*'
    
    #A string containing ignored characters (spaces and tabs)
    t_ANY_ignore  = ' \t\r,'
    
    def __init__(self):
        # Build the lexer
        self.lexer = lex.lex(module=self,debug=0,reflags=re.UNICODE | re.VERBOSE)
        self.htmlLevel = 0

    def t_EOL(self,t):
        r'(;\n|\n|;)'
        t.value = t.value
        return t
        
    def t_INITIAL_htmlstyle_ID(self,t):
        r'[a-zA-Z_!&|\u0080-\u3000/][a-zA-Z_!&|0-9\.\u0080-\u3000/]*'
        t.type = self.reserved.get(t.value,'ID')    # Check for reserved words
        return t
        
    def t_ANY_HTML_START(self,t):
        r'<'
        t.value = t.value
        self.htmlLevel += 1
        if self.htmlLevel == 1:
            t.lexer.begin('htmlstring')
        else:
            t.lexer.begin('htmlstyle')
        # print(t.lexer.lexdata)
        # print(t.lexer.lexdata[t.lexer.lexpos:])
        # lineRem = re.search('[^;\n]*[;\n|\n|;]',t.lexer.lexdata[t.lexer.lexpos:]).group()
        # candidate = '/' + (re.search('<([^>]*)>',t.lexer.lexmatch.group()).group(1))
        # print(f'lineRem: {lineRem}, {type(lineRem)}')
        # print(f'candidate: {candidate}, {type(candidate)}')
        # check = re.search(candidate,lineRem)
        # print(f'Is {candidate} in {lineRem}: {check}')
        return t

    def t_htmlstring_htmlstyle_HTML_END(self,t):
        r'>'
        t.value = t.value
        self.htmlLevel -= 1
        if self.htmlLevel >= 1:
            t.lexer.begin('htmlstring')
        else:
            t.lexer.begin('INITIAL')
        return t
        
    def t_htmlstring_STRING(self,t):
        r'[^><]+'
        t.value = t.value
        return t

    def t_LBRACKET(self,t):
        r'\['
        t.value = t.value
        return t

    def t_RBRACKET(self,t):
        r'\]'
        t.value = t.value
        return t
        
    def t_INITIAL_htmlstyle_STRING(self,t):
        r'(\"[^\"]*\")|(\'[^\']*\')|(\[[^\]]*\])'
        t.value = t.value
        return t
        
    # # Error handling rule
    def t_ANY_error(self,t):
        print("Illegal character '%s'" % t.value[0])
        print(t.value[0].encode('raw_unicode_escape'))
        t.lexer.skip(1)

    # Build the lexer
    def build(self,**kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    # Test it output
    def test(self,data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
             
#            print(tok)

            pattern = '.*\(([^,]*),.*'

            matches = re.finditer(pattern, f'{tok}')
            for match in matches:
#                print(f'{match.group(1)}')     
                print(f'{tok}, {match.group(1)}')     
                    
        if self.htmlLevel != 0:
            print(f'Error in HTML start/end tags: {"Missing End Tag" if self.htmlLevel > 0 else "Too many End Tags"}')
