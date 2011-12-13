from lxml.html import submit_form
def index():
    redirect(URL(r=request,f="listar"))

def inserir():
    periodoform = SQLFORM(db.diasletivos)
    if periodoform.accepts(request.vars,session):
        response.flash = "Período inserido"
    elif periodoform.errors:
       response.flash = 'Houve algum problema'
    return dict(periodoform=periodoform)

def alterar():
    periodoid = request.args(0)
    periodo = db(db.diasletivos.id == periodoid).select()[0]
    editform = SQLFORM(db.diasletivos, periodo, deletable=True)
    if editform.accepts(request.vars, session):
        session.flash = "Período Alterado"
        redirect(URL(r=request,f = "listar",args=periodoid))
    return dict(editform=editform, periodo=periodo)

def listar():
    query = request.vars.query
    registros = db(query).select(db.diasletivos.ALL)
    return dict(registros=registros)

def localizar():
    form, rows=crud.search(db.disciplinas)
    return dict(form=form, rows=rows)

def visualizar():
    periodoid = request.args(0)
    periodo = db(db.diasletivos.id == periodoid).select()[0]
    return dict(periodo=periodo)
