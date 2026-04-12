import tkinter as tk #gui
from tkinter import messagebox, simpledialog, scrolledtext, ttk #gui
from tkinter.font import Font #gui
import random #random num for automatic mode
import threading 
import time #add delay like sleep()

MAX_PROCESSES = 10
MAX_RESOURCES = 10
AUTO_PROCESSES = 5  # Fixed for automatic mode
AUTO_RESOURCES = 3  # Fixed for automatic mode

class BankersAlgorithmGUI:
    def __init__(self, root): #Matrix Initialization
        self.root = root
        self.root.title("☁️ Cloud Resource Manager - Banker's Algorithm")
        self.root.geometry("1000x800")
        self.root.configure(bg="#f1e0fd")
        
        # Color scheme
        self.colors = {
            'bg': "#f1e0fd",
            'header': "#2a0061",
            'safe': '#4CAF50',
            'unsafe': '#F44336',
            'button': "#350053",
            'highlight': "#C99300",
            'text': '#212121',
            'disabled': '#9E9E9E',
            'mode1': "#3E0070",
            'mode2': "#004E11"
        }
        
        # Custom fonts
        self.bold_font = Font(family="Segoe UI", size=10)
        self.title_font = Font(family="Segoe UI", size=12, weight="bold")
        self.large_font = Font(family="Segoe UI", size=14, weight="bold")
        
        # Initialize variables
        self.n = 0
        self.m = 0
        self.available = [0] * MAX_RESOURCES
        self.max = [[0] * MAX_RESOURCES for _ in range(MAX_PROCESSES)]
        self.allocation = [[0] * MAX_RESOURCES for _ in range(MAX_PROCESSES)]
        self.need = [[0] * MAX_RESOURCES for _ in range(MAX_PROCESSES)]
        self.running = False
        self.simulation_thread = None
        
        # Create mode selection screen
        self.create_mode_selection()

    def create_mode_selection(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Header
        header_frame = tk.Frame(self.root, bg=self.colors['header'])
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        header_label = tk.Label(
            header_frame, 
            text="☁️ Cloud Resource Manager",
            font=self.large_font,
            bg=self.colors['header'],
            fg='white',
            padx=10,
            pady=20
        )
        header_label.pack()
        
        # Main content frame
        content_frame = tk.Frame(self.root, bg=self.colors['bg'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=20)
        
        # Mode 1 button
        mode1_btn = tk.Button(
            content_frame,
            text=" 🛠️ Manual Resource Management\n\nDirectly manage tenant resource allocations",
            font=self.title_font,
            bg=self.colors['mode1'],
            fg='white',
            activebackground=self.colors['highlight'],
            bd=0,
            padx=20,
            pady=30,
            width=50,
            command=self.start_interactive_mode
        )
        mode1_btn.pack(pady=(0, 30))
        
        # Mode 2 button
        mode2_btn = tk.Button(
            content_frame,
            text="🤖 Automatic Simulation\n\nSimulate real-world tenant behavior",
            font=self.title_font,
            bg=self.colors['mode2'],
            fg='white',
            activebackground=self.colors['highlight'],
            bd=0,
            padx=20,
            pady=30,
            width=50,
            command=self.start_automatic_mode
        )
        mode2_btn.pack()
        
        # Footer
        footer_frame = tk.Frame(self.root, bg=self.colors['bg'])
        footer_frame.pack(fill=tk.X, pady=(20, 0))
        
        tk.Label(
            footer_frame,
            text="Cloud Infrastructure Safety System - Uses Banker's Algorithm to prevent deadlocks",
            bg=self.colors['bg'],
            fg=self.colors['text'],
            font=('Segoe UI', 8)
        ).pack()

    def create_interactive_mode_gui(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Create menu
        self.create_menu()
        
        # Main frame
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        header_frame = tk.Frame(main_frame, bg=self.colors['mode1'])
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        header_label = tk.Label(
            header_frame, 
            text="🛠️ Manual Resource Management - Banker's Algorithm",
            font=self.title_font,
            bg=self.colors['mode1'],
            fg='white',
            padx=10,
            pady=10
        )
        header_label.pack()
        
        # System state display
        state_frame = tk.LabelFrame(
            main_frame, 
            text=" 📊 System State ",
            font=self.bold_font,
            bg=self.colors['bg'],
            fg=self.colors['text'],
            padx=5,
            pady=5
        )
        state_frame.pack(fill=tk.BOTH, expand=True)
        
        self.system_state_text = scrolledtext.ScrolledText(
            state_frame, 
            wrap=tk.WORD, 
            width=90, 
            height=25, 
            state=tk.DISABLED,
            bg='white',
            fg=self.colors['text'],
            font=('Consolas', 10),
            padx=10,
            pady=10
        )
        self.system_state_text.pack(fill=tk.BOTH, expand=True)
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Action buttons
        button_style = {
            'bg': self.colors['button'],
            'fg': 'white',
            'activebackground': self.colors['highlight'],
            'font': self.bold_font,
            'bd': 0,
            'padx': 10,
            'pady': 5
        }
        
        tk.Button(
            button_frame, 
            text="📝 Make Request", 
            command=self.make_request,
            **button_style
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame, 
            text="❌ Abort Tenant", 
            command=self.abort_process, #process termination
            **button_style
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame, 
            text="⚡ Preempt Tenant", 
            command=self.preempt_process, #process preempt
            **button_style
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame, 
            text="🔄 Refresh", 
            command=self.update_system_state_display, #State Display
            **button_style
        ).pack(side=tk.RIGHT, padx=5)
        
        tk.Button(
            button_frame, 
            text="🔙 Back to Mode Selection", 
            command=self.create_mode_selection,
            bg=self.colors['mode1'],
            fg='white',
            activebackground=self.colors['highlight'],
            font=self.bold_font,
            bd=0,
            padx=10,
            pady=5
        ).pack(side=tk.RIGHT, padx=5)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("🔵 Please initialize the system first.")
        
        status_bar = tk.Label(
            main_frame, 
            textvariable=self.status_var,
            bd=1, 
            relief=tk.SUNKEN, 
            anchor=tk.W,
            bg='white',
            fg=self.colors['text'],
            font=self.bold_font,
            padx=10
        )
        status_bar.pack(fill=tk.X, pady=(10, 0))

    def create_automatic_mode_gui(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main frame
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        header_frame = tk.Frame(main_frame, bg=self.colors['mode2'])
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        header_label = tk.Label(
            header_frame, 
            text="🤖 Automatic Simulation - Banker's Algorithm",
            font=self.title_font,
            bg=self.colors['mode2'],
            fg='white',
            padx=10,
            pady=10
        )
        header_label.pack()
        
        # Control frame
        control_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # System state display
        state_frame = tk.LabelFrame(
            main_frame, 
            text=" 📊 System State ",
            font=self.bold_font,
            bg=self.colors['bg'],
            fg=self.colors['text'],
            padx=5,
            pady=5
        )
        state_frame.pack(fill=tk.BOTH, expand=True)
        
        self.auto_state_text = scrolledtext.ScrolledText(
            state_frame, 
            wrap=tk.WORD, 
            width=100, 
            height=30, 
            state=tk.DISABLED,
            bg='white',
            fg=self.colors['text'],
            font=('Consolas', 10),
            padx=10,
            pady=10
        )
        self.auto_state_text.pack(fill=tk.BOTH, expand=True)
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Action buttons
        self.start_btn = tk.Button(
            button_frame, 
            text="▶️ Start Simulation", 
            command=self.start_automatic_simulation,
            bg=self.colors['mode2'],
            fg='white',
            activebackground=self.colors['highlight'],
            font=self.bold_font,
            bd=0,
            padx=10,
            pady=5
        )
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = tk.Button(
            button_frame, 
            text="⏹️ Stop Simulation", 
            command=self.stop_automatic_simulation,
            bg=self.colors['unsafe'],
            fg='white',
            activebackground=self.colors['highlight'],
            font=self.bold_font,
            bd=0,
            padx=10,
            pady=5,
            state=tk.DISABLED
        )
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame, 
            text="🔄 Change Resources", 
            command=self.ask_for_auto_resources,
            bg=self.colors['button'],
            fg='white',
            activebackground=self.colors['highlight'],
            font=self.bold_font,
            bd=0,
            padx=10,
            pady=5
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame, 
            text="🔙 Back to Mode Selection", 
            command=self.create_mode_selection,
            bg=self.colors['mode1'],
            fg='white',
            activebackground=self.colors['highlight'],
            font=self.bold_font,
            bd=0,
            padx=10,
            pady=5
        ).pack(side=tk.RIGHT, padx=5)
        
        # Status bar
        self.auto_status_var = tk.StringVar()
        self.auto_status_var.set("🔵 Please enter available resources to begin")
        
        status_bar = tk.Label(
            main_frame, 
            textvariable=self.auto_status_var,
            bd=1, 
            relief=tk.SUNKEN, 
            anchor=tk.W,
            bg='white',
            fg=self.colors['text'],
            font=self.bold_font,
            padx=10
        )
        status_bar.pack(fill=tk.X, pady=(10, 0))
        
        # Initialize automatic mode variables
        self.n = AUTO_PROCESSES
        self.m = AUTO_RESOURCES
        self.running = False
        self.simulation_thread = None
        
        # Ask for resources
        self.ask_for_auto_resources()

    def create_menu(self):
        menubar = tk.Menu(self.root, bg=self.colors['bg'], fg=self.colors['text'])
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0, bg=self.colors['bg'], fg=self.colors['text'])
        file_menu.add_command(label="🔄 Initialize System", command=self.initialize_system)
        file_menu.add_separator()
        file_menu.add_command(label="🚪 Exit", command=self.root.quit)
        menubar.add_cascade(label="📁 File", menu=file_menu)
        
        # Actions menu
        actions_menu = tk.Menu(menubar, tearoff=0, bg=self.colors['bg'], fg=self.colors['text'])
        actions_menu.add_command(label="📝 Make Resource Request", command=self.make_request)
        actions_menu.add_command(label="❌ Abort Tenant", command=self.abort_process) #process termination
        actions_menu.add_command(label="⚡ Preempt Tenant", command=self.preempt_process) # process preempt
        menubar.add_cascade(label="⚙️ Actions", menu=actions_menu)
        
        self.root.config(menu=menubar)

    def start_interactive_mode(self):
        self.create_interactive_mode_gui()
        self.initialize_system()

    def start_automatic_mode(self):
        self.create_automatic_mode_gui()

    def ask_for_auto_resources(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("📝 Enter Available Resources")
        dialog.geometry("400x300")
        dialog.configure(bg=self.colors['bg'])
        dialog.resizable(False, False)
        
        # Center the dialog
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'+{x}+{y}')
        
        # Main frame
        main_frame = tk.Frame(dialog, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        tk.Label(
            main_frame, 
            text="Enter Available Resources", 
            font=self.title_font,
            bg=self.colors['bg'],
            fg=self.colors['header']
        ).pack(pady=(0, 20))
        
        # Resource entries
        self.resource_entries = []
        for i in range(self.m):
            frame = tk.Frame(main_frame, bg=self.colors['bg'])
            frame.pack(fill=tk.X, pady=5)
            
            tk.Label(
                frame, 
                text=f"Resource R{i}:",
                bg=self.colors['bg'],
                fg=self.colors['text'],
                width=10
            ).pack(side=tk.LEFT)
            
            entry = ttk.Entry(frame)
            entry.pack(side=tk.RIGHT, fill=tk.X, expand=True)
            self.resource_entries.append(entry)
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        def on_submit():
            try:
                for i in range(self.m):
                    self.available[i] = int(self.resource_entries[i].get())
                    if self.available[i] < 0:
                        raise ValueError("Negative value")
                
                # Initialize maximum and need matrices
                for i in range(self.n):
                    for j in range(self.m):
                        self.max[i][j] = random.randint(1, self.available[j])
                        self.allocation[i][j] = 0
                        self.need[i][j] = self.max[i][j]
                
                dialog.destroy()
                self.start_btn.config(state=tk.NORMAL)
                self.auto_status_var.set("🟢 Ready to start simulation")
                self.update_auto_state_display()
                
            except ValueError:
                messagebox.showerror("Invalid Input", 
                                   "Please enter valid positive integers for all resources.",
                                   parent=dialog)
        
        ttk.Button(
            button_frame, 
            text="Submit", 
            command=on_submit,
            style='Accent.TButton'
        ).pack(side=tk.RIGHT)
        
        # Configure ttk style
        style = ttk.Style()
        style.configure('Accent.TButton', background=self.colors['highlight'], foreground='black')
        
        dialog.transient(self.root)
        dialog.grab_set()
        self.root.wait_window(dialog)

    def start_automatic_simulation(self):
        if not self.running: #flag starts/stops the thread
            self.running = True
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            
            self.auto_status_var.set("🟢 Simulation running...")
            self.update_auto_state_display()
            
            # Start simulation thread , creation ,                 sep thread o  run,      exit,mainexit,
            self.simulation_thread = threading.Thread(target=self.run_automatic_simulation, daemon=True) #automatic simulation thread
            self.simulation_thread.start()

    def stop_automatic_simulation(self):
        if self.running:
            self.running = False
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.auto_status_var.set("🔴 Simulation stopped")

    def run_automatic_simulation(self): #automatic simulation thread
        while self.running: #Loop Control, click stop, start_automatic_simulation()/stop_automatic_simulation()
            time.sleep(2)  # Delay between iterations
            
            # Process a random customer
            customer_id = random.randint(0, self.n - 1)
            
            # Randomly decide to request or release
            if random.random() < 0.7:  # 70% chance to request
                request = [0] * self.m
                for j in range(self.m):
                    if self.need[customer_id][j] > 0:
                        request[j] = random.randint(0, self.need[customer_id][j])
                
                if any(request):  # Only process if there's a real request
                    self.process_auto_request(customer_id, request) #request check
            else:  # 30% chance to release
                release = [0] * self.m
                for j in range(self.m):
                    if self.allocation[customer_id][j] > 0:
                        release[j] = random.randint(0, self.allocation[customer_id][j])
                
                if any(release):  # Only process if there's a real release
                    self.process_auto_release(customer_id, release)
            
            # Update display in main thread
            self.root.after(0, self.update_auto_state_display) #update GUI from the thread

    def process_auto_request(self, customer_id, request): #request check
        self.log_auto_message(f"\n=== Tenant T{customer_id} requesting: {request} ===")
        
        # Check request ≤ need and ≤ available
        valid = True
        for j in range(self.m):
            if request[j] > self.need[customer_id][j]:
                self.log_auto_message(f"❌ Request exceeds need for resource R{j}")
                valid = False
                break
            if request[j] > self.available[j]:
                self.log_auto_message(f"❌ Not enough available resources (R{j})")
                valid = False
                break
        
        if not valid:
            self.log_auto_message("❌ Request denied")
            return False
        
        # Pretend to allocate
        for j in range(self.m):
            self.available[j] -= request[j]
            self.allocation[customer_id][j] += request[j]
            self.need[customer_id][j] -= request[j]
        
        self.log_auto_message("🔄 Temporarily allocating resources...")
        
        if self.is_safe_state():
            self.log_auto_message("✅ Request granted (system is in safe state)") # banker
            return True
        else:
            # Rollback
            for j in range(self.m):
                self.available[j] += request[j]
                self.allocation[customer_id][j] -= request[j]
                self.need[customer_id][j] += request[j]
            self.log_auto_message("❌ Request denied (would lead to unsafe state)")
            return False

    def process_auto_release(self, customer_id, release):
        self.log_auto_message(f"\n=== Tenant T{customer_id} releasing: {release} ===")
        
        for j in range(self.m):
            if release[j] <= self.allocation[customer_id][j]:
                self.allocation[customer_id][j] -= release[j]
                self.available[j] += release[j]
                self.need[customer_id][j] += release[j]
        
        self.log_auto_message("✅ Resources released successfully")

    def log_auto_message(self, message):
        self.auto_state_text.config(state=tk.NORMAL)
        self.auto_state_text.insert(tk.END, f"{message}\n")
        self.auto_state_text.see(tk.END)
        self.auto_state_text.config(state=tk.DISABLED)

    def update_auto_state_display(self):
        self.auto_state_text.config(state=tk.NORMAL)
        self.auto_state_text.insert(tk.END, "\n══════════════════════════════════════════════════\n", 'header')
        self.auto_state_text.insert(tk.END, "🛡️ Current System State\n\n", 'bold')
        
        # Display available resources
        self.auto_state_text.insert(tk.END, "Available Cloud Resources:\n")
        for j in range(self.m):
            self.auto_state_text.insert(tk.END, f"R{j}: {self.available[j]}\t")
        self.auto_state_text.insert(tk.END, "\n\n")
        
        # Display matrices
        self.auto_state_text.insert(tk.END, "Tenants\tAllocation\t\tMaximum\t\tNeed\n", 'bold')
        for i in range(self.n):
            self.auto_state_text.insert(tk.END, f"T{i}\t", 'tenant')
            
            # Allocation
            for j in range(self.m):
                self.auto_state_text.insert(tk.END, f"{self.allocation[i][j]} ")
            self.auto_state_text.insert(tk.END, "\t\t")
            
            # Max
            for j in range(self.m):
                self.auto_state_text.insert(tk.END, f"{self.max[i][j]} ")
            self.auto_state_text.insert(tk.END, "\t\t")
            
            # Need
            for j in range(self.m):
                self.auto_state_text.insert(tk.END, f"{self.need[i][j]} ")
            self.auto_state_text.insert(tk.END, "\n")
        
        # Check safety , bankers
        safe, safe_seq = self.is_safe_state()
        if safe:
            self.auto_state_text.insert(tk.END, "\n✅ System is in ", 'safe')
            self.auto_state_text.insert(tk.END, "SAFE", 'safe_bold')
            self.auto_state_text.insert(tk.END, " state\n🔐 Safe sequence: ", 'safe')
            self.auto_state_text.insert(tk.END, " → ".join([f"P{p}" for p in safe_seq]) + "\n", 'safe_bold')
        else:
            self.auto_state_text.insert(tk.END, "\n⚠️ System is in ", 'unsafe')
            self.auto_state_text.insert(tk.END, "UNSAFE", 'unsafe_bold')
            self.auto_state_text.insert(tk.END, " state. Deadlock likely!\n", 'unsafe')
        
        self.auto_state_text.insert(tk.END, "══════════════════════════════════════════════════\n", 'header')
        
        # Configure tags for coloring
        self.auto_state_text.tag_config('header', foreground='#3f51b5', font=self.bold_font)
        self.auto_state_text.tag_config('bold', font=self.bold_font)
        self.auto_state_text.tag_config('process', foreground='#795548')
        self.auto_state_text.tag_config('safe', foreground=self.colors['safe'])
        self.auto_state_text.tag_config('safe_bold', foreground=self.colors['safe'], font=self.bold_font)
        self.auto_state_text.tag_config('unsafe', foreground=self.colors['unsafe'])
        self.auto_state_text.tag_config('unsafe_bold', foreground=self.colors['unsafe'], font=self.bold_font)
        
        self.auto_state_text.config(state=tk.DISABLED)
        self.auto_state_text.see(tk.END)

    def initialize_system(self):
        # Create a styled dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("🚀 System Initialization")
        dialog.geometry("500x400")
        dialog.configure(bg=self.colors['bg'])
        dialog.resizable(False, False)
        
        # Center the dialog
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'+{x}+{y}')
        
        # Main frame
        main_frame = tk.Frame(dialog, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        tk.Label(
            main_frame, 
            text="System Initialization", 
            font=self.title_font,
            bg=self.colors['bg'],
            fg=self.colors['header']
        ).pack(pady=(0, 20))
        
        # Process count
        tk.Label(
            main_frame, 
            text="Number of Tenants (1-10):",
            bg=self.colors['bg'],
            fg=self.colors['text']
        ).pack(anchor=tk.W)
        
        process_entry = ttk.Entry(main_frame)
        process_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Resource count
        tk.Label(
            main_frame, 
            text="Number of resources (1-10):",
            bg=self.colors['bg'],
            fg=self.colors['text']
        ).pack(anchor=tk.W)
        
        resource_entry = ttk.Entry(main_frame)
        resource_entry.pack(fill=tk.X, pady=(0, 20))
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        def on_submit():
            try:
                n = int(process_entry.get())
                m = int(resource_entry.get())
                
                if not (1 <= n <= MAX_PROCESSES and 1 <= m <= MAX_RESOURCES):
                    raise ValueError
                
                dialog.destroy()
                self.get_initial_data(n, m)
                
            except ValueError:
                messagebox.showerror("Invalid Input", 
                                   "Please enter valid numbers (1-10 for both tenants and resources).",
                                   parent=dialog)
        
        ttk.Button(
            button_frame, 
            text="Continue", 
            command=on_submit,
            style='Accent.TButton'
        ).pack(side=tk.RIGHT)
        
        ttk.Button(
            button_frame, 
            text="Cancel", 
            command=dialog.destroy
        ).pack(side=tk.RIGHT, padx=5)
        
        # Configure ttk style
        style = ttk.Style()
        style.configure('Accent.TButton', background=self.colors['highlight'], foreground='black')
        
        dialog.transient(self.root)
        dialog.grab_set()
        self.root.wait_window(dialog)

    def get_initial_data(self, n, m):
        self.n = n
        self.m = m
        
        # Get available resources
        avail_str = simpledialog.askstring("Available Resources", 
                                         f"💎 Enter available resources ({m} space-separated values):",
                                         parent=self.root)
        if avail_str is None:
            return
        
        try:
            available = list(map(int, avail_str.split()))
            if len(available) != m:
                raise ValueError
            if any(x < 0 for x in available):
                raise ValueError
        except:
            messagebox.showerror("Error", f"❌ Please enter exactly {m} non-negative integers.", icon='error')
            return
        
        self.available = available + [0] * (MAX_RESOURCES - m)
        
        # Get allocation and max matrices
        for i in range(n):
            # Allocation matrix
            alloc_str = simpledialog.askstring("Allocation Matrix", 
                                             f"📊 Allocate resources for T{i} ({m} space-separated values):",
                                             parent=self.root)
            if alloc_str is None:
                return
            
            try:
                alloc = list(map(int, alloc_str.split()))
                if len(alloc) != m:
                    raise ValueError
                if any(x < 0 for x in alloc):
                    raise ValueError
            except:
                messagebox.showerror("Error", f"❌ Please enter exactly {m} non-negative integers.", icon='error')
                return
            
            self.allocation[i] = alloc + [0] * (MAX_RESOURCES - m)
            
            # Max matrix
            max_str = simpledialog.askstring("Maximum Demand", 
                                            f"📈 Maximum demand for T{i} ({m} space-separated values):",
                                            parent=self.root)
            if max_str is None:
                return
            
            try:
                max_res = list(map(int, max_str.split()))
                if len(max_res) != m:
                    raise ValueError
                if any(x < 0 for x in max_res):
                    raise ValueError
                if any(max_res[j] < self.allocation[i][j] for j in range(m)):
                    raise ValueError("Max < Allocation")
            except ValueError as e:
                if str(e) == "Max < Allocation":
                    messagebox.showerror("Error", 
                                       f"❌ Max demand can't be less than allocation for T{i}.", icon='error')
                else:
                    messagebox.showerror("Error", f"❌ Please enter exactly {m} non-negative integers.", icon='error')
                return
            
            self.max[i] = max_res + [0] * (MAX_RESOURCES - m)
        
        self.calculate_need() #need cal
        self.update_system_state_display() #State Display
        messagebox.showinfo("Success", "🎉 System initialized successfully!", parent=self.root)

    def make_request(self):
        if self.n == 0 or self.m == 0:
            messagebox.showerror("Error", "❌ Please initialize the system first.", icon='error')
            return
        
        # Create a styled dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("📝 Resource Request")
        dialog.geometry("400x300")
        dialog.configure(bg=self.colors['bg'])
        dialog.resizable(False, False)
        
        # Center the dialog
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'+{x}+{y}')
        
        # Main frame
        main_frame = tk.Frame(dialog, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        tk.Label(
            main_frame, 
            text="Resource Request", 
            font=self.title_font,
            bg=self.colors['bg'],
            fg=self.colors['header']
        ).pack(pady=(0, 20))
        
        # Process ID
        tk.Label(
            main_frame, 
            text=f"Tenants ID (0-{self.n-1}):",
            bg=self.colors['bg'],
            fg=self.colors['text']
        ).pack(anchor=tk.W)
        
        pid_entry = ttk.Entry(main_frame)
        pid_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Request
        tk.Label(
            main_frame, 
            text=f"Request ({self.m} space-separated values):",
            bg=self.colors['bg'],
            fg=self.colors['text']
        ).pack(anchor=tk.W)
        
        request_entry = ttk.Entry(main_frame)
        request_entry.pack(fill=tk.X, pady=(0, 20))
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        def on_submit():
            try:
                pid = int(pid_entry.get())
                if not (0 <= pid < self.n):
                    raise ValueError
                
                request = list(map(int, request_entry.get().split()))
                if len(request) != self.m:
                    raise ValueError
                if any(x < 0 for x in request):
                    raise ValueError
                
                dialog.destroy()
                if self.request_resources(pid, request): #resourse management
                    messagebox.showinfo("Success", "✅ Request granted safely!", parent=self.root)
                    self.calculate_need() #need cal
                    self.update_system_state_display() #State Display
                else:
                    messagebox.showerror("Denied", "❌ Request denied. Would lead to unsafe state.", parent=self.root)
                
            except ValueError:
                messagebox.showerror("Invalid Input", 
                                   f"Please enter valid tenant ID (0-{self.n-1}) and {self.m} non-negative integers.",
                                   parent=dialog)
        
        ttk.Button(
            button_frame, 
            text="Submit", 
            command=on_submit,
            style='Accent.TButton'
        ).pack(side=tk.RIGHT)
        
        ttk.Button(
            button_frame, 
            text="Cancel", 
            command=dialog.destroy
        ).pack(side=tk.RIGHT, padx=5)
        
        dialog.transient(self.root)
        dialog.grab_set()
        self.root.wait_window(dialog)

    def request_resources(self, pid, request): #resource management
        if pid < 0 or pid >= self.n:
            messagebox.showerror("Error", f"❌ Invalid tenant ID {pid}.", icon='error')
            return False
        
        for j in range(self.m):
            if request[j] < 0:
                messagebox.showerror("Error", "❌ Requested resources cannot be negative.", icon='error')
                return False
            if request[j] > self.need[pid][j]:
                messagebox.showerror("Error", 
                    f"❌ Tenant T{pid} has requested more than its need for resource {j}.", icon='error')
                return False
            if request[j] > self.available[j]:
                messagebox.showerror("Error", 
                    f"❌ Not enough available resources for resource {j}.", icon='error')
                return False
        
        # Try allocating requested resources
        for j in range(self.m):
            self.available[j] -= request[j]
            self.allocation[pid][j] += request[j]
            self.need[pid][j] -= request[j]
        
        safe, _ = self.is_safe_state() #banker
        
        if not safe:
            # Rollback allocation
            for j in range(self.m):
                self.available[j] += request[j]
                self.allocation[pid][j] -= request[j]
                self.need[pid][j] += request[j]
            return False
        
        return True

    def abort_process(self): #process termination
        if self.n == 0 or self.m == 0:
            messagebox.showerror("Error", "❌ Please initialize the system first.", icon='error')
            return
        
        pid = simpledialog.askinteger("Abort Tenant", 
                                     f"❌ Enter tenant ID to abort (0-{self.n-1}):",
                                     parent=self.root,
                                     minvalue=0,
                                     maxvalue=self.n-1)
        if pid is None:
            return
        
        for j in range(self.m):
            self.available[j] += self.allocation[pid][j]
            self.allocation[pid][j] = 0
            self.max[pid][j] = 0
        
        self.calculate_need() #need cal
        self.update_system_state_display() # State Display
        messagebox.showinfo("Success", f"✅ Tenant T{pid} aborted.", parent=self.root)

    def preempt_process(self): #process preempt
        if self.n == 0 or self.m == 0:
            messagebox.showerror("Error", "❌ Please initialize the system first.", icon='error')
            return
        
        pid = simpledialog.askinteger("Preempt Tenant", 
                                     f"⚡ Enter tenant ID to preempt (0-{self.n-1}):",
                                     parent=self.root,
                                     minvalue=0,
                                     maxvalue=self.n-1)
        if pid is None:
            return
        
        for j in range(self.m):
            self.available[j] += self.allocation[pid][j]
            self.need[pid][j] += self.allocation[pid][j]
            self.allocation[pid][j] = 0
        
        self.calculate_need() #need cal
        self.update_system_state_display() #State Display
        messagebox.showinfo("Success", f"✅ Tenant T{pid} preempted.", parent=self.root)

    def calculate_need(self): #need cal
        for i in range(self.n):
            for j in range(self.m):
                self.need[i][j] = self.max[i][j] - self.allocation[i][j]

    def update_system_state_display(self): #state display
        self.system_state_text.config(state=tk.NORMAL)
        self.system_state_text.delete(1.0, tk.END)
        
        # Display available resources
        self.system_state_text.insert(tk.END, "══════════════════════════════════════════════════\n", 'header')
        self.system_state_text.insert(tk.END, "🛡️ Available Resources: ", 'bold')
        self.system_state_text.insert(tk.END, " ".join(map(str, self.available[:self.m])) + "\n\n")
        
        # Display matrices
        self.system_state_text.insert(tk.END, "Tenant   Allocation\t  Maximum\t      Need\n", 'bold')
        for i in range(self.n):
            self.system_state_text.insert(tk.END, f"T{i}\t", 'tenant')
            
            # Allocation
            for j in range(self.m):
                self.system_state_text.insert(tk.END, f"{self.allocation[i][j]} ")
            self.system_state_text.insert(tk.END, "\t  ")
            
            # Max
            for j in range(self.m):
                self.system_state_text.insert(tk.END, f"{self.max[i][j]} ")
            self.system_state_text.insert(tk.END, "\t  ")
            
            # Need
            for j in range(self.m):
                self.system_state_text.insert(tk.END, f"{self.need[i][j]} ")
            self.system_state_text.insert(tk.END, "\n")
        
        self.system_state_text.insert(tk.END, "══════════════════════════════════════════════════\n\n", 'header')
        
        # Check safety
        safe, safe_seq = self.is_safe_state() #banker
        if safe:
            self.system_state_text.insert(tk.END, "✅ System is in ", 'safe')
            self.system_state_text.insert(tk.END, "SAFE", 'safe_bold')
            self.system_state_text.insert(tk.END, " state.\n🔐 Safe sequence is: ", 'safe')
            self.system_state_text.insert(tk.END, " → ".join([f"P{p}" for p in safe_seq]) + "\n", 'safe_bold')
            self.status_var.set(f"✅ System is SAFE | Safe sequence: {' → '.join([f'P{p}' for p in safe_seq])}")
        else:
            self.system_state_text.insert(tk.END, "⚠️ System is in ", 'unsafe')
            self.system_state_text.insert(tk.END, "UNSAFE", 'unsafe_bold')
            self.system_state_text.insert(tk.END, " state. Deadlock likely!\n", 'unsafe')
            self.status_var.set("⚠️ System is UNSAFE - Deadlock likely!")
        
        # Configure tags for coloring
        self.system_state_text.tag_config('header', foreground='#3f51b5', font=self.bold_font)
        self.system_state_text.tag_config('bold', font=self.bold_font)
        self.system_state_text.tag_config('process', foreground='#795548')
        self.system_state_text.tag_config('safe', foreground=self.colors['safe'])
        self.system_state_text.tag_config('safe_bold', foreground=self.colors['safe'], font=self.bold_font)
        self.system_state_text.tag_config('unsafe', foreground=self.colors['unsafe'])
        self.system_state_text.tag_config('unsafe_bold', foreground=self.colors['unsafe'], font=self.bold_font)
        
        self.system_state_text.config(state=tk.DISABLED)

    def is_safe_state(self): #banker, deadlock
        work = self.available.copy()
        finish = [False] * self.n
        safe_seq = []
        
        while True:
            progress = False
            for i in range(self.n):
                if not finish[i] and all(self.need[i][j] <= work[j] for j in range(self.m)):
                    for j in range(self.m):
                        work[j] += self.allocation[i][j]
                    finish[i] = True
                    safe_seq.append(i)
                    progress = True
            
            if not progress:
                break
        
        if all(finish):
            return True, safe_seq
        return False, []

if __name__ == "__main__":
    root = tk.Tk()
    
    # Set theme (requires ttkthemes library - optional)
    try:
        from ttkthemes import ThemedStyle
        style = ThemedStyle(root)
        style.set_theme("arc")
    except ImportError:
        pass
    
    app = BankersAlgorithmGUI(root)
    root.mainloop()