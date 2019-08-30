# coding: utf-8
from flask import Flask, render_template, request, redirect, session, flash, url_for
from models import Jogo, Usuario
from dao import JogoDao, UsuarioDao
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'flask'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Paty!@#$1234'
app.config['MYSQL_DB'] = 'jogoteca'
app.config['MYSQL_PORT'] = 3306

db = MySQL(app)

jogo_dao = JogoDao(db)
usuario_dao = UsuarioDao(db)

# USUARIO
@app.route('/')
def login():
    next = request.args.get('next_page')
    return render_template('login.html', next_page=next)


@app.route('/authenticate', methods=['POST',])
def autenticar():

    next_page = request.form['next_page']
    usuario = usuario_dao.buscar_por_id(request.form['id'])

    if usuario:

        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.nome
            session['grupo'] = usuario.grupo
            flash('Bem Vindo, ' + session['usuario_logado'] + '!')

            return redirect(next_page)

        else:
            flash('Senha Inválida! Tente novamente')

            return redirect(url_for('login', next_page=next_page))

    else:
        flash('Usuário ou Senha inválidos! Tente novamente')

        return redirect(url_for('login', next_page=next_page))


@app.route('/logout')
def logout():
    flash('Usuário ' + session['usuario_logado'] + ' Deslogado!')
    session.clear()

    return redirect(url_for('login'))


@app.route('/signup_user')
def cadastrar_usuario():

    return render_template('cadastrar_usuario.html', titulo='Cadastre o Usuário!')


@app.route('/create_user', methods=['POST',])
def criar_usuario():

    id = request.form['id']
    nome = request.form['nome']
    senha = request.form['senha']
    grupo = request.form['grupo']

    usuario = Usuario(id, nome, senha, grupo)

    usuario_dao.cadastrar_usuario(usuario)

    return redirect(url_for('listar_usuario'))


@app.route('/list_user')
def listar_usuario():

    return render_template('lista_usuario.html', usuarios=usuario_dao.listar())

@app.route('/del_user')
def deletar_usuario():

    id = request.args.get('id')
    usuario_dao.deletar(id)

    return redirect(url_for('listar_usuario'))

@app.route('/update_user')
def update_user():
     pass

# HOME
@app.route('/home')
def home():

    if session['usuario_logado']:
        return render_template('home.html', titulo='Bem Vindo a lista de Jogos!', grupo=session['grupo'])
    else:
        return redirect(url_for('login', next_page=url_for('home')))

# JOGO
@app.route('/list_game')
def listar_jogo():

    if session['usuario_logado']:
        return render_template('lista.html', titulo='Jogos', jogos=jogo_dao.listar())
    else:
        return redirect(url_for('login', next_page=url_for('listar_jogo')))


@app.route('/signup_game')
def cadastrar_jogo():

    if session['usuario_logado']:
        return render_template('cadastrar_jogo.html', titulo='Cadastrar Jogos')
    else:
        return redirect(url_for('login', next_page=url_for('cadastrar_jogo')))


@app.route('/create_game', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']

    jogo = Jogo(nome, categoria, console)
    jogo_dao.salvar(jogo)

    return redirect(url_for('listar_jogo'))


@app.route('/del_game')
def deletar():

    jogo_id = int(request.args.get('id'))
    jogo_dao.deletar(jogo_id)

    return redirect(url_for('listar_jogo'))


@app.route('/update_game')
def update():
    
    pass


if __name__ == '__main__':
    app.run(host='localhost', port=8000, debug=True)
