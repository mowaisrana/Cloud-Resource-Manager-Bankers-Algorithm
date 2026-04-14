# ☁️ Cloud Resource Manager & Banker's Algorithm

*An academic project developed for the Operating Systems course in the BS Computer Science program.*

## 📖 Overview
This repository contains a dual-language implementation of the **Banker's Algorithm**, a core Operating Systems concept used for resource allocation and deadlock avoidance. The project bridges the gap between low-level system understanding and high-level application by simulating cloud infrastructure management.

It includes two distinct implementations:
1. **Cloud Resource Manager (Python):** A graphical user interface (GUI) simulating cloud tenant resource requests, utilizing the Banker's Algorithm to prevent infrastructure deadlocks.
2. **Banker's Algorithm CLI (C):** A low-level, terminal-based implementation focusing on matrix calculations, safe sequence detection, and active deadlock resolution.

---

## 🛠️ Features & Implementation

### 1. Python Cloud Resource Manager (`Cloud-Resource-Manager.py`)
Built with `tkinter` and `threading`, this application provides a visual representation of system states.
* **Manual Mode:** Directly manage up to 10 cloud tenants and 10 resources. Allows for manual resource requests, tenant preemption, and process termination.
* **Automatic Simulation Mode:** Uses multi-threading to simulate real-world, randomized tenant behavior (requesting and releasing resources continuously) while maintaining system safety.
* **Real-Time State Display:** Visually tracks Available, Maximum, Allocation, and Need matrices, updating safe sequences dynamically.

### 2. C CLI Implementation (`Bankers-Algorithm.c`)
A strict, algorithmic implementation of deadlock avoidance designed to run in the terminal.
* **Core Calculations:** Automatically computes the *Need* matrix and evaluates system safety via the *Work* and *Finish* arrays.
* **Safe Sequence Generation:** Identifies and prints the exact execution sequence required to avoid deadlocks.
* **Deadlock Resolution System:** If a request forces an unsafe state, the system triggers a resolution menu allowing the user to:
  * Abort a specific process.
  * Preempt a process (release its resources back to the pool).
  * Restart the sequence.

---

## 💻 Tech Stack
* **Python 3.10:** `tkinter` (GUI), `threading` (Simulation), `time`, `random`
* **C:** Standard GCC libraries (`stdio.h`, `stdbool.h`, `stdlib.h`)

---

## 🚀 How to Run

### Running the Python GUI
Ensure you have Python 3 installed. No external pip packages are required as it uses the standard `tkinter` library.
```bash
# Navigate to the directory
cd OS-Bankers-Algorithm

# Run the script
python Cloud-Resource-Manager.py
```

### Compiling and Running the C Program
Ensure you have a C compiler (like GCC) installed on your system.

```bash
# Navigate to the directory
cd OS-Bankers-Algorithm

# Compile the C file
gcc Bankers-Algorithm.c -o bankers_algo

# Run the executable
# On Windows:
bankers_algo.exe

# On Mac/Linux:
./bankers_algo
```

---

## 👨‍💻 Academic Context & Author
Muhammad Owais
B.S. Computer Science

This project was developed to demonstrate practical competency in handling operating system concurrency, resource allocation graphs, and deadlock avoidance protocols.
