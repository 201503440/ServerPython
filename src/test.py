from main import app
import unittest
import json

class FlaskTestCase(unittest.TestCase):

    #Prueba unitaria metodo main
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(b'{"Python_Server_Main":"Grupo 3"}\n', response.data)

    #Prueba unitaria login con usuario que existe
    def test_index2(self):
        tester = app.test_client(self)
        info = {'email': 'esperancito@gmail.com', 'password': 'esperancito'}
        resp = tester.post('/login', data=json.dumps(info), headers={'Content-Type': 'application/json'})
        self.assertEqual(resp.status_code, 200)
    
    def test_index3(self):
        tester = app.test_client(self)
        info = {'nombre_empresa': '', 'direccion': 'Direccion 1', 'nombres': 'Esperancito', 'apellidos': 'Limonada', 'email': 'esperancito@gmail.com', 'celular': '1234-1234'}
        resp = tester.post('/update', data=json.dumps(info), headers={'Content-Type': 'application/json'})
        self.assertEqual(resp.status_code, 200)

if __name__ == '__main__':
    unittest.main()