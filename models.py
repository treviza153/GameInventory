# coding: utf-8
class Jogo(object):
    "Classe para jogos"

    def __init__(self, nome, categoria, console, id=None):
        self.id = id
        self.nome = nome
        self.categoria = categoria
        self.console = console


class Usuario(object):
    "Classe para usuarios"

    def __init__(self, id, nome, senha, grupo):
        self.id = id
        self.nome = nome
        self.senha = senha
        self.grupo = grupo