#Controlador das disciplinas

def index():
    redirect(URL(r=request,f="listar"))
    
def incluir():
    disciplinaform = SQLFORM(db.disciplinas,submit_button="Inserir Disciplina")
    if disciplinaform.accepts(request.vars, session):
        session.flash = "Disciplina Inserida!"
        redirect(URL(r=request, f="visualizar", args=disciplinaform.vars.id))
    return dict(disciplinaform=disciplinaform)

def visualizar():
    disciplinaid = request.args(0)
    disciplina = db(db.disciplinas.id == disciplinaid).select()[0]
    return dict(disciplina=disciplina)

def localizar():
    form, rows=crud.search(db.disciplinas)
    return dict(form=form, rows=rows)

def listar():
    query = request.vars.query
    registros = db(query).select(db.disciplinas.ALL)
    return dict(registros=registros)

def alterar():
    disciplinaid = request.args(0)
    disciplina = db(db.disciplinas.id == disciplinaid).select()[0]
    editform = SQLFORM(db.disciplinas, disciplina, deletable=True)
    if editform.accepts(request.vars, session):
        redirect(URL(r=request,f = "listar",args=disciplinaid))
    return dict(editform=editform, disciplina=disciplina)