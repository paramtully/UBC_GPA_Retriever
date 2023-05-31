
#include<stdio.h>
#include<unistd.h>
#include<string.h>
#include<stdlib.h>

/* RUNS COMMAND LINE PROGRAM
    - 2 args: username, password with all sems
    - 3 args: specified account with username, password, and specified sem
    - Note: above args dont include './runapp' itself
*/
int main(int argc, char* argv[]) {
    if (argc > 3 || argc <= 2) fprintf(stderr, "Too many arguments given\n");


    // set up args
    char *args[7] = {"python3", "-m", "UBCGPACalculator.ui.calc", NULL, NULL, NULL, NULL};
    
    if (argc == 3 || argc == 4) {
        args[3] = argv[1];
        args[4] = argv[2];
    }
    if (argc == 4) args[5] = argv[3];

    // exec call
    execvp(args[0], args);
    fprintf(stderr, "Program failed to run\n");
    return -1;
}