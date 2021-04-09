

def create_token_lst(s):
    """create token list:
    """
    s = s.replace('(', ' ( ')
    s = s.replace(')', ' ) ')

    return s.split()


def replace_and(s):
    s = s.replace('E', 'and')
    return s

def replace_or(s):
    s = s.replace('OU', 'or')
    return s

def replace_expressao(s, disciplinas):
    expressao = replace_and(s)
    expressao = replace_or(expressao)
    tokens = create_token_lst(expressao)
    for t in tokens:
        if t != '(' and t != ')' and t != 'and' and t != 'or':
            if t in disciplinas:
                expressao = expressao.replace(t, 'True')
            else:
                expressao = expressao.replace(t, 'False')
    return expressao


def create_token_expressao(expressao_requisitos):
    """
        Separa os código dos componentes da expressão.
    """
    s = expressao_requisitos.replace('(', '')
    s = s.replace(')', '')
    s = s.replace('E', '')
    s = s.replace('OU', '')

    return s.split()
