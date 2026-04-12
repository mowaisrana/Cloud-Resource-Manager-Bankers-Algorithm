#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>

#define MAX_PROCESSES 10
#define MAX_RESOURCES 10

int n, m; // processes and resources
int available[MAX_RESOURCES]; //currently available resources, tracks free resources
int max[MAX_PROCESSES][MAX_RESOURCES]; //max demand of each process
int allocation[MAX_PROCESSES][MAX_RESOURCES]; //currently allocated resources for each process
int need[MAX_PROCESSES][MAX_RESOURCES];  //remaining need (max - allocated) 

/* returns true if safe, fills safeSeq with safe order, returns length of safe sequence in *seqLen, bassically check 
if sytem is safe  
*/
bool isSafe(int safeSeq[], int *seqLen) {
    int work[MAX_RESOURCES]; // work array to track available resources during safety check
    bool finish[MAX_PROCESSES] = { false }; // finish array to track if processes are finished
    for (int i = 0; i < m; i++) work[i] = available[i]; // initialize work with available resources

    *seqLen = 0; // initialize safe sequence length to 0

    while (true) { 
        bool progress = false; // flag to track if any process can proceed in this iteration
        for (int i = 0; i < n; i++) {
            if (!finish[i]) {// if process i is not finished
                bool canProceed = true; // assume process can proceed
                for (int j = 0; j < m; j++) { // check if process i can proceed
                    if (need[i][j] > work[j]) { // if need of process i exceeds available resources
                        canProceed = false; // process cannot proceed
                        break;
                    }
                }
                if (canProceed) { 
                    for (int j = 0; j < m; j++) work[j] += allocation[i][j]; // add allocated resources of process i to work
                    finish[i] = true; // mark process i as finished
                    safeSeq[(*seqLen)++] = i; // add process i to safe sequence
                    progress = true; // mark progress as true since a process was able to proceed
                }
            }
        }
        if (!progress) break; // if no process can proceed, exit the loop
    }

    for (int i = 0; i < n; i++) if (!finish[i]) return false; // if any process is not finished, system is not in a safe state
    return true; 
}

//calculate the need  (max - allocation)
void calculateNeed() {
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++)
            need[i][j] = max[i][j] - allocation[i][j]; // calculate need for each process
}
// print the current system state,  
void printSystemState() {
    printf("\n===== SYSTEM STATE =====\n");
    printf("Available Resources: ");
    for (int i = 0; i < m; i++) printf("%d ", available[i]); // print available resources
    printf("\n\nProcess   Allocation\t  Maximum\t      Need\n");
    for (int i = 0; i < n; i++) { 
        printf("P%d\t", i); // print process ID
        for (int j = 0; j < m; j++) printf("%d ", allocation[i][j]); // print allocation
        printf("\t  "); // spacing for maximum
        for (int j = 0; j < m; j++) printf("%d ", max[i][j]); // print maximum
        printf("\t  ");  
        for (int j = 0; j < m; j++) printf("%d ", need[i][j]); // print need
        printf("\n"); 
    }
    printf("========================\n\n");
}
// requestResources function checks if the request can be granted without leading to an unsafe state
bool requestResources(int pid, int request[]) {
    if (pid < 0 || pid >= n) {  // check if process ID is valid
        printf("Error: Invalid process ID %d.\n", pid); // process ID should be in range [0, n-1]
        return false;
    }

    for (int i = 0; i < m; i++) { // check if request is valid
        if (request[i] < 0) {
            printf("Error: Requested resources cannot be negative.\n");
            return false;
        }
        if (request[i] > need[pid][i]) {
            printf("Error: Process P%d has requested more than its need for resource %d.\n", pid, i);
            return false;
        }
        if (request[i] > available[i]) {
            printf("Error: Not enough available resources for resource %d.\n", i);
            return false;
        }
    }

    // Try allocating requested resources
    for (int i = 0; i < m; i++) {
        available[i] -= request[i]; // reduce available resources
        allocation[pid][i] += request[i]; // allocate resources to process
        need[pid][i] -= request[i]; // reduce the need of the process
    }

    int safeSeq[MAX_PROCESSES]; // array to hold the safe sequence
    int seqLen; // length of the safe sequence
    bool safe = isSafe(safeSeq, &seqLen); // check if the system is in a safe state after allocation

    if (!safe) { // if not safe, rollback the allocation
        for (int i = 0; i < m; i++) {
            available[i] += request[i]; // restore available resources
            allocation[pid][i] -= request[i]; // deallocate resources from process
            need[pid][i] += request[i]; // restore the need of the process
        }
    }
    return safe;
}

void resolveDeadlock();      

// performResourceRequest function allows a process to request resources and checks if the request can be granted safely
void performResourceRequest() { 
    int pid;
    int req[MAX_RESOURCES]; // array to hold requested resources
    printf("Enter process ID to request resources: ");
    if (scanf("%d", &pid) != 1) {       
        printf("Invalid input for process ID.\n");
        while(getchar() != '\n'); // clear input buffer
        return;
    }
    if (pid < 0 || pid >= n) {
        printf("Invalid process ID.\n");
        return;
    }
    printf("Enter requested resources (%d values): ", m);
    for (int i = 0; i < m; i++) {
        if (scanf("%d", &req[i]) != 1) {
            printf("Invalid input for resource request.\n");
            while(getchar() != '\n');// clear input buffer
            return;
        }
        if (req[i] < 0) { // check if requested resources are negative
            printf("Resource request cannot be negative.\n");
            return;
        }
    }

    if (requestResources(pid, req)) {// if request can be granted safely
        printf("Request granted safely.\n");
    } else {
        printf("Request denied. Would lead to unsafe state.\n");
    }
    calculateNeed(); // recalculate need after request
    printSystemState(); // print the current system state
}
// resolveDeadlock function provides options to resolve deadlock situations
void resolveDeadlock() {
    printf("\n\u26A0 Deadlock detected! Choose resolution method:\n");
    printf("1. Abort process\n");
    printf("2. Preempt process\n");
    printf("3. Restart program\n");
    printf("4. Run Banker's Algorithm (resource request)\n");
    printf("5. Exit program\n> ");
    int choice;
    if (scanf("%d", &choice) != 1) { 
        printf("Invalid input.\n");
        while(getchar() != '\n'); // clear input buffer
        return;
    }

    switch (choice) {
        case 1: {
            int pid;
            printf("Enter process ID to abort: ");
            if (scanf("%d", &pid) != 1 || pid < 0 || pid >= n) { 
                printf("Invalid process ID.\n");
                while(getchar() != '\n');
                return;
            }
            for (int j = 0; j < m; j++) {// release resources held by the process
                available[j] += allocation[pid][j]; // add allocated resources back to available
                allocation[pid][j] = 0; // set allocation to zero
                max[pid][j] = 0; // set max to zero
            }
            calculateNeed(); // recalculate need after aborting
            printf("Process P%d aborted.\n", pid);
            break;
        }
        case 2: {
            int pid;
            printf("Enter process ID to preempt: ");
            if (scanf("%d", &pid) != 1 || pid < 0 || pid >= n) {
                printf("Invalid process ID.\n");
                while(getchar() != '\n');
                return;
            }
            for (int j = 0; j < m; j++) {// release resources held by the process
                available[j] += allocation[pid][j]; // add allocated resources back to available
                need[pid][j] += allocation[pid][j]; // restore the need of the process
                allocation[pid][j] = 0; // set allocation to zero
            }
            printf("Process P%d preempted.\n", pid); 
            break;
        }
        case 3:
            printf("Restarting program...\n");
            exit(0);
        case 4:
            performResourceRequest(); // allow user to make a resource request
            break;
        case 5:
            printf("Exiting program...\n");
            exit(0);
        default:
            printf("Invalid option.\n");
    }
    calculateNeed(); // recalculate need after resolution
    printSystemState(); // print the current system state after resolution
}

int main() {
    printf("Enter number of processes (max %d): ", MAX_PROCESSES);  // get number of processes
    if (scanf("%d", &n) != 1 || n <= 0 || n > MAX_PROCESSES) {//number of processes is valid
        printf("Invalid number of processes.\n"); 
        return 1;
    }
    printf("Enter number of resources (max %d): ", MAX_RESOURCES); // get number of resources
    if (scanf("%d", &m) != 1 || m <= 0 || m > MAX_RESOURCES) {// checknumber of resources is valid
        printf("Invalid number of resources.\n");
        return 1;
    }

    printf("Enter available resources (%d values): ", m);// get available resources
    for (int i = 0; i < m; i++) {
        if (scanf("%d", &available[i]) != 1 || available[i] < 0) { // check if input is valid
            printf("Invalid input for available resources.\n");
            return 1;
        }
    }

    printf("Enter allocation matrix (%d x %d):\n", n, m); // get allocation matrix
    for (int i = 0; i < n; i++) { // get allocation matrix
        printf("Allocation for process P%d: ", i);
        for (int j = 0; j < m; j++) { // get allocation for each resource
            if (scanf("%d", &allocation[i][j]) != 1 || allocation[i][j] < 0) { // check if input is valid
                printf("Invalid allocation input.\n");
                return 1;
            }
        }
    }

    printf("Enter maximum demand matrix (%d x %d):\n", n, m); ///
    for (int i = 0; i < n; i++) {// get maximum demand matrix
        printf("Maximum demand for process P%d: ", i); 
        for (int j = 0; j < m; j++) {
            if (scanf("%d", &max[i][j]) != 1 || max[i][j] < 0) {//
                printf("Invalid max demand input.\n");//
                return 1;
            }
            if (max[i][j] < allocation[i][j]) {// check if max demand is less than allocation
                printf("Max demand can't be less than allocation for process P%d resource %d.\n", i, j);
                return 1;
            }
        }
    }

    calculateNeed();// calculate the need matrix (max - allocation)
    printSystemState();

    int safeSeq[MAX_PROCESSES], seqLen; // array to hold the safe sequence and its length
    bool safe = isSafe(safeSeq, &seqLen); // check if the system is in a safe state

    if (safe) { // if system is in a safe state
        printf("System is in SAFE state.\nSafe sequence is: ");
        for (int i = 0; i < seqLen; i++) {//
            printf("P%d ", safeSeq[i]); // print the safe sequence
        }
        printf("\n");
    } else {
        printf("System is in UNSAFE state. Deadlock likely!\n");
        while (true) {// loop until deadlock is resolved
            resolveDeadlock();

            safe = isSafe(safeSeq, &seqLen); // check if the system is safe after resolution
            if (safe) {// if system is safe after resolution
                printf("System is now in SAFE state.\nSafe sequence is: ");
                for (int i = 0; i < seqLen; i++) {
                    printf("P%d ", safeSeq[i]);
                }
                printf("\n");
                break;  // break out of deadlock resolution loop
            } else {
                printf("System still unsafe after resolution.\n");
            }
        }
    }

    // Allow user to make resource requests or quit
    while (true) {
        printf("\nChoose an option:\n");
        printf("1. Make a resource request\n");
        printf("2. Show current system state\n");
        printf("3. Exit\n> ");
        int option;
        if (scanf("%d", &option) != 1) {
            printf("Invalid input.\n");
            while(getchar() != '\n');//buffer
            continue;// continue to prompt for valid input
        }

        if (option == 1) {
            performResourceRequest();// allow user to make a resource request

            int safeSeq2[MAX_PROCESSES], seqLen2; // array to hold the safe sequence and its length after request
            bool safeNow = isSafe(safeSeq2, &seqLen2); // check if the system is still in a safe state after request
            if (safeNow) {
                printf("System remains in SAFE state.\nSafe sequence: "); // print safe sequence after request
                for (int i = 0; i < seqLen2; i++) {
                    printf("P%d ", safeSeq2[i]); 
                }
                printf("\n");
            } else {
                printf("System moved to UNSAFE state.\n");
                resolveDeadlock(); // resolve deadlock if system is unsafe after request
            }
        } else if (option == 2) {
            printSystemState();
        } else if (option == 3) {
            printf("Exiting program...\n");
            break;
        } else {
            printf("Invalid option.\n");
        }
    }

    return 0;
}
