'''
SCRABBLE

Este módulo inclui as rotinas necessárias para implementar uma versão básica do jogo Scrabble, com funções para:  
- Criar tabuleiros e casas de jogo;
- Baralhar conjuntos de letras com base numa sequência pseudo-aleatória;
- Validar e processar jogadas;
- Apresentar os dados de jogo ao jogador de forma organizada;
- Permitir jogar contra bots de 3 dificuldades diferentes.

O programa suporta até 4 jogadores e regras simplificadas do Scrabble tradicional.
'''
# para as docstrings de funções de baixo nível, os tipos dos TADs foram representados pelo seu tipo interno.
# para as de funções de alto nível, foram representados pelo próprio TAD

ABECEDARIO = ('A','B','C','Ç','D','E','F','G','H','I','J','L','M','N','O','P','Q','R','S','T','U','V','X','Z')
TAMANHO_TABULEIRO = 15
COORDS_CASA_CENTRAL = (TAMANHO_TABULEIRO // 2 + 1,) * 2
NUMERO_LETRAS = 7
CASA_VAZIA = '.'
PONTOS = {
    "A": 1, "B": 3, "C": 2, "Ç": 3, "D": 2, "E": 1,
    "F": 4, "G": 4, "H": 4, "I": 1, "J": 5, "L": 2,
    "M": 1, "N": 3, "O": 1, "P": 2, "Q": 6, "R": 1,
    "S": 1, "T": 1, "U": 1, "V": 4, "X": 8, "Z": 8
}
SACO = {
    "A": 14, "F": 2,  "M": 6,  "S": 8,
    "B": 3,  "G": 2,  "N": 4,  "T": 5,
    "C": 4,  "H": 2,  "O": 10, "U": 7,
    "Ç": 2,  "I": 10, "P": 4,  "V": 2,
    "D": 5,  "J": 2,  "Q": 1,  "X": 1,
    "E": 11, "L": 5,  "R": 6,  "Z": 1
}

##### TAD: CASA
### FUNÇÕES DE BAIXO NÍVEL
# CONSTRUTOR
def cria_casa(linha: int, coluna: int):
    """Cria um TAD casa com os parâmetros dados.

    Args:
        linha (int): a linha da casa
        coluna (int): a coluna da casa

    Raises:
        ValueError: quando algum dos dois valores não é um inteiro dentro dos limites do tabuleiro

    Returns:
        tuple: TAD casa com os valores linha e coluna armazenados
    """    
    if type(linha) == int and type(coluna) == int and 1 <= linha <= TAMANHO_TABULEIRO and 1 <= coluna <= TAMANHO_TABULEIRO:
        return (linha, coluna)
    else:
        raise ValueError('cria_casa: argumentos inválidos')
    
# SELETORES
def obtem_col(casa):
    """Retorna a coluna de uma casa.

    Args:
        casa (tuple): TAD casa a examinar

    Returns:
        int: a coluna guardada na casa
    """    
    return casa[1]

def obtem_lin(casa):
    """Retorna a linha de uma casa.

    Args:
        casa (tuple): TAD casa a examinar

    Returns:
        int: a linha guardada na casa
    """    
    return casa[0]

# RECONHECEDOR 
def eh_casa(arg):
    """Avalia se o argumento passado é um TAD casa

    Args:
        arg (Any): argumento a ser avaliado

    Returns:
        bool: True caso o argumento seja um TAD casa, False caso contrário
    """    
    return (isinstance(arg, tuple)
            and len(arg) == 2 
            and all(type(num) == int 
                    and 1 <= num <= TAMANHO_TABULEIRO 
                    for num in arg))

# TESTE
def casas_iguais(c1, c2): 
    """Verifica se os dois argumentos são ambos TADs casa e iguais um ao outro.

    Args:
        c1 (Any): argumento 1
        c2 (Any): argumento 2

    Returns:
        bool: True caso sejam ambos TADs casa e iguais um ao outro, False caso contrário
    """    
    return (eh_casa(c1)
           and eh_casa(c2)
           and c1 == c2)

# TRANSFORMADORES
def casa_para_str(casa):
    """Transforma um TAD casa numa string, de forma a ficar num formato legível para o utilizador.

    Args:
        casa (tuple): TAD casa a ser transformada

    Returns:
        str: representação da casa através de uma cadeia de caracteres
    """    
    return f'({obtem_lin(casa)},{obtem_col(casa)})'

def str_para_casa(string):
    """Transforma uma string num TAD casa, utilizável em código.

    Args:
        string (str): representação da casa a ser transformada

    Returns:
        tuple: TAD casa obtido 
    """    
    return eval(string)

### FUNÇÕES DE ALTO NÍVEL

def incrementa_casa(casa, dir, dist):
    """Gera uma casa que corresponde à transformação do TAD casa fornecido através do incremento de uma das suas dimensões.

    Args:
        casa (TAD casa): casa inicial que se pretende incrementar
        dir (str): direção em que se pretende incrementar a casa ('H' para horizontal, 'V' para vertical)
        dist (int): quantidade de linhas/colunas que se pretende incrementar a casa

    Returns:
        TAD casa: casa incrementada
    """    
    try:
        if dir == 'H':
            return cria_casa(obtem_lin(casa), obtem_col(casa) + dist)
        if dir == 'V':
            return cria_casa(obtem_lin(casa) + dist, obtem_col(casa))
    except ValueError:
        return casa


##### TAD: JOGADOR
### FUNÇÕES DE BAIXO NÍVEL
# CONSTRUTOR
def cria_humano(nome):
    """Recebe um nome e cria um jogador humano com esse nome.

    Args:
        nome (str): nome do jogador

    Raises:
        ValueError: caso o nome não seja uma string ou seja uma string vazia

    Returns:
        dict: TAD jogador com o nome `nome`, 0 pontos e sem letras
    """    
    if type(nome) != str or not nome:
        raise ValueError('cria_humano: argumento inválido')
    return {'nome': nome, 'pontos': 0, 'letras': []}

def cria_agente(nivel):
    """Recebe um nível de dificuldade e cria um jogador agente com esse nível de dificuldade.

    Args:
        nivel (str): nível de dificuldade do agente ('FACIL', 'MEDIO' ou 'DIFICIL')

    Raises:
        ValueError: caso o nível inserido não seja um dos 3 especificados

    Returns:
        dict: TAD jogador com o nível `nivel`, 0 pontos e sem letras
    """    
    if nivel not in ('FACIL', 'MEDIO', 'DIFICIL'):
        raise ValueError('cria_agente: argumento inválido')
    return {'nivel': nivel, 'pontos': 0, 'letras': []}

# SELETORES
def jogador_identidade(jogador):
    """Recebe um jogador e devolve o seu nome, caso seja humano, e o seu nível, caso seja um agente.

    Args:
        jogador (dict): TAD jogador a examinar

    Returns:
        str: nome do jogador, caso humano, ou nível de dificuldade, caso agente
    """    
    if 'nome' in jogador.keys():
        return jogador['nome']
    return jogador['nivel']

def jogador_pontos(jogador):
    """Recebe um jogador e devolve os seus pontos.

    Args:
        jogador (dict): TAD jogador a examinar

    Returns:
        int: pontuação do jogador
    """    
    return jogador['pontos']

def jogador_letras(jogador):
    """Recebe um jogdor e retorna uma string com as suas letras ordenadas.

    Args:
        jogador (dict): TAD jogador a examinar

    Returns:
        str: string com as letras ordenadas do jogador
    """    
    return ''.join(sorted(jogador['letras'], key=lambda x: ABECEDARIO.index(x)))

# MODIFICADORES
def recebe_letra(jogador, letra):
    """Adiciona a letra `letra` às letras do jogador `jogador`, e retorna o jogador.

    Args:
        jogador (dict): TAD jogador a modificar
        letra (str): letra a adicionar ao inventário do jogador

    Returns:
        dict: TAD jogador modificado
    """    
    jogador['letras'].append(letra)
    return jogador

def usa_letra(jogador, letra):
    """Remove a letra `letra` das letras do jogador `jogador`, e retorna o jogador.

    Args:
        jogador (dict): TAD jogador a modificar
        letra (str): letra a remover do inventário do jogador

    Returns:
        dict: TAD jogador modificado
    """    
    jogador['letras'].remove(letra)
    return jogador

def soma_pontos(jogador, pontos):
    """Soma o número de pontos `pontos` à pontuação do jogador `jogador`, e retorna o jogador.

    Args:
        jogador (dict): TAD jogador a modificar
        pontos (int): número de pontos a adicionar

    Returns:
        dict: TAD jogador modificado
    """    
    jogador['pontos'] += pontos
    return jogador

# RECONHECEDOR
def eh_jogador(arg):
    """Avalia se o argumento passado é um TAD jogador válido.

    Args:
        arg (Any): argumento a ser avaliado

    Returns:
        bool: True caso o argumento seja um TAD jogador, False caso contrário
    """    
    return (type(arg) == dict
            and len(arg) == 3
            and 'pontos' in arg.keys()
            and 'letras' in arg.keys()
            and (('nome' in arg.keys() and len(arg['nome'])) or ('nivel' in arg.keys() and len(arg['nivel'])))
            and type(arg['pontos']) == int and arg['pontos'] >= 0
            and type(arg['letras']) == list)

def eh_humano(arg):
    """Avalia se o argumento passado é um TAD jogador humano.

    Args:
        arg (Any): argumento a ser avaliado

    Returns:
        bool: True caso o argumento seja um TAD jogador humano, False caso contrário
    """    
    return eh_jogador(arg) and 'nome' in arg.keys()

def eh_agente(arg):
    """Avalia se o argumento passado é um TAD jogador agente.

    Args:
        arg (Any): argumento a ser avaliado

    Returns:
        bool: True caso o argumento seja um TAD jogador agente, False caso contrário
    """    
    return eh_jogador(arg) and not eh_humano(arg)    

# TESTE
def jogadores_iguais(j1, j2):
    """Avalia se dois argumentos são ambos jogadores e iguais um ao outro.

    Args:
        j1 (Any): primeiro argumento a ser avaliado
        j2 (Any): segundo argumento a ser avaliado

    Returns:
        bool: True caso ambos sejam jogadores e iguais um ao outro, False caso contrário
    """    
    return (eh_jogador(j1) and eh_jogador(j2)
            and ((eh_agente(j1) and eh_agente(j2)) or (eh_humano(j1) and eh_humano(j2)))
            and jogador_identidade(j1) == jogador_identidade(j2)
            and jogador_pontos(j1) == jogador_pontos(j2)
            and sorted(jogador_letras(j1)) == sorted(jogador_letras(j2)))

# TRANSFORMADOR
def jogador_para_str(jog):
    """Converte o perfil de um jogador para formato string, legível para o utilizador.

    Args:
        jog (dict): TAD jogador a transformar

    Returns:
        str: string do tipo '<IDENTIDADE> (<PONTOS>): <LETRAS>'
    """    
    if eh_humano(jog):
        return f"{jogador_identidade(jog)} ({jogador_pontos(jog):>3}):{' ' if jogador_letras(jog) else ''}{' '.join(jogador_letras(jog))}"
    if eh_agente(jog):
        return f"BOT({jogador_identidade(jog)}) ({jogador_pontos(jog):>3}):{' ' if jogador_letras(jog) else ''}{' '.join(jogador_letras(jog))}"
        
### FUNÇÕES DE ALTO NÍVEL           
def distribui_letras(jog, saco, num):
    """Retira `num` letras da lista `saco` e adiciona-a às letras do jogador `jog`.

    Args:
        jog (TAD jogador): jogador que vai receber as letras
        saco (list): lista de letras de onde vão ser retiradas as letras
        num (int): número de letras que vão ser retiradas do saco

    Returns:
        TAD jogador: o jogador modificado
    """    
    for _ in range(num):
        if saco:
            recebe_letra(jog, saco.pop())
    return jog

##### TAD: VOCABULARIO
### AUXILIARES (não pedidas no enunciado) (BAIXO NÍVEL)
def palavra_existe(vocab, palavra): 
    """Verifica se uma palavra existe num vocabulário.

    Args:
        vocab (dict): TAD vocabulário onde a palavra vai ser procurada
        palavra (str): palavra a procurar no vocabulário

    Returns:
        bool: True caso seja encontrada, False caso contrário
    """    
    return (len(palavra) in vocab 
            and palavra[0] in vocab[len(palavra)] 
            and palavra in vocab[len(palavra)][palavra[0]][1])

### FUNÇÕES DE BAIXO NÍVEL
# CONSTRUTOR
def cria_vocabulario(palavras):
    """Recebe um tuplo de palavras e retorna um TAD vocabulário com essas palavras.

    Args:
        palavras (tuple): tuplo com strings das palavras a adicionar

    Raises:
        ValueError: caso o argumento passado não seja um tuplo não vazio de strings que representem palavras válidas

    Returns:
        dict: TAD vocabulário criado
    """    
    # VALIDAÇÃO DOS ARGUMENTOS
    if (type(palavras) != tuple
        or not palavras
        or len(palavras) != len(set(palavras))
        or any((type(palavra) != str or not (2 <= len(palavra) <= TAMANHO_TABULEIRO)) for palavra in palavras)
        or any(letra not in ABECEDARIO for palavra in palavras for letra in palavra)):
        raise ValueError('cria_vocabulario: argumento inválido')
    
    # CRIAÇÃO DO VOCABULÁRIO   
    vocab = {}
    for palavra in palavras:
        pontos = sum(PONTOS[letra] for letra in palavra)
        tuplo = (palavra, pontos)
        if len(palavra) in vocab and palavra[0] in vocab[len(palavra)]:
            vocab[len(palavra)][palavra[0]][0].append(tuplo)
            vocab[len(palavra)][palavra[0]][1].add(palavra)
        elif len(palavra) in vocab:
            vocab[len(palavra)].update({palavra[0]: ([tuplo], {palavra})})
        else:
            vocab[len(palavra)] = {palavra[0]: ([tuplo], {palavra})}

    # ordenamos logo as listas para não termos de ordenar sempre no obtem_palavras()
    for comp in vocab:
        for letra in vocab[comp]:
            vocab[comp][letra][0].sort(key=lambda t: (-t[1], tuple(ABECEDARIO.index(l) for l in t[0])))

    return vocab

# SELETORES
def obtem_pontos(vocab, palavra):
    """recebe um TAD vocabulario e uma string `palavra` e devolve os pontos associados a essa palavra, obtidos através da soma das pontuções das suas letras.

    Args:
        vocab (dict): TAD vocabulário onde a palavra deve estar presente
        palavra (str): palavra a avaliar

    Returns:
        int: pontuação da palavra
    """    
    # VERIFICAÇÃO DE QUE EXISTE
    if not palavra_existe(vocab, palavra):
        return 0
    
    # EXTRAÇÃO DOS PONTOS
    return sum(PONTOS[letra] for letra in palavra)

def obtem_palavras(vocab, comp, letra):
    """Recebe um TAD vocab, um int `comprimento` e uma string `letra`, e devolve um tuplo de todas as palavras em `vocab` com o respetivo comprimento e primeira letra.

    Args:
        vocab (dict): TAD vocabulário a examinar
        comp (int): comprimento das palavras a procurar
        letra (str): string com a primeira letra das palavras a procurar

    Returns:
        tuple: tuplo de todas as palavras que pertencem ao vocabulário com a primeira letra `letra` e o comprimento `comp`
    """    
    return tuple(vocab[comp][letra][0]) if comp in vocab and letra in vocab[comp] else ()

# TESTE
def testa_palavra_padrao(vocab, palavra, padrao, letras):
    '''
    Verifica se é possível inserir uma palavra num espaço selecionado, com base nas letras disponíveis no inventário de um jogador,
    comparando-a a um padrão extraído do tabuleiro.

    Args: 
        vocab (dict): TAD vocabulário que contém as palavras que se podem utilizar
        palavra (str): palavra que pretendemos inserir
        padrao (str): representa o padrão avaliado onde pretendemos inserir a palavra
        letras (str): string com as letras disponíveis

    Returns:
        bool: True se for possível chegar à palavra escolhida através da inserção de letras no padrão, False caso contrário
    '''
    if len(palavra) != len(padrao) or not palavra_existe(vocab, palavra):
        return False
    
    letras_dict = {letra: letras.count(letra) for letra in set(letras)} # dicionário em vez de lista por otimização.
    for letra_palavra, letra_padrao in zip(palavra, padrao):
        if letra_palavra == letra_padrao:
            continue

        if letra_padrao != CASA_VAZIA: # se são diferentes mas a casa está ocupada por uma letra
            return False
        # a casa no padrão está vazia:
        if letras_dict.get(letra_palavra, 0) > 0:
            letras_dict[letra_palavra] -= 1
        else:
            return False
            
    # se chegámos aqui, a palavra é válida
    return True

# TRANSFORMADORES:
def ficheiro_para_vocabulario(nome_fich):
    """Recebe o nome de um ficheiro e retorna o vocabulário composto pelas palavras dispostas nas suas linhas.

    Args:
        nome_fich (str): nome do ficheiro que se pretende passar a vocabulário

    Returns:
        dict: TAD vocabulário com as palavras válidas do ficheiro
    """    
    with open(nome_fich, 'r') as file:
        # transformamos num set antes de passar a tuple para evitar repetições
        return cria_vocabulario(tuple({linha.strip().upper() for linha in file if 2 <= len(linha.strip()) <= TAMANHO_TABULEIRO and all(char in ABECEDARIO for char in linha.strip().upper())}))
    
def vocabulario_para_str(vocab):
    """Transforma o tad vocabulario `vocab` recebido numa string com carcteres de mudança de linha a separar as respetivas palavras.

    Args:
        vocab (dict): TAD vocabulario a transformar

    Returns:
        str: string que representa as palavras no vocabulário
    """    
    # primeiro por comprimento, depois por ordem da primeira letra, depois por pontos decrescente, depois por ordem lexicográfica
    return '\n'.join(sorted([tuplo[0] for subdict in vocab.values() for lista_de_tuplos, _ in subdict.values() for tuplo in lista_de_tuplos], key=lambda palavra: (len(palavra), palavra[0], -obtem_pontos(vocab, palavra), tuple(ABECEDARIO.index(letra) for letra in palavra))))

### FUNÇÕES DE ALTO NÍVEL
def procura_palavra_padrao(vocab, padrao, letras, min_pontos):
    """Recebe um TAD `vocab`, uma string `padrao`, uma string `letras` e um inteiro `min_pontos` e
    retorna, das palavra em `vocab` que é possível formar aplicando as letras de `letras` ao `padrao`, 
    aquela que vale mais pontos, ou, no caso de empate, a que vem primeiro em ordem lexicográfica.

    Args:
        vocab (dict): TAD vocabulário para pesquisa
        padrao (str): padrão com letras e espaços livres
        letras (str): letras disponíveis para preencher os espaços livres do padrão
        min_pontos (int): o mínimo de pontos que uma palavra precisa de ter para ser aceite

    Returns:
        tuple: tuplo com a palavra escolhida e a sua pontuação
    """      
    melhor_palavra_pontos = ('', 0)
    
    # se o padrão começa com uma letra:
    if padrao[0] != CASA_VAZIA:
        palavras_candidatas = obtem_palavras(vocab, len(padrao), padrao[0])
        for palavra, pontos in palavras_candidatas:
            if pontos < min_pontos or pontos < melhor_palavra_pontos[1]:
                break
                
            if testa_palavra_padrao(vocab, palavra, padrao, letras):

                if pontos >= min_pontos:
                    return (palavra, pontos) # como o output de obtem_palavras() está ordenado por ordem decrescente, podemos escolher o primeiro resultado
                else:
                    break
        return ('', 0) 

    # se o padrão começa com um espaço vazio:
    letras_unicas_mao = set(letras) # para não repetirmos primeiras letras
    for letra in letras_unicas_mao:
        palavras_candidatas = obtem_palavras(vocab, len(padrao), letra)  
        for palavra, pontos in palavras_candidatas:
            if pontos < min_pontos or pontos < melhor_palavra_pontos[1]:
                break 
            if pontos == melhor_palavra_pontos[1] and melhor_palavra_pontos[0] != '': # escolhemos por ordem lexicográfica
                atual = tuple(ABECEDARIO.index(l) for l in palavra)
                melhor = tuple(ABECEDARIO.index(l) for l in melhor_palavra_pontos[0])
                if atual >= melhor:
                    continue # a melhor vem primeiro lexicograficamente
            if testa_palavra_padrao(vocab, palavra, padrao, letras):
                melhor_palavra_pontos = (palavra, pontos)
                
    if melhor_palavra_pontos[1] >= min_pontos:
        return melhor_palavra_pontos
    return ('', 0)


##### TAD: TABULEIRO
### FUNÇÕES DE BAIXO NÍVEL
# CONSTRUTOR
def cria_tabuleiro():
    """Cria um tabuleiro de tamanho especificado em `TAMANHO_TABULEIRO`.

    Returns:
        list: TAD tabuleiro com lado `TAMANHO_TABULEIRO`
    """    
    return [[CASA_VAZIA for _ in range(TAMANHO_TABULEIRO)] for _ in range(TAMANHO_TABULEIRO)]

# SELETORES
def obtem_letra(tab, casa):
    '''
    Extrai o valor que estiver inserido numa casa do tabuleiro através das suas coordenadas ('.' caso vazia).

    Args:
        tab (list): TAD tabuleiro a examinar 
        casa (TAD casa): casa com as coordenadas a examinar
    Returns: 
        str: string com o conteúdo que se encontra na casa selecionada
    '''
    return tab[obtem_lin(casa) - 1][obtem_col(casa) - 1] # subtraímos 1 para traduzir as coordenadas do jogador para coordenadas "reais"

# MODIFICADORES
def insere_letra(tab, casa, letra):
    '''
    Preenche a casa selecionada no tabuleiro com uma letra.

    Args:
        tab (list): TAD tabuleiro a modificar
        casa (TAD casa): tuplo com as coordenadas da casa a preencher
        letra (str): string com a letra que se pretende inserir
    Returns:
        list: TAD tabuleiro com a casa preenchida pela letra especificada
    '''
    tab[obtem_lin(casa) - 1][obtem_col(casa) - 1] = letra # subtraímos 1 para traduzir as coordenadas do jogador para coordenadas "reais"
    return tab

# RECONHECEDORES
def eh_tabuleiro(arg):
    """Verifica se o argumento fornecido é um TAD tabuleiro válido.

    Args:
        arg (Any): argumento a avaliar

    Returns:
        bool: True caso seja um TAD tabuleiro, False caso contrário
    """    
    return (isinstance(arg, list)
            and all(isinstance(linha, list) for linha in arg)
            and len(arg)
            and all(len(linha) == len(arg) == TAMANHO_TABULEIRO for linha in arg)
            and all((valor == CASA_VAZIA or valor in ABECEDARIO) for linha in arg for valor in linha))

def eh_tabuleiro_vazio(arg):
    """Verifica se o argumento fornecido é um tabuleiro vazio.

    Args:
        arg (Any): argumento a avaliar

    Returns:
        bool: True caso o argumento seja um tabuleiro vazio, False caso contrário
    """    
    return eh_tabuleiro(arg) and all(valor == CASA_VAZIA for linha in arg for valor in linha)

#TESTE
def tabuleiros_iguais(t1, t2):
    """Verifica se dois argumentos são ambos tabuleiros e se são iguais.

    Args:
        t1 (Any): primeiro argumento a avaliar
        t2 (Any): segundo argumento a avaliar

    Returns:
        bool: True caso ambos os argumentos sejam tabuleiros e iguais um ao outro, False caso contrário
    """    
    return eh_tabuleiro(t1) and eh_tabuleiro(t2) and t1 == t2

# TRANSFORMADOR
def tabuleiro_para_str(tab) -> str:
    '''Converte um tabuleiro de jogo para formato string, legível para o utilizador.

    Args: 
        tab (list): TAD tabuleiro a converter
    
    Returns:
        display (str): string que dispõe o conteúdo do tabuleiro, bem como a moldura e contagem das linhas/colunas
    '''
    cima = ' ' * 4
    for i in range(1, TAMANHO_TABULEIRO + 1):
        cima += f" {i // 10 if i >= 10 else ' '}" # espaço em branco na casa das dezenas até chegar ao 10
    cima += '\n    '
    for i in range(1, TAMANHO_TABULEIRO + 1):
        cima += f" {i % 10}"
    cima += '\n'

    borda_baixo = '   +'
    for _ in range(TAMANHO_TABULEIRO):
        borda_baixo += '--'
    borda_baixo += '-+'

    borda_cima = borda_baixo + '\n'
     
    linhas = ''.join(f"{i+1:>2} | {' '.join(tab[i])} |\n" for i in range(TAMANHO_TABULEIRO))

    display = cima + borda_cima + linhas + borda_baixo
    return display

### FUNÇÕES DE ALTO NÍVEL
def obtem_padrao(tab, inicial, final):
    """Extrai um padrão de um tabuleiro `tab`, desde a casa `inicial` até à `final`

    Args:
        tab (TAD tabuleiro): tabuleiro de onde se vai retirar o padrão
        inicial (TAD casa): casa onde se inicia a extração
        final (TAD casa): casa onde termina a extração

    Returns:
        str: sequência de caracteres que reflete o que ocorre no tabuleiro entre as duas casas
    """    
    if obtem_lin(inicial) != obtem_lin(final):
        return ''.join(obtem_letra(tab, incrementa_casa(inicial, 'V', i)) for i in range(obtem_lin(final) + 1 - obtem_lin(inicial)))
        # junta os valores de todas as casas entre a `inicial` e a `final`
    if obtem_col(inicial) != obtem_col(final):
        return ''.join(obtem_letra(tab, incrementa_casa(inicial, 'H', i)) for i in range(obtem_col(final) + 1 - obtem_col(inicial)))
    # se forem iguais:
    return obtem_letra(tab, inicial)

def insere_palavra(tab, casa, direcao, palavra):
    '''
    Preenche o espaço selecionado no tabuleiro com uma palavra.

    Args:
        tab (TAD tabuleiro): tabuleiro a modificar
        casa (TAD casa): casa onde vai ser colocada a primeira letra da palavra
        direcao (str): direção em que a palavra vai ser escrita ('H' para horizontal e 'V' para vertical)
        palavra (str): palavra a inserir
    
    Returns:
        TAD tabuleiro: tabuleiro modificado, com o espaço preenchido pela palavra especificada
    '''
    for i, letra in zip(range(len(palavra)), palavra):
        insere_letra(tab, incrementa_casa(casa, direcao, i), letra)
    return tab

def obtem_subpadroes(tab, inicial, final, max_livres):
    """Extrai todos os subpadrões válidos obtíveis entre duas casas de um tabuleiro, bem como um tuplo com as casas iniciais de cada um

    Args:
        tab (TAD tabuleiro): tabuleiro de onde se extrai o padrão
        inicial (TAD casa): casa inicial, onde a extração começa
        final (TAD casa): casa final, onde a extração termina
        max_livres (int): número máximo de casas livres que um padrão pode ter para ser válido

    Returns:
        tuple: tuplo composto por dois tuplos: um com os subpadrões obtidos, e outro com as respetivas casas iniciais
    """    
    padrao = obtem_padrao(tab, inicial, final)
    res = [(),()]
    for i in range(len(padrao)):
        for j in range(len(padrao), i, -1):
            if (CASA_VAZIA in padrao[i:j] 
                and any(letra != CASA_VAZIA for letra in padrao[i:j])
                and (i == 0 or padrao[i - 1] == CASA_VAZIA) # verificamos se i == 0 para evitar IndexError
                and (j == len(padrao) or padrao[j] == CASA_VAZIA) 
                and padrao[i:j].count(CASA_VAZIA) <= max_livres):
                # condições definidas em 2.1)
                res[0] += (padrao[i:j],)
                if obtem_lin(inicial) != obtem_lin(final):
                    # vertical
                    res[1] += (incrementa_casa(inicial, 'V', i),) # parênteses à volta para dar para concatenar
                elif obtem_col(inicial) != obtem_col(final):
                    # horizontal
                    res[1] += (incrementa_casa(inicial, 'H', i),)
                else: #iguais ??
                    res[1] += (inicial,)
    return tuple(res)

def gera_todos_padroes(tab, max_livres):
    """Cria um tuplo com todos os subpadrões válidos de todas as linhas e colunas de um tabuleiro, com um máximo de `max_livres` espaços livres, incluindo também as suas casas iniciais e direções

    Args:
        tab (TAD tabuleiro): tabuleiro de onde vão ser extraídos os padrões
        max_livres (int): máximo de espaços livres por padrão

    Returns:
        tuple: tuplo que inclui, respetivamente, um tuplo com todos os padrões, um com as casas iniciais de cada um, e outro com as suas direções ('H' ou 'V')
    """    
    res = [(), (), ()]
    for i in range(1, TAMANHO_TABULEIRO + 1):
        # criamos casas inicial e final para podermos usar nas funções dos padrões
        inicial = cria_casa(i, 1)
        final = cria_casa(i, TAMANHO_TABULEIRO)
        padroes, casas = obtem_subpadroes(tab, inicial, final, max_livres)
        res[0] += padroes
        res[1] += casas
        res[2] += tuple('H' for _ in range(len(padroes)))
    for i in range(1, TAMANHO_TABULEIRO + 1):
        inicial = cria_casa(1, i)
        final = cria_casa(TAMANHO_TABULEIRO, i)
        padroes, casas = obtem_subpadroes(tab, inicial, final, max_livres)
        res[0] += padroes
        res[1] += casas
        res[2] += tuple('V' for _ in range(len(padroes)))
    return tuple(res)

##### FUNÇÕES ADICIONAIS
def gera_numero_aleatorio(s: int) -> int:
    '''Gera um número pseudo-aleatório através de um algoritmo que aplica a operação 'xorshift' num valor inicial designado por 'seed'. 
    Cada vez que esta operação for aplicada, obtemos um novo 'estado' do gerador.

    Args:
        s (int): seed. Este parâmetro é modificado consoante o algoritmo e devolvido após ser processado.
    
    Returns:
        s (int): inteiro que corresponde ao número pseudo-aleatório que prentendíamos gerar. Este número nunca varia se utilizarmos sempre a mesma 'seed' para o gerar.
    '''
    s ^= (s << 13) & 0xFFFFFFFF
    s ^= (s >> 17) & 0xFFFFFFFF
    s ^= (s << 5) & 0xFFFFFFFF
    return s

def permuta_letras(letras: list[str], estado: int):
    '''Troca a ordem de elementos de uma lista com base no algoritmo de Fisher-Yates.
    Esta função modifica destrutivamente a própria lista `letras`, não retornando nenhum valor.
    
    Args:
        letras (list): lista de letras que pretendemos baralhar
        estado (int): inteiro que representa o estado inicial do gerador com que efetuamos cada operação
    '''
    for i in range(len(letras) - 1, 0, -1):
        estado = gera_numero_aleatorio(estado) # atualiza o estado cada vez que uma troca é efetuada
        letras[i], letras[estado % (i + 1)] = letras[estado % (i + 1)], letras[i]
    return

def baralha_saco(seed):
    """Cria uma pilha ao baralhar as letras do `SACO`, com base numa seed.

    Args:
        seed (int): estado do gerador utilizado para baralhar o saco

    Returns:
        list: lista de letras baralhada
    """    
    conjunto_baralhado = sorted([key for key in SACO for _ in range(SACO[key])], key=lambda x: ABECEDARIO.index(x))
    permuta_letras(conjunto_baralhado, seed)
    return conjunto_baralhado

def jogada_humano(tab, jog, vocab, pilha):
    """Processa a jogada de um jogador humano, aceitando as jogadas passar ('P'), trocar ('T' seguido da sequência de letras a trocar, separadas por um espaço),
    e jogar ('J' seguido da linha e coluna da casa inicial, a direção ('H' ou 'V'), e a palavra a inserir).

    Args:
        tab (TAD tabuleiro): o tabuleiro de jogo
        jog (TAD jogador): o jogador de quem é a vez
        vocab (TAD vocabulário): vocabulário para consulta de palavras
        pilha (list): lista de letras com as quais se substituem as letras usadas no inventário do jogador

    Returns:
        bool: True caso o jogador jogue ou troque, False caso passe
    """    
    while True: # quando o programa deteta um input válido, executa as instruções apropriadas e sai do loop
        jogada_raw = input(f"Jogada {jogador_identidade(jog)}: ")
        jogada = jogada_raw.strip().split() # dividimos o input em elementos de uma lista para facilitar a análise
        if not jogada:
            continue
        if jogada[0] == 'P': # PASSAR
            if len(jogada) == 1:
                return False
            
        if jogada[0] == 'T': # TROCAR
            seq_letras = jogada[1:]
            if not seq_letras:
                continue

            # verifica se todas as letras existem no inventário do jogador e em quantidade suficiente, bem como se todas as letras são válidas e a pilha contem pelo menos 7 letras
            if (all(letra in jogador_letras(jog)
                and seq_letras.count(letra) <= jogador_letras(jog).count(letra) 
                and letra in ABECEDARIO for letra in seq_letras) 
                and len(pilha) >= NUMERO_LETRAS):
                for letra in seq_letras: # retira cada letra do inventário do jogador
                    usa_letra(jog, letra)
                for _ in range(len(seq_letras)): # retira letras da pilha e adiciona-as ao inventário do jogador
                    recebe_letra(jog, pilha.pop())
                return True
            
        if (jogada[0] == 'J' # JOGAR
            and len(jogada) == 5 
            and jogada[1].isdigit() 
            and jogada[2].isdigit() 
            and 1 <= int(jogada[1]) <= TAMANHO_TABULEIRO 
            and 1 <= int(jogada[2]) <= TAMANHO_TABULEIRO 
            and (jogada[3] == 'V' or jogada[3] == 'H') 
            and all(letra in ABECEDARIO for letra in jogada[4])
            and 2 <= len(jogada[4]) <= TAMANHO_TABULEIRO):
            # verifica se todas as letras existem no inventário do jogador e em quantidade suficiente, bem como se todas as letras e coordenadas são válidas
            dir = jogada[3]
            palavra = jogada[4]
            inicial = cria_casa(int(jogada[1]), int(jogada[2]))
            final = incrementa_casa(inicial, dir, len(palavra) - 1)
            if inicial == final: # se incrementa_casa() passou dos limites do tabuleiro
                continue
            padrao = obtem_padrao(tab, inicial, final)
            # impedir que o humano escolha um padrão que tenha uma letra imediatamente antes ou depois
            if dir == 'H':
                # casa antes da inicial
                if obtem_col(inicial) > 1:
                    casa_antes = cria_casa(obtem_lin(inicial), obtem_col(inicial) - 1)
                    if obtem_letra(tab, casa_antes) != CASA_VAZIA:
                        continue
                # casa depois do final
                if obtem_col(final) < TAMANHO_TABULEIRO:
                    casa_depois = cria_casa(obtem_lin(final), obtem_col(final) + 1)
                    if obtem_letra(tab, casa_depois) != CASA_VAZIA:
                        continue
            else: # 'V'
                if obtem_lin(inicial) > 1:
                    casa_antes = cria_casa(obtem_lin(inicial) - 1, obtem_col(inicial))
                    if obtem_letra(tab, casa_antes) != CASA_VAZIA:
                        continue
                if obtem_lin(final) < TAMANHO_TABULEIRO:
                    casa_depois = cria_casa(obtem_lin(final) + 1, obtem_col(final))
                    if obtem_letra(tab, casa_depois) != CASA_VAZIA:
                        continue
            if CASA_VAZIA not in padrao:
                continue
            if eh_tabuleiro_vazio(tab):
                centro = cria_casa(COORDS_CASA_CENTRAL[0], COORDS_CASA_CENTRAL[1]) # (8,8)
                cobre_centro = False
                if dir == 'H' and obtem_lin(inicial) == obtem_lin(centro) and obtem_col(inicial) <= obtem_col(centro) <= obtem_col(final):
                    cobre_centro = True
                elif dir == 'V' and obtem_col(inicial) == obtem_col(centro) and obtem_lin(inicial) <= obtem_lin(centro) <= obtem_lin(final):
                    cobre_centro = True

                if not cobre_centro:
                    continue # se for a primeira e nao cobrir o centro
            if all(char == CASA_VAZIA for char in padrao) and not eh_tabuleiro_vazio(tab): # se nao for a primeira e nao intercetar outras palavras
                continue 

            if not testa_palavra_padrao(vocab, palavra, padrao, jogador_letras(jog)):
                continue

            # CONSEGUE JOGAR
            insere_palavra(tab, inicial, dir, jogada[4])
            for i in range(len(palavra)):
                if padrao[i] == CASA_VAZIA:
                    usa_letra(jog, palavra[i])
            distribui_letras(jog, pilha, padrao.count(CASA_VAZIA))
            soma_pontos(jog, obtem_pontos(vocab, palavra))
            return True
        
def jogada_agente(tab, jog, vocab, pilha):
    """Processa a jogada de um jogador agente, que avalia e executa a melhor jogada que encontrar.

    Args:
        tab (TAD tabuleiro): o tabuleiro de jogo
        jog (TAD jogador): o jogador de quem é a vez
        vocab (TAD vocabulário): vocabulário para consulta de palavras
        pilha (list): lista de letras com as quais se substituem as letras usadas no inventário do jogador

    Returns:
        bool: True caso o jogador jogue ou troque, False caso passe
    """    
    if eh_tabuleiro_vazio(tab):
        print(f'Jogada {jogador_identidade(jog)}: P')
        return False

    # TENTATIVA DE JOGAR
    nivel = jogador_identidade(jog)
    if nivel == 'FACIL':
        N_padroes = 100
    elif nivel == 'MEDIO':
        N_padroes = 50
    else:
        N_padroes = 10

    padroes, casas, direcoes = gera_todos_padroes(tab, len(jogador_letras(jog)))
    padroes = padroes[::N_padroes]
    casas = casas[::N_padroes]
    direcoes = direcoes[::N_padroes]

    melhor_palavra_pontos = ('', 0)
    melhor_padrao_casa_direcao = ()

    for i in range(len(padroes)):
        palavra, pontos = procura_palavra_padrao(vocab, padroes[i], jogador_letras(jog), melhor_palavra_pontos[1])
        if pontos > melhor_palavra_pontos[1]:  # consegue jogar
            melhor_palavra_pontos = (palavra, pontos)
            melhor_padrao_casa_direcao = (padroes[i], casas[i], direcoes[i])

    if melhor_palavra_pontos[0]:
        palavra = melhor_palavra_pontos[0]
        pontos = melhor_palavra_pontos[1]
        padrao, casa, direcao = melhor_padrao_casa_direcao
        insere_palavra(tab, casa, direcao, palavra)
        for j, letra in enumerate(palavra):
            if padrao[j] == CASA_VAZIA and letra in jogador_letras(jog):  # CORREÇÃO AQUI
                usa_letra(jog, letra)
        distribui_letras(jog, pilha, padrao.count(CASA_VAZIA))
        soma_pontos(jog, pontos)
        print(f'Jogada {jogador_identidade(jog)}: J {obtem_lin(casa)} {obtem_col(casa)} {direcao} {palavra}')
        return True

    # SE NÃO CONSEGUIU JOGAR
    if len(pilha) >= NUMERO_LETRAS:
        letras = jogador_letras(jog)
        print(f"Jogada {jogador_identidade(jog)}: T {' '.join(letras)}")
        for letra in list(letras):
            usa_letra(jog, letra)
        distribui_letras(jog, pilha, NUMERO_LETRAS)
        return True

    # SE NÃO CONSEGUIU TROCAR
    print(f"Jogada {jogador_identidade(jog)}: P")
    return False

def scrabble2(jogadores, nome_fich, seed):
    """Inicia um jogo de Scrabble, e retorna a pontuação dos jogadores no final.

    Args:
        jogadores (tuple): tuplo com os nomes dos jogadores (caso humanos) e nível de dificuldade antecedido de '@' (caso agentes)
        nome_fich (str): nome do ficheiro de onde se pretende extrair o vocabulário, não vazio
        seed (int): estado do gerador para fins de baralhamento do saco, inteiro positivo

    Raises:
        ValueError: caso algum dos argumentos não seja válido, de acordo com as indicações especificadas

    Returns:
        tuple: tuplo com as pontuações dos jogadores pela ordem em que foram inseridos
    """    
    # VALIDAÇÃO DOS ARGUMENTOS

    if (type(jogadores) != tuple
        or not 2 <= len(jogadores) <= 4
        or not all(type(jog) == str and jog for jog in jogadores)
        or type(nome_fich) != str
        or not nome_fich
        or type(seed) != int 
        or seed <= 0):
        raise ValueError('scrabble2: argumentos inválidos')

    # PREPARAÇÃO
    vocab = ficheiro_para_vocabulario(nome_fich)
    pilha = baralha_saco(seed) # criação de uma lista com base no dicionário `SACO`
    lista_jogadores = []
    for identidade in jogadores:
        if identidade[0] == '@':
            if len(identidade) == 1 or identidade[1:] not in ('FACIL', 'MEDIO', 'DIFICIL'):
                raise ValueError('scrabble2: argumentos inválidos')
            lista_jogadores.append(cria_agente(identidade[1:]))
        else:
            lista_jogadores.append(cria_humano(identidade))
    end = False # flag para determinar o fim do jogo
    pass_counter = 0
    tab = cria_tabuleiro()
    insere_palavra(tab, (8,8), 'V', 'MEIAS')
    for jogador in lista_jogadores:
        distribui_letras(jogador, pilha, 7) # todos os jogadores recebem 7 letras

    # INÍCIO DO JOGO
    print('Bem-vindo ao SCRABBLE2.')
    # insere_palavra(tab, cria_casa(8,8), 'H', 'AMOR')
    while True:
        for jogador in lista_jogadores:
            print(tabuleiro_para_str(tab))
            for jogador_a_imprimir in lista_jogadores:
                print(jogador_para_str(jogador_a_imprimir))
            if eh_agente(jogador):
                if jogada_agente(tab, jogador, vocab, pilha):
                    pass_counter = 0
                else:
                    pass_counter += 1 # o booleano retornado é usado para contar os "pass"    
            if eh_humano(jogador):
                if jogada_humano(tab, jogador, vocab, pilha):
                    pass_counter = 0
                else:
                    pass_counter += 1
            if (not pilha and any(not jogador_letras(player) for player in lista_jogadores)) or pass_counter >= len(lista_jogadores):
                end = True # o jogo acaba quando os requisitos apropriados são alcançados
                break
        if end:
            break
    pontuação = tuple(jogador_pontos(jog) for jog in lista_jogadores)
    return pontuação

scrabble2(('@DIFICIL', '@DIFICIL', '@DIFICIL'), 'vocab25k.txt', 5)