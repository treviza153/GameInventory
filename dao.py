# coding: utf-8
from models import Jogo, Usuario

SQL_DELETA_JOGO = 'delete from jogo where id = %s'
SQL_DELETA_USUARIO = 'delete from usuario where id = %s'
SQL_JOGO_POR_ID = 'SELECT id, nome, categoria, console from jogo where id = %s'
SQL_USUARIO_POR_ID = 'SELECT id, nome, senha, grupo from usuario where id = %s'
SQL_CADASTRA_USUARIO = 'INSERT into usuario (id, nome, senha, grupo) values (%s, %s, %s, %s)'
SQL_ATUALIZA_JOGO = 'UPDATE jogo SET nome=%s, categoria=%s, console=%s where id = %s'
SQL_BUSCA_JOGOS = 'SELECT id, nome, categoria, console from jogo'
SQL_BUSCA_USUARIOS = 'SELECT id, nome, senha, grupo from usuario'
SQL_CRIA_JOGO = 'INSERT into jogo (nome, categoria, console) values (%s, %s, %s)'


class JogoDao:
    def __init__(self, db):
        self.__db = db

    def salvar(self, jogo):
        cursor = self.__db.connection.cursor()

        if (jogo.id):
            cursor.execute(SQL_ATUALIZA_JOGO, (jogo.nome, jogo.categoria, jogo.console, jogo.id))
        else:
            cursor.execute(SQL_CRIA_JOGO, (jogo.nome, jogo.categoria, jogo.console))
            jogo.id = cursor.lastrowid
        self.__db.connection.commit()
        return jogo

    def listar(self):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BUSCA_JOGOS)
        jogos = traduz_jogos(cursor.fetchall())
        return jogos

    def busca_por_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_JOGO_POR_ID, (id,))
        tupla = cursor.fetchone()
        return Jogo(tupla[1], tupla[2], tupla[3], id=tupla[0])

    def deletar(self, id):
        self.__db.connection.cursor().execute(SQL_DELETA_JOGO, (id, ))
        self.__db.connection.commit()


class UsuarioDao:
    def __init__(self, db):
        self.__db = db

    def buscar_por_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_USUARIO_POR_ID, (id,))
        dados = cursor.fetchone()
        usuario = traduz_usuario(dados) if dados else None
        return usuario

    def cadastrar_usuario(self, usuario):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_CADASTRA_USUARIO, (usuario.id, usuario.nome, usuario.senha, usuario.grupo))
        self.__db.connection.commit()
        return usuario

    def listar(self):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BUSCA_USUARIOS)
        usuarios = traduz_usuario_lista(cursor.fetchall())
        return usuarios

    def deletar(self, id):
        self.__db.connection.cursor().execute(SQL_DELETA_USUARIO, (id, ))
        self.__db.connection.commit()


def traduz_jogos(jogos):
    def cria_jogo_com_tupla(tupla):
        return Jogo(tupla[1], tupla[2], tupla[3], id=tupla[0])
    return list(map(cria_jogo_com_tupla, jogos))


def traduz_usuario(tupla):
    return Usuario(tupla[0], tupla[1], tupla[2], tupla[3])

def traduz_usuario_lista(usuarios):
    def cria_usuario_com_tupla(tupla):
        return Usuario(tupla[0], tupla[1], tupla[2], tupla[3])
    return list(map(cria_usuario_com_tupla, usuarios))
