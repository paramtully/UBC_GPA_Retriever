import sys
from ..models.GPACalculator import GPACalculator

n = len(sys.argv)
if n < 4 and n > 5: print("Inavlid number of arguments...")
else:
    username = sys.argv[1]
    password = sys.argv[2]
    summary = GPACalculator().getSummary(sys.argv[1], sys.argv[2], sys.argv[3] if n == 4 else None)

    if summary: 
        print("Your Grade Summary:")
        print(f"Average:            {summary[0]}")
        print(f"GPA (4.0 Scale):    {summary[1]} / 4.0")
        print(f"GPA (4.33 Scale):   {summary[2]} / 4.33")
    else: 
        print("No results were found")
        print("Either no courses were completed during the requested session or your login credentials were incorrect")

