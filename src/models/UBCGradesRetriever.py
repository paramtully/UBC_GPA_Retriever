from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

PATH = f"https://www.google.ca/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwiQurTO8Jr5AhUBCjQIHW1KD60QFnoECAsQAQ&url=https%3A%2F%2Fssc.adm.ubc.ca%2Fsscportal%2Fservlets%2FSRVSSCFramework&usg=AOvVaw0YXKH8AbXZYWNZaZHcB7UH"

class UBCGradeRetriever:
    # EFFECTS: initializes webdriver
    def __init__(self):
        ChromeOptions = Options()
        # Uncomment these lines to enable headless
        ChromeOptions.headless = True
        ChromeOptions.add_argument(f"user-agent=Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=ChromeOptions)
    
    # MODIFIES: this
    # EFFECTS: Gets grades from ubc's ssc
    def getGrades(self, username, password, session=None):
        if session: session = session.upper()
        result = []

        try:
            self.logInSSC(username, password)
            self.enterGradeSummaryPage()
            self.enterGradeTableFrame()
            if session: self.enterSessionPage(session)
            gradeTable = self.getGradeTable(session)
            self.processGradesTable(gradeTable, result, session)
        except:
            pass
        finally:
            self.driver.quit()
            return result
    
    """  THESE FUNCTIONS ARE HELPERS FOR getGrades AND SHOULD NOT BE CALLED DIRECTLY """

    # MODIFIES: this
    # EFFECTS: Logs into SSC
    def logInSSC(self, username, password):
        self.driver.get(PATH)
        self.driver.find_element(By.ID, "username").send_keys(username)
        self.driver.find_element(By.ID, "password").send_keys(password, Keys.RETURN)
    

    # MODIFIES: 
    # EFFECTS: Enters grade summary page 
    def enterGradeSummaryPage(self):
        element = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Your Grades Summary"))
            )
        element.click()
    
    # MODIFIES: this
    # EFFECTS: Finds and enters virtual frame containing grade table
    def enterGradeTableFrame(self):
        iframe = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.ID, "iframe-main"))
            )
        self.driver.switch_to.frame(iframe)
    
    # MODIFIES:
    # EFFECTS: Finds requested session page
    def enterSessionPage(self, session):
        id = f"#tabs-{ session }"
        self.driver.find_element(By.XPATH, f"//a[@href='{ id }']").click()
    
    # MODIFIES:
    # EFFECTS: Finds grade table
    def getGradeTable(self, session):
        id = f"tabs-{ session }" if session else "allSessionsGrades"
        gradeTable = self.driver.find_element(By.ID, f"{ id }").find_elements(By.XPATH, "//tr[@class='listRow']")
        return gradeTable
    
    # MODIFIES: 
    # EFFECTS: Extract grade info of completed courses in form: (grade, letter grade, credit) 
    #          and adds them to a list
    def processGradesTable(self, gradeTable, result, session):
        infoIndeces = {'grade': 4, 'letterGrade': 5, 'credit': 7} if session else {'grade': 2, 'letterGrade': 3, 'credit': 8}
        for row in gradeTable:
            data = row.find_elements(By.TAG_NAME, "td")
            if data[infoIndeces['grade']].text != data[infoIndeces['letterGrade']].text != data[infoIndeces['credit']].text:
                result.append((data[infoIndeces['grade']].text,
                               data[infoIndeces['letterGrade']].text, 
                               data[infoIndeces['credit']].text))