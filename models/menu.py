# -*- coding: utf-8 -*-


## Customizando o menu da aplicacao e alguns nomes interessantes

response.title = request.application
response.subtitle = T('Aplicativo para o LEC')

#http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'you'
response.meta.description = 'Programa de alocacao de disciplinas no laboratorio de computacao da UFC'
response.meta.keywords = 'programa, lec, univeridade federal do ceara'
response.meta.generator = 'Framework utlizado - Web2py'
response.meta.copyright = 'Feito por: Francisco Jose Lins Magalhaes e Julia Bessa Braz'


##########################################
## Este é o menu principal da aplicacao
##########################################

response.menu = [
    (T('Home'), False, URL('default','index'), [])
    ]


response.menu+=[
    (T('Disciplinas'), False, URL('disciplinas', 'index'),
     [
            (T('Inserir'),False,URL('disciplinas', 'incluir')),
            (T('Listar'),False,URL('disciplinas', 'listar')),
            (T('Localizar'),False,URL('disciplinas', 'localizar')),
            ]
   )]

response.menu+=[
    (T('Horario'), False, URL('alocarHorario', 'index'),
     [
            (T('Alocar'), False,URL('alocarHorario', 'alocar')),
            (T('Horarios Disponiveis'), False,URL('alocarHorario', 'disponiveis')),
            (T('Horarios Alocados'), False,URL('alocarHorario', 'listar')),
            ]
   )]

#Adicionando o periodo letivo
response.menu+=[
    (T('Periodo'), False, URL('periodo', 'index'),
     [
            (T('Inserir'), False,URL('periodo', 'inserir')),
            (T('Listar'), False,URL('periodo', 'listar')),
            (T('Localizar'), False,URL('periodo', 'localizar')),
            ]
   )]