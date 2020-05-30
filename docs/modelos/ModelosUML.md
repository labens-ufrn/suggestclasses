# Modelos UML

Criamos alguns modelos usando [YUML](http://yuml.me):

## Diagrama de Classe - Votação

![UML Votação de Componentes](https://github.com/labens-ufrn/suggestclasses/blob/master/docs/modelos/votacao.png)

### Código YUML

```
[Votacao]<>-periodo>[PeriodoLetivo|ano;periodo]
[Votacao]<>-curso>[Curso]
[Votacao|id;nome;dt_inicio;dt_fim;num_votos]<>-votos*>[Voto]
[Votacao]++-status>[Status]-[note: PLANEJADA, ATIVA, ENCERRADA]
[Voto]++-discente>[Discente]
[Voto]++-componente>[ComponenteCurricular]
[Voto]++-horarios*>[Horario]
```
Criado com https://yuml.me/

## Diagrama de Classe - Reserva de Salas

![UML Reserva de Salas](modelos/reservas.png)
![UML Reserva de Horário](https://github.com/labens-ufrn/suggestclasses/blob/master/docs/modelos/reservas.png)

Código YUML:

```
[Horario|+dia;+turno;+ordem]-[note: Ex: 24M34{bg:wheat}]
[Sala|+nome:string;sigla:string;+unidade_responsavel]
[Centro]<>-salas*>[Sala]
[TipoAlocação]-[note: Alocação Livre
Alocação por Reserva]
[Prioridade|+curso;+turno]
[Sala]<>-prioridades*>[Prioridade]
[Sala]<>-tipo_alocacao>[TipoAlocação]
[ReservaSala|+tipo;+data_inicio;+data_fim]
[StatusReserva|+situacao;+justificativa]-[note: Recusada
Autorizada]
[ReservaSala]<>-status>[StatusReserva]
[ReservaSala]<>-tipo>[TipoReserva]-[note: Ensino Semestral
Ensino Ocasional
Evento]
[Sala]<>-reservas>[ReservaSala]
[ReservaSala]<>-horarios>[Horario]
```
