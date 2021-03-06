# -*- coding: utf-8 -*-
# Este arquivo é referente ao banco de dados.
#Aqui definimos as tabelas e as relações entre elas

#Conectando com o banco de dados
db = DAL('postgres://postgres:postgres@localhost/lec')

# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []

from gluon.tools import Crud, Service
#mail = Mail()                                  # mailer
#auth = Auth(db)                                # authentication/authorization
crud = Crud(db)                                # for CRUD helpers using auth
service = Service()                            # for json, xml, jsonrpc, xmlrpc, amfrpc
                # for configuring plugins

#Validadores Personalizados
IS_IN_DB_MSG = error_message = T('Este campo é obrigatório')
IS_NOT_EMPTY_MSG = error_message = T('Este campo é obrigatório')
H_IS_NOT_EMPTY = IS_NOT_EMPTY(error_message = IS_NOT_EMPTY_MSG)

##Definindo as tabelas que estamos utilizando

#Tabela de disciplinas. 
db.define_table('disciplinas',
                Field('codigo',requires=H_IS_NOT_EMPTY),
                Field('nome',requires=H_IS_NOT_EMPTY),
                format='%(nome)s')

#Tabelas com as horas disponiveis, o usuario podera inserir uma hora
db.define_table('horas',
                Field('intervalo'),
                format='%(intervalo)s')

#Tabela com todos os horarios do semestre
db.define_table('calendario',
                Field('disciplina', db.disciplinas, requires = IS_IN_DB(db,db.disciplinas,db.disciplinas._format,error_message=IS_IN_DB_MSG)),
                Field('data','date'),
                Field('hora',db.horas,requires = IS_IN_DB(db,db.horas,db.horas._format,error_message=IS_IN_DB_MSG))
                )

#Tabela de horarios ocupados
db.define_table('horariosocupados',
                Field('disciplina', db.disciplinas, label=T('Disciplina'),
                      requires=IS_IN_DB(db, db.disciplinas, db.disciplinas._format, error_message=IS_IN_DB_MSG)),
                Field('data','date',label=T('Data')),
                Field('hora',db.horas,requires = IS_IN_DB(db,db.horas,db.horas._format,error_message=IS_IN_DB_MSG)),
                Field('semestre','integer',requires=IS_IN_SET(['1', '2'])),
                Field('fixo','boolean')
                )
#Tabela para inserir um novo semestre letivo
db.define_table('diasletivos',
                Field('semestre','integer', requires=H_IS_NOT_EMPTY),
                Field('inicio','date',requires=H_IS_NOT_EMPTY),
                Field('fim','date',requires=H_IS_NOT_EMPTY)
                )
