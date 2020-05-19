import django
django.setup()
from django import db
from core.tests.povoar_testes import criar_dados, remover_dados

from core.bo.turma import get_turno, converte_desc_horario, get_turmas, get_sugestao_turmas
from django.test import TestCase
from core.models import Horario, EstruturaCurricular


class TurmaBOTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print('\nTurmaBOTests')
        print(db.connections.databases)
        criar_dados()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        remover_dados()

    def test_get_turno(self):
        hm = '246M12'
        ht = '56T12'
        hn = '23N23'

        self.assertEqual('M', get_turno(hm), 'Testando Horário Manhã')
        self.assertEqual('T', get_turno(ht), 'Testando Horário Tarde')
        self.assertEqual('N', get_turno(hn), 'Testando Horário Noite')
        self.assertEqual(None, get_turno('12X56'), 'Testando Horário Errado')

    def test_converte_desc_horario(self):
        hm = '246M12'
        hm_list = [Horario(dia='2', turno='M', ordem='1'), Horario(dia='2', turno='M', ordem='2'),
                   Horario(dia='4', turno='M', ordem='1'), Horario(dia='4', turno='M', ordem='2'),
                   Horario(dia='6', turno='M', ordem='1'), Horario(dia='6', turno='M', ordem='2')]
        ht = '56T12'
        ht_list = [Horario(dia='5', turno='T', ordem='1'), Horario(dia='5', turno='T', ordem='2'),
                   Horario(dia='6', turno='T', ordem='1'), Horario(dia='6', turno='T', ordem='2')]
        hn = '23N23'
        hn_list = [Horario(dia='2', turno='N', ordem='2'), Horario(dia='2', turno='N', ordem='3'),
                   Horario(dia='3', turno='N', ordem='2'), Horario(dia='3', turno='N', ordem='3')]
        htt = '24T34 5T12'
        htt_list = [Horario(dia='2', turno='T', ordem='3'), Horario(dia='2', turno='T', ordem='4'),
                    Horario(dia='4', turno='T', ordem='3'), Horario(dia='4', turno='T', ordem='4'),
                    Horario(dia='5', turno='T', ordem='1'), Horario(dia='5', turno='T', ordem='2')]
        httt = '2T34 5T12 6T56'
        httt_list = [Horario(dia='2', turno='T', ordem='3'), Horario(dia='2', turno='T', ordem='4'),
                     Horario(dia='5', turno='T', ordem='1'), Horario(dia='5', turno='T', ordem='2'),
                     Horario(dia='6', turno='T', ordem='5'), Horario(dia='6', turno='T', ordem='6')]
        hmm = '3M23456'
        hmm_list = [Horario(dia='3', turno='M', ordem='2'), Horario(dia='3', turno='M', ordem='3'),
                    Horario(dia='3', turno='M', ordem='4'), Horario(dia='3', turno='M', ordem='5'),
                    Horario(dia='3', turno='M', ordem='6')]
        hmtn = '2M34 5T12 6N34'
        hmtn_list = [Horario(dia='2', turno='M', ordem='3'), Horario(dia='2', turno='M', ordem='4'),
                     Horario(dia='5', turno='T', ordem='1'), Horario(dia='5', turno='T', ordem='2'),
                     Horario(dia='6', turno='N', ordem='3'), Horario(dia='6', turno='N', ordem='4')]

        self.assertEqual(6, len(converte_desc_horario(hm)), 'Testando quantidade de horários: ' + hm)
        self.assertEqual(hm_list, converte_desc_horario(hm), 'Testando horários: ' + hm)
        self.assertEqual(4, len(converte_desc_horario(ht)), 'Testando quantidade de horários: ' + ht)
        self.assertEqual(ht_list, converte_desc_horario(ht), 'Testando horários: ' + ht)
        self.assertEqual(4, len(converte_desc_horario(hn)), 'Testando quantidade de horários: ' + hn)
        self.assertEqual(hn_list, converte_desc_horario(hn), 'Testando horários: ' + hn)
        self.assertEqual(6, len(converte_desc_horario(htt)), 'Testando quantidade de horários: ' + htt)
        self.assertEqual(htt_list, converte_desc_horario(htt), 'Testando horários: ' + htt)
        self.assertEqual(6, len(converte_desc_horario(httt)), 'Testando quantidade de horários: ' + httt)
        self.assertEqual(httt_list, converte_desc_horario(httt), 'Testando horários: ' + httt)
        self.assertEqual(5, len(converte_desc_horario(hmm)), 'Testando quantidade de horários: ' + hmm)
        self.assertEqual(hmm_list, converte_desc_horario(hmm), 'Testando horários: ' + hmm)
        self.assertEqual(6, len(converte_desc_horario(hmtn)), 'Testando quantidade de horários: ' + hmtn)
        self.assertEqual(hmtn_list, converte_desc_horario(hmtn), 'Testando horários: ' + hmtn)

    def test_get_turmas(self):
        estrutura = EstruturaCurricular.objects.get(id_curriculo=999999999)
        semestre = 1
        turmas = get_turmas(estrutura, semestre, 2020, 1)

        self.assertEqual(2, len(turmas), 'Testando Quantidade de Turma - 1º Semestre')
        self.assertEqual('DCT9999', turmas[0].componente.codigo, 'Testando Código do Componente de Turma')
        self.assertEqual('DCT9998', turmas[1].componente.codigo, 'Testando Código do Componente de Turma')

        semestre = 2
        turmas = get_turmas(estrutura, semestre, 2020, 1)
        self.assertEqual(2, len(turmas), 'Testando Quantidade de Turma - 2º Semestre')
        self.assertEqual('DCT9997', turmas[0].componente.codigo, 'Testando Código do Componente de Turma')
        self.assertEqual('DCT9997', turmas[1].componente.codigo, 'Testando Código do Componente de Turma')

    def test_get_sugestao_turmas(self):
        estrutura = EstruturaCurricular.objects.get(id_curriculo=999999999)
        semestre = 1
        turmas = get_sugestao_turmas(estrutura, semestre, 2020, 2)

        self.assertEqual(3, len(turmas), 'Testando Quantidade de Sugestões de Turma - 1º Semestre')
        self.assertEqual('DCT9999', turmas[0].componente.codigo, 'Testando Código do Componente de Turma')
        self.assertEqual('DCT9999', turmas[1].componente.codigo, 'Testando Código do Componente de Turma')
        self.assertEqual('DCT9998', turmas[2].componente.codigo, 'Testando Código do Componente de Turma')

        semestre = 2
        turmas = get_sugestao_turmas(estrutura, semestre, 2020, 2)
        self.assertEqual(2, len(turmas), 'Testando Quantidade de Sugestões de Turma - 2º Semestre')
        self.assertEqual('DCT9997', turmas[0].componente.codigo, 'Testando Código do Componente de Turma')
        self.assertEqual('DCT9997', turmas[1].componente.codigo, 'Testando Código do Componente de Turma')
