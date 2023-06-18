from django.test import TestCase
from django.test import TransactionTestCase


# Create your tests here.

class TestDBexists(TestCase):
    def setUp(self):
        pass

    def test_NumberDBTables(self):
        """The SQLite DB has the correct number of tables"""
        from django.db import connection
        self.assertTrue(
            len(connection.introspection.table_names()) >= 11)
        

class TestDBpredtable(TestCase):

    def setUp(self):
        from cantinedata.models import Prediction
        import datetime
    
        str2datetime = lambda string1 :datetime.datetime.strptime(string1,"%Y-%m-%d").date()
                
        Prediction.objects.create(date=str2datetime('2011-01-03'), total_modele=10000)
        Prediction.objects.create(date=str2datetime('2011-01-04'), total_modele=11000)


    def test_PredObjects(self):
        """Prediction objects are queried correctly"""
        from cantinedata.models import Prediction
        import datetime
        str2datetime = lambda string1 :datetime.datetime.strptime(string1,"%Y-%m-%d").date()
        
        pred1 = Prediction.objects.get(total_modele=10000)
        pred2 = Prediction.objects.get(total_modele=11000)
        self.assertTrue(pred1.date>=str2datetime('2011-01-01'))
        self.assertTrue(pred2.date>=str2datetime('2011-01-0'))
        
class TestHomePage(TransactionTestCase):
    def setUp(self):
        pass

    def test_Route200(self):
        """The Homepage sends back a 200 response"""
        from rest_framework import status
        from django.test import Client
        
        client=Client()
        response = client.get(
            'http://127.0.0.1:8000/cantinedata/prediction/?date=2011-01-03',
            follow=True
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class TestPredictAPI(TransactionTestCase):
    def setUp(self):
        pass

    def test_APIRoute(self):
        """The Predict API send back a reasonnable number"""
        from rest_framework import status
        from django.test import Client
        
        client=Client(SERVER_NAME='localhost')
        response = client.get(
            'http://127.0.0.1:8000/cantinedata/prediction/?date=2011-01-03'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(int(response.getvalue())>1000)

