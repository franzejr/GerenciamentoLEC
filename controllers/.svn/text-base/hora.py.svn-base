def index():
    redirect(URL(r=request,f="listar"))

def inserir():
    horaform = SQLFORM(db.horas)
    if horaform.accepts(request.vars, session):
       redirect(URL(r=request, f="visualizar", args=horaform.vars.id))
    return dict(horaform=horaform)

def alterar():
    horaid = request.args(0)
    hora = db(db.horas.id == horaid).select()[0]
    editform = SQLFORM(db.horas, hora, deletable=True)
    if editform.accepts(request.vars, session):
        redirect(URL(r=request,f = "visualizar",args=horaid))
    return dict(editform=editform, hora=hora)

def listar():
    query = request.vars.query
    registros = db(query).select(db.horas.ALL)
    return dict(registros=registros)

def visualizar():
    horaid = request.args(0)
    hora = db(db.horas.id == horaid).select()[0]
    return dict(hora=hora)