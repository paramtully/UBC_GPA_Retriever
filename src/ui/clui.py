from ..models.GPACalculator import GPACalculator

# NOTE: to run, go to 1 up from UBCGPACalculator and enter into the command line:   
#           python3 -m UBCGPACalculator.ui.gpacalc 
# to run the app

print("Welcome to UBC GPA Calculator!")
print("This application only works for UBC Students.")
print("NOTE: Once your login is entered, it will open chrome locally find your grades!")
username = input("Input CWL ID: ")
password = input("Input CWL Password: ")
session = input("Input Session (ex in form 2022W or 2022S) or leave blank to for overall GPA: ")
if len(session) != 5: session = None
summary = GPACalculator().getSummary(username, password, session)
if summary: 
    print("Your Grade Summary:")
    print(f"Average:            {summary[0]}")
    print(f"GPA (4.0 Scale):    {summary[1]} / 4.0")
    print(f"GPA (4.33 Scale):   {summary[2]} / 4.33")
else: 
    print("No results were found")
    print("Either no courses were completed during the requested session or your login credentials were incorrect")



