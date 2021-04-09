from core.bo.requisitos import replace_expressao
from django.test import TestCase


class RequisitoTests(TestCase):

    def test_check_requisitos(self):

        requisito1 = '( ( BSI3102 ) OU ( DCT2305 ) ) E ( ( BSI1107 ) OU ( DCT1107 ) ) '
        requisito2 = '( ( BSI2301 ) OU ( DCT2301 ) ) E ( ( BSI2201 ) OU ( DCT2201 ) ) E ( ( BSI1109 ) OU ( DCT1109 ) ) '
        disciplinas = ['BSI3102', 'DCT1107', 'DCT2201', 'DCT2301']

        print(requisito1)
        req_expression = replace_expressao(requisito1, disciplinas)
        print(req_expression)
        print(eval(req_expression))
        self.assertTrue((eval(req_expression)), 'Requisito1 é atendido!')
        
        print(requisito2)
        req_expression = replace_expressao(requisito2, disciplinas)
        print(req_expression)
        print(eval(req_expression))
        self.assertFalse((eval(req_expression)), 'Requisito2 não é atendido!')
