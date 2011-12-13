
def index():
    redirect(URL(r=request,f="listar"))
    

def alocar():
    horarioform = SQLFORM(db.horariosocupados,submit_button = T('Alocar Horário'))
    if horarioform.accepts(request.vars, session):
        session.flash = "Horário Alocado com sucesso"
        redirect(URL(r=request, f="visualizar", args=horarioform.vars.id))
    return dict(horarioform=horarioform)

def alterar():
    horariosocupadosid = request.args(0)
    horariosocupados = db(db.horariosocupados.id == horariosocupadosid).select()[0]
    editform = SQLFORM(db.horariosocupados, horariosocupados, deletable=True, submit_button = T('Submeter'))
    if editform.accepts(request.vars, session):
        redirect(URL(r=request,f = "visualizar",args=horariosocupadosid))
    return dict(editform=editform, horariosocupados=horariosocupados)

#Metodo que ira retornar para a visao os horarios que podem ser colocados
#Eh feita uma consulta na tabela horarios ocupados, pegando somente os que estoa desocupados
def listar():
    query = request.vars.query
    registros = db(query).select(db.horariosocupados.ALL)
    #semelhante a linhas = db.executesql('SELECT * from horariosocupados')
    return dict(registros=registros)

def disponiveis():
    
    form = SQLFORM(db.calendario,fields=['data','hora'],submit_button='Verificar! :-)',writable=False,record=None)
    if form.accepts(request.vars,session,dbio=False):
        redirect(URL('alocarHorario','verificarHorarioDisponivel',vars=dict(data=form.vars.data,hora=form.vars.hora)))
    
    return dict(msg="Horários Disponíveis", form=form)

#Desaloca um horario somente e este eh fixo
def desalocarHorarioFixo():
    data = request.vars.data
    hora = request.vars.hora
    disciplina = request.vars.disciplina
    
    sql = 'SELECT liberar_horario_fixo('+data+','+hora+','+disciplina+');'
    linhas = db.executesql(sql)
    return dict(msg="HorarioDesalocado")

#Desaloca um horario nao fixo ou todo um agendamento fixo
def desalocarHorarioNaoFixo():
    idHorario = request.vars.idHorario
    sql = 'delete from horariosocupados where id='+idHorario+';'
    
    retorno = db.executesql(sql)
    session.flash = "Desalocado"
    return redirect(URL('alocarHorario','listar'))
    
    #redirect(URL('alocarHorario','listar'))


def verificarHorarioDisponivel():
    #Pegando variaveis da requisicao
    data = request.vars.data #tipo timestamp
    hora = request.vars.hora #tipo inteiro de acordo com as horas que existem
    sql = "SELECT disciplina from calendario where hora ="+hora+"and data="+"'"+data+"'"+';'
    consulta = db.executesql(sql)
    
    return dict(horarios = response.json(consulta))

def visualizar():
    horarioid = request.args(0)
    horario = db(db.horariosocupados.id == horarioid).select()[0]
    return dict(horario=horario)