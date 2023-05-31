import unittest
from ..models.GPACalculator import GPACalculator
from dotenv import load_dotenv
import os

# NOTE:  In order to run test, go 1 up from top level module (UBCGPACalculator)
#        Then input: python3 -m UBCGPAcalculator.tests.testGPACalculator

class TestGPACalculator(unittest.TestCase):
    def setUp(self) -> None:
        load_dotenv()
        self.calculator = GPACalculator()
        self.username = os.getenv("DEFAULT_USERNAME")
        self.password = os.getenv("DEFAULT_PASSWORD")
    
    def testValidLoginAllSessions(self):
        self.assertEqual(GPACalculator().getSummary(self.username, self.password), (82.48, 3.63, 3.62))
    
    def testValidLoginIncompleteSession(self):
        self.assertIsNone(GPACalculator().getSummary(self.username, self.password, "3021W"))
    
    def testValidLoginValidCompleteSession(self):
        self.assertEqual(GPACalculator().getSummary(self.username, self.password, "2021W"), (82.48, 3.63, 3.62))
    
    def testInvalidLogin(self):
        self.assertIsNone(GPACalculator().getSummary("john", "doe", "2021W"))
    
    def testValidLoginInvalidSession(self):
        self.assertIsNone(GPACalculator().getSummary(self.username, self.password, "2023W"))

if __name__ == '__main__':
    unittest.main()