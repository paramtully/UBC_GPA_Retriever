from .UBCGradesRetriever import UBCGradeRetriever

class GPACalculator:
    # EFFECTS: initializes this object with grade retrieving tool
    #          and letter grade to grade point maps
    def __init__(self):
        self.gradeRetreiver = UBCGradeRetriever()
        self.letterGradeToCreditTable4 = {'A+': 4, 'A': 4, 'A-': 3.7, 'B+': 3.3, 'B': 3, 'B-': 2.7, 'C+': 2.3, 'C': 2, 'C-': 1.7, 'D+': 1.3, 'D': 1, 'F': 0}
        self.letterGradeToCreditTable433 = {'A+': 4.33, 'A': 4, 'A-': 3.67, 'B+': 3.33, 'B': 3, 'B-': 2.67, 'C+': 2.33, 'C': 2, 'C-': 1.67, 'D+': 1.33, 'D': 1, 'F': 0}
    
    # MODIFIES: this
    # EFFECTS: Returns summary in form (average, GPA on 4.0 scale, GPA on 4.33 scale)
    #          or None if no grades are found
    def getSummary(self, username, password, session=None):
        grades = self.gradeRetreiver.getGrades(username, password, session)
        if not len(grades): return None
        return (self.calculateAverage(grades), self.calculateGPA(grades), self.calculateGPA(grades, False))
    
    """  THESE FUNCTIONS ARE HELPERS FOR getSummary AND SHOULD NOT BE CALLED DIRECTLY  """
    
    # REQUIRES: grades is not empty
    # MODIFIES:
    # EFFECTS: Calculates GPA on 4.0 scale when is4 is set to true, and 4.33 scale otherwise.
    #          Defaults to 4.0 scale if is4 is not set
    def calculateGPA(self, grades, is4=True):
        totalWeightedGPs, totalCredits = 0, 0
        for grade in grades:
            weightedGradePoint = (self.letterGradeToCreditTable4[grade[1]] if is4 else self.letterGradeToCreditTable433[grade[1]]) * int(float(grade[2]))
            totalWeightedGPs += weightedGradePoint
            totalCredits += int(float(grade[2]))
        return round(totalWeightedGPs / totalCredits, 2)

    # REQUIRES: grades is not empty
    # MODIFIES: 
    # EFFECTS: calculates average grade in percent format
    def calculateAverage(self, grades):
        totalWeightedGrade, totalCredits = 0, 0
        for grade in grades:
            totalWeightedGrade += int(grade[0]) * int(float(grade[2]))
            totalCredits += int(float(grade[2]))
        return round(totalWeightedGrade / totalCredits, 2)

