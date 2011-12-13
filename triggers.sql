-- Function: verificar_data()
-- Essa funcao eh associada a um trigger

CREATE OR REPLACE FUNCTION verificar_data()
  RETURNS trigger AS
$BODY$
declare
	dia date;
	hora integer;
	dia_semana integer;
	ano integer;

begin
	dia = new.data;
	hora = new.hora;
	select date_part('dow', dia) into dia_semana;
	select date_part('year', dia) into ano;
	
	--Verificando se existe uma disciplina no mesmo horario e data da que queremos inserir
	if ((select c.disciplina from calendario c where c.data = dia and c.hora = hora) is not null) then
		raise exception 'Horario indisponivel.';
	end if;
	
	if(new.fixo = 'T') then
	
		--Verificando se algum dos horarios já está ocupado 
		if (exists(select disciplina from calendario d where (date_part('dow', d.data)) = dia_semana and
		d.hora = hora and disciplina in (select id from disciplinas) and data >= new.data and
							data <= (select fim from diasletivos
								where semestre = new.semestre
								and date_part('year', fim) = ano))) then
		
			raise exception 'Impossivel alocar. Um ou mais horarios ocupados.';
		else
			update calendario set disciplina = new.disciplina		 
			where  date_part('dow', data) =
			 dia_semana and calendario.hora = hora;
			 
		end if;
		 
	--Se ele nao for um dia fixo, entao coloca em somente um horario
	else
		update calendario set disciplina = new.disciplina
		where calendario.data = dia and calendario.hora = hora;
		
	end if;

	return new;
end;
$BODY$
  LANGUAGE 'plpgsql'
  
  
create trigger t2
before insert or update on horariosocupados
for each row execute procedure verificar_data();


-- Function: desalocar_horario()
-- Essa funcao eh associada a um trigger

CREATE OR REPLACE FUNCTION desalocar_horario()
  RETURNS trigger AS
$BODY$
declare
	dia date;
	hora integer;
	dia_semana integer;
	ano integer;

begin
	dia = old.data;
	hora = old.hora;
	select date_part('dow', dia) into dia_semana;
	select date_part('year', dia) into ano;
	
	if(old.fixo = 'T') then
		update calendario set disciplina = null
		where  (date_part('dow', data)) = dia_semana
		and calendario.hora = hora and data <= 
		(select fim from diasletivos d where d.semestre = old.semestre
			and date_part('year',fim) = ano );
	--Se ele nao for um dia fixo, entao desaloca somente um horario
	else
		update calendario set disciplina = null
		where calendario.data = dia and calendario.hora = hora;
		
	end if;

	return new;
end;
$BODY$
  LANGUAGE 'plpgsql'
  
create trigger desalocar
after delete on horariosocupados
for each row execute procedure desalocar_horario();


-- Function: addanoletivo()
--Essa funcao eh associada a um trigger

CREATE OR REPLACE FUNCTION addanoletivo()
  RETURNS trigger AS
$BODY$
declare
	i date;
	d_inicio date;
	d_fim date;
	j integer;
begin

    d_inicio = new.inicio;
    d_fim = new.fim;
    i = d_inicio;

    while i <= d_fim loop
		for j in 1..5 loop
	    	insert into calendario (hora, data) values (j, i);
		end loop;
	
        i = i + interval '1 day';
                
    end loop;

    return null;
end;
$BODY$
  LANGUAGE 'plpgsql';
  
create trigger t_inserirLetivos
after insert on diasletivos
for each row execute procedure addAnoLetivo();


-- Function: liberar_horario_fixo(date, integer, integer)

CREATE OR REPLACE FUNCTION liberar_horario_fixo(ddia date, dhora integer, ddisciplina integer)
  RETURNS void AS
$BODY$

begin
	update calendario c set disciplina = null
	where data = ddia and hora = dhora and disciplina = ddisciplina;

	return;
end;
$BODY$
  LANGUAGE 'plpgsql';

