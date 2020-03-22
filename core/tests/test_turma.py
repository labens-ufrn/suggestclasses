import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from core.bo.turma import get_turno
from django.test import TestCase


class TurmaBOTests(TestCase):

    def test_get_turno(self):
        hm = '246M12'
        ht = '56T12'
        hn = '23N23'

        self.assertEqual('M', get_turno(hm), 'Testando Horário Manhã')
        self.assertEqual('T', get_turno(ht), 'Testando Horário Tarde')
        self.assertEqual('N', get_turno(hn), 'Testando Horário Noite')
        self.assertEqual(None, get_turno('12X56'), 'Testando Horário Errado')
