import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import mysql.connector
from mysql.connector import Error
import re
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
import sys

# Define tab categories for better organization
TAB_CATEGORIES = {
    "Location": ["city", "barangay", "street", "address"],
    "Customers": ["customer", "customer_order", "customer_order_details", "contact_details", "contact_type"],
    "Inventory": ["item"],
    "Merchants": ["merchant", "merchant_order", "merchant_order_details"],
    "Expenses": ["expense", "expense_type", "expense_details"],
    "Suppliers": ["supplier"]
}

# Define prettier display names for tables
TABLE_DISPLAY_NAMES = {
    # Location tables
    "city": "Cities",
    "barangay": "Barangays",
    "street": "Streets",
    "address": "Addresses",
    
    # Customer tables
    "customer": "Customers",
    "customer_order": "Customer Orders",
    "customer_order_details": "Order Details",
    "contact_details": "Contact Details",
    "contact_type": "Contact Types",
    
    # Inventory tables
    "item": "Inventory Items",
    
    # Merchant tables
    "merchant": "Merchants",
    "merchant_order": "Merchant Orders",
    "merchant_order_details": "Order Details",
    
    # Expense tables
    "expense": "Expenses",
    "expense_type": "Expense Types",
    "expense_details": "Expense Details",
    
    # Supplier tables
    "supplier": "Suppliers"
}

# Define prettier column names
COLUMN_DISPLAY_NAMES = {
    "id": "ID",
    "name": "Name",
    "address": "Address",
    "contact_number": "Contact Number",
    "email": "Email",
    "date": "Date",
    "amount": "Amount",
    "description": "Description",
    "price": "Price",
    "quantity": "Quantity",
    "total": "Total",
    "type": "Type",
    "details": "Details",
    "customer_id": "Customer",
    "order_id": "Order",
    "item_id": "Item",
    "merchant_id": "Merchant",
    "expense_id": "Expense",
    "supplier_id": "Supplier"
}

class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.foreign_key_cache = {}  # Cache for foreign key values
        self.column_cache = {}  # Cache for table columns
        self.connect_to_database()
        
    def connect_to_database(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="jprare_database"
            )
            print("Successfully connected to the database")
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            messagebox.showerror("Database Error", f"Could not connect to the database: {e}")
    
    def execute_query(self, query, params=None):
        try:
            if self.connection is None or not self.connection.is_connected():
                self.connect_to_database()
                
            cursor = self.connection.cursor(buffered=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
                
            self.connection.commit()
            return cursor
        except Error as e:
            print(f"Error executing query: {e}")
            messagebox.showerror("Query Error", f"Error executing query: {e}")
            return None
    
    def fetch_data(self, query, params=None):
        cursor = self.execute_query(query, params)
        if cursor:
            result = cursor.fetchall()
            cursor.close()
            return result
        return []
    
    def insert_data(self, table, data):
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        cursor = self.execute_query(query, list(data.values()))
        if cursor:
            last_id = cursor.lastrowid
            cursor.close()
            return last_id
        return None
    
    def update_data(self, table, data, condition):
        set_clause = ', '.join([f"{column} = %s" for column in data.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {condition}"
        
        cursor = self.execute_query(query, list(data.values()))
        if cursor:
            affected_rows = cursor.rowcount
            cursor.close()
            return affected_rows
        return 0
    
    def delete_data(self, table, condition):
        query = f"DELETE FROM {table} WHERE {condition}"
        
        cursor = self.execute_query(query)
        if cursor:
            affected_rows = cursor.rowcount
            cursor.close()
            return affected_rows
        return 0
    
    def get_table_columns(self, table):
        # Check cache first
        if table in self.column_cache:
            return self.column_cache[table]
            
        query = f"SHOW COLUMNS FROM {table}"
        result = self.fetch_data(query)
        columns = [column[0] for column in result]
        
        # Store in cache
        self.column_cache[table] = columns
        return columns
    
    def get_foreign_keys(self, table):
        query = f"""
        SELECT 
            COLUMN_NAME, 
            REFERENCED_TABLE_NAME, 
            REFERENCED_COLUMN_NAME
        FROM 
            INFORMATION_SCHEMA.KEY_COLUMN_USAGE
        WHERE 
            TABLE_SCHEMA = 'jprare_database' AND
            TABLE_NAME = '{table}' AND
            REFERENCED_TABLE_NAME IS NOT NULL
        """
        return self.fetch_data(query)
    
    def get_pretty_column_name(self, column_name):
        """Convert database column names to prettier display names"""
        # Check if we have a predefined pretty name
        if column_name in COLUMN_DISPLAY_NAMES:
            return COLUMN_DISPLAY_NAMES[column_name]
        
        # Otherwise, format it nicely
        # Replace underscores with spaces and capitalize each word
        words = column_name.split('_')
        return ' '.join(word.capitalize() for word in words)
    
    def close_connection(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed")

class TableFrame(ttk.Frame):
    def __init__(self, parent, db_manager, table_name, category=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.table_name = table_name
        self.category = category
        self.columns = self.db_manager.get_table_columns(table_name)
        self.foreign_keys = {fk[0]: (fk[1], fk[2]) for fk in self.db_manager.get_foreign_keys(table_name)}
        self.data_loaded = False
        
        self.setup_ui()
        # Don't load data on initialization
    
    def setup_ui(self):
        # Create main container frame with padding
        main_container = ttk.Frame(self, padding="10")
        main_container.pack(fill="both", expand=True)
        
        # Create a frame for the form with better styling
        form_title = TABLE_DISPLAY_NAMES.get(self.table_name, self.table_name.capitalize())
        form_frame = ttk.LabelFrame(main_container, text=f"{form_title} Form", padding="10")
        form_frame.pack(fill="x", pady=10)
        
        # Create form fields with grid layout and better spacing
        self.form_entries = {}
        
        # Create a frame for the form fields with a grid layout
        fields_frame = ttk.Frame(form_frame)
        fields_frame.pack(fill="x", expand=True, padx=5, pady=5)
        
        # Configure grid columns to be more responsive
        fields_frame.columnconfigure(0, weight=1)
        fields_frame.columnconfigure(1, weight=3)
        
        row = 0
        for column in self.columns:
            # Create a frame for each field for better alignment
            field_frame = ttk.Frame(fields_frame)
            field_frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=2)
            
            # Configure the field frame columns
            field_frame.columnconfigure(0, weight=1)
            field_frame.columnconfigure(1, weight=3)
            
            # Add the label and entry/combobox with prettier column names
            pretty_column = self.db_manager.get_pretty_column_name(column)
            ttk.Label(field_frame, text=f"{pretty_column}:", width=20).grid(row=0, column=0, sticky="w", padx=5)
            
            if column in self.foreign_keys:
                # Create a combobox for foreign keys
                ref_table, ref_column = self.foreign_keys[column]
                values = self.get_foreign_key_values(ref_table, ref_column)
                
                combo = ttk.Combobox(field_frame, values=values, state="readonly", width=30)
                combo.grid(row=0, column=1, sticky="ew", padx=5)
                self.form_entries[column] = combo
            else:
                entry = ttk.Entry(field_frame, width=30)
                entry.grid(row=0, column=1, sticky="ew", padx=5)
                self.form_entries[column] = entry
            
            row += 1
        
        # Create buttons frame with better styling
        buttons_frame = ttk.Frame(form_frame)
        buttons_frame.pack(fill="x", pady=10)
        
        # Add styled buttons with icons (if available)
        style = ttk.Style()
        style.configure('Action.TButton', font=('Segoe UI', 9))
        
        # Center the buttons
        buttons_container = ttk.Frame(buttons_frame)
        buttons_container.pack(anchor="center")
        
        ttk.Button(buttons_container, text="Add Record", style='Action.TButton', 
                   command=self.add_record).pack(side="left", padx=5)
        ttk.Button(buttons_container, text="Update Record", style='Action.TButton', 
                   command=self.update_record).pack(side="left", padx=5)
        ttk.Button(buttons_container, text="Delete Record", style='Action.TButton', 
                   command=self.delete_record).pack(side="left", padx=5)
        ttk.Button(buttons_container, text="Clear Form", style='Action.TButton', 
                   command=self.clear_form).pack(side="left", padx=5)
        
        # Create a frame for the table with better styling
        table_title = TABLE_DISPLAY_NAMES.get(self.table_name, self.table_name.capitalize())
        table_frame = ttk.LabelFrame(main_container, text=f"{table_title}", padding="10")
        table_frame.pack(fill="both", expand=True, pady=10)
        
        # Create a container for the treeview and scrollbars
        tree_container = ttk.Frame(table_frame)
        tree_container.pack(fill="both", expand=True)
        
        # Create treeview with improved styling
        style.configure("Treeview", font=('Segoe UI', 9))
        style.configure("Treeview.Heading", font=('Segoe UI', 9, 'bold'))
        
        self.tree = ttk.Treeview(tree_container, columns=self.columns, show="headings", style="Treeview")
        
        # Set column headings with better sizing and prettier names
        for i, column in enumerate(self.columns):
            pretty_column = self.db_manager.get_pretty_column_name(column)
            self.tree.heading(column, text=pretty_column, anchor="center")
            
            # Adjust column width based on content type
            if column.lower().endswith('id'):
                width = 80
            elif 'name' in column.lower() or 'title' in column.lower():
                width = 150
            elif 'date' in column.lower():
                width = 100
            elif 'description' in column.lower() or 'details' in column.lower():
                width = 200
            else:
                width = 120
                
            self.tree.column(column, width=width, anchor="center")
        
        # Add scrollbars with better integration
        vsb = ttk.Scrollbar(tree_container, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_container, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Pack the treeview and scrollbars for better layout
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        # Make the treeview expandable
        tree_container.rowconfigure(0, weight=1)
        tree_container.columnconfigure(0, weight=1)
        
        # Add alternating row colors
        self.tree.tag_configure('oddrow', background='#f5f5f5')
        self.tree.tag_configure('evenrow', background='#ffffff')
        
        # Bind treeview selection event
        self.tree.bind("<<TreeviewSelect>>", self.on_record_select)
        
        # Add a search frame
        search_frame = ttk.Frame(table_frame)
        search_frame.pack(fill="x", pady=5)
        
        ttk.Label(search_frame, text="Search:").pack(side="left", padx=5)
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side="left", padx=5)
        ttk.Button(search_frame, text="Search", command=self.search_records).pack(side="left", padx=5)
        ttk.Button(search_frame, text="Clear Search", command=self.load_data).pack(side="left", padx=5)
        
        # Bind the Enter key to the search function
        self.search_entry.bind("<Return>", lambda event: self.search_records())
    
    def search_records(self):
        search_term = self.search_entry.get().strip()
        if not search_term:
            self.load_data()
            return
        
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Build a search query for all text columns
        search_columns = []
        for column in self.columns:
            # Skip searching in ID columns for better performance
            if not column.endswith('ID'):
                search_columns.append(f"{column} LIKE '%{search_term}%'")
        
        if search_columns:
            query = f"SELECT * FROM {self.table_name} WHERE " + " OR ".join(search_columns)
            records = self.db_manager.fetch_data(query)
            
            # Insert data into treeview with alternating row colors
            for i, record in enumerate(records):
                tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                self.tree.insert("", "end", values=record, tags=(tag,))
    
    def load_data(self):
        # Set flag to indicate data has been loaded
        self.data_loaded = True
        
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Fetch data from database with a limit for better performance
        query = f"SELECT * FROM {self.table_name} LIMIT 100"
        records = self.db_manager.fetch_data(query)
        
        # Insert data into treeview with alternating row colors
        for i, record in enumerate(records):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.insert("", "end", values=record, tags=(tag,))
    
    def on_record_select(self, event):
        # Get selected item
        selected_item = self.tree.selection()
        if not selected_item:
            return
        
        # Get values of selected item
        values = self.tree.item(selected_item[0], "values")
        
        # Clear form
        self.clear_form()
        
        # Fill form with selected values
        for i, column in enumerate(self.columns):
            if column in self.foreign_keys:
                self.form_entries[column].set(values[i])
            else:
                self.form_entries[column].insert(0, values[i])
    
    def add_record(self):
        # Get values from form
        data = {}
        for column, entry in self.form_entries.items():
            if column.endswith('ID') and column != self.columns[0]:  # Skip primary key for inserts
                continue
            
            if isinstance(entry, ttk.Combobox):
                value = entry.get()
            else:
                value = entry.get()
            
            if value:  # Only include non-empty values
                data[column] = value
        
        # Insert data into database
        if data:
            last_id = self.db_manager.insert_data(self.table_name, data)
            if last_id:
                messagebox.showinfo("Success", f"Record added successfully with ID: {last_id}")
                self.clear_form()
                self.load_data()
    
    def update_record(self):
        # Get selected item
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a record to update")
            return
        
        # Get values from form
        data = {}
        for column, entry in self.form_entries.items():
            if column == self.columns[0]:  # Skip primary key for updates
                continue
            
            if isinstance(entry, ttk.Combobox):
                value = entry.get()
            else:
                value = entry.get()
            
            if value:  # Only include non-empty values
                data[column] = value
        
        # Update data in database
        if data:
            primary_key = self.columns[0]
            primary_key_value = self.tree.item(selected_item[0], "values")[0]
            condition = f"{primary_key} = {primary_key_value}"
            
            affected_rows = self.db_manager.update_data(self.table_name, data, condition)
            if affected_rows:
                messagebox.showinfo("Success", f"Record updated successfully")
                self.clear_form()
                self.load_data()
    
    def delete_record(self):
        # Get selected item
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a record to delete")
            return
        
        # Confirm deletion
        if not messagebox.askyesno("Confirm", "Are you sure you want to delete this record?"):
            return
        
        # Delete data from database
        primary_key = self.columns[0]
        primary_key_value = self.tree.item(selected_item[0], "values")[0]
        condition = f"{primary_key} = {primary_key_value}"
        
        affected_rows = self.db_manager.delete_data(self.table_name, condition)
        if affected_rows:
            messagebox.showinfo("Success", f"Record deleted successfully")
            self.clear_form()
            self.load_data()
    
    def clear_form(self):
        # Clear all form entries
        for entry in self.form_entries.values():
            if isinstance(entry, ttk.Combobox):
                entry.set("")
            else:
                entry.delete(0, "end")
    
    def get_foreign_key_values(self, table, column):
        # Check if values are in the cache
        cache_key = f"{table}_{column}"
        if cache_key in self.db_manager.foreign_key_cache:
            return self.db_manager.foreign_key_cache[cache_key]
            
        # If not in cache, fetch from database
        query = f"SELECT {column} FROM {table}"
        result = self.db_manager.fetch_data(query)
        values = [str(row[0]) for row in result]
        
        # Store in cache for future use
        self.db_manager.foreign_key_cache[cache_key] = values
        return values

class QueryFrame(ttk.Frame):
    def __init__(self, parent, db_manager):
        super().__init__(parent)
        self.db_manager = db_manager
        
        self.setup_ui()
    
    def setup_ui(self):
        # Create main container with padding
        main_container = ttk.Frame(self, padding="10")
        main_container.pack(fill="both", expand=True)
        
        # Create a frame for the query input with better styling
        query_frame = ttk.LabelFrame(main_container, text="Custom SQL Query", padding="10")
        query_frame.pack(fill="both", expand=True, pady=10)
        
        # Add query instructions
        instructions = "Enter your SQL query below. Examples:\n" + \
                      "- SELECT * FROM Customer\n" + \
                      "- SELECT c.customer_name, a.description FROM Customer c JOIN Address a ON c.addressID = a.addressID\n" + \
                      "- INSERT INTO City (cityName) VALUES ('New City')"
        
        instruction_label = ttk.Label(query_frame, text=instructions, justify="left", wraplength=700)
        instruction_label.pack(fill="x", pady=5)
        
        # Create text area for query input with syntax highlighting styling
        query_container = ttk.Frame(query_frame)
        query_container.pack(fill="both", expand=True, pady=5)
        
        self.query_text = scrolledtext.ScrolledText(query_container, height=8, font=('Consolas', 10))
        self.query_text.pack(fill="both", expand=True)
        
        # Add a dark background for the SQL editor
        self.query_text.configure(bg='#f0f0f0', fg='#000080', insertbackground='#000000')
        
        # Create button to execute query with better styling
        button_frame = ttk.Frame(query_frame)
        button_frame.pack(fill="x", pady=10)
        
        execute_button = ttk.Button(button_frame, text="Execute Query", command=self.execute_query)
        execute_button.pack(side="left", padx=5)
        
        clear_button = ttk.Button(button_frame, text="Clear Query", command=lambda: self.query_text.delete(1.0, tk.END))
        clear_button.pack(side="left", padx=5)
        
        # Create a frame for the query results with better styling
        results_frame = ttk.LabelFrame(main_container, text="Query Results", padding="10")
        results_frame.pack(fill="both", expand=True, pady=10)
        
        # Create text area for query results with better styling
        results_container = ttk.Frame(results_frame)
        results_container.pack(fill="both", expand=True)
        
        self.results_text = scrolledtext.ScrolledText(results_container, height=12, font=('Consolas', 10))
        self.results_text.pack(fill="both", expand=True)
        
        # Add a light background for the results
        self.results_text.configure(bg='#ffffff', fg='#000000')
    
    def execute_query(self):
        # Get query from text area
        query = self.query_text.get("1.0", "end-1c").strip()
        if not query:
            messagebox.showwarning("Warning", "Please enter a SQL query")
            return
        
        # Execute query and display results
        try:
            # Check if query is a SELECT query
            if re.match(r'^\s*SELECT', query, re.IGNORECASE):
                # Fetch data
                results = self.db_manager.fetch_data(query)
                
                # Display results
                self.results_text.delete("1.0", "end")
                if results:
                    # Get column names
                    cursor = self.db_manager.execute_query(query)
                    columns = [column[0] for column in cursor.description]
                    cursor.close()
                    
                    # Format column headers
                    header = " | ".join(columns)
                    separator = "-" * len(header)
                    
                    # Display headers
                    self.results_text.insert("end", header + "\n")
                    self.results_text.insert("end", separator + "\n")
                    
                    # Display data
                    for row in results:
                        self.results_text.insert("end", " | ".join(str(value) for value in row) + "\n")
                    
                    self.results_text.insert("end", f"\n{len(results)} row(s) returned.")
                else:
                    self.results_text.insert("end", "No results found.")
            else:
                # Execute non-SELECT query
                cursor = self.db_manager.execute_query(query)
                if cursor:
                    affected_rows = cursor.rowcount
                    cursor.close()
                    
                    self.results_text.delete("1.0", "end")
                    self.results_text.insert("end", f"Query executed successfully. {affected_rows} row(s) affected.")
        except Error as e:
            self.results_text.delete("1.0", "end")
            self.results_text.insert("end", f"Error executing query: {e}")

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("JPRare Database Management System")
        self.geometry("1200x800")
        self.minsize(800, 600)
        
        # Start the application maximized
        self.state('zoomed')
        
        # Initialize database
        self.db_manager = DatabaseManager()
        
        # Setup UI
        self.setup_ui()
        
        # Set up closing protocol without confirmation
        self.protocol("WM_DELETE_WINDOW", self.destroy)
    
    def setup_ui(self):
        # Set application icon if available
        try:
            self.iconbitmap("icon.ico")
        except:
            pass
        
        # Create main container frame
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True)
        
        # Create header with application title
        header_frame = ttk.Frame(main_frame, style="Header.TFrame")
        header_frame.pack(fill="x", padx=10, pady=10)
        
        header_label = ttk.Label(header_frame, text="JPRare Database Management System", 
                                font=("Segoe UI", 16, "bold"))
        header_label.pack(side="left", padx=10)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Get all tables from the database
        tables = self.db_manager.fetch_data(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'jprare_database'"
        )
        table_names = [table[0] for table in tables]
        
        # For debugging
        print(f"Tables found in database: {table_names}")
        
        # Create tabs organized by categories
        self.category_notebooks = {}
        
        for category, category_tables in TAB_CATEGORIES.items():
            # Create a frame for this category
            category_frame = ttk.Frame(self.notebook)
            self.notebook.add(category_frame, text=category)
            
            # Create a notebook for tables in this category
            category_notebook = ttk.Notebook(category_frame)
            category_notebook.pack(fill="both", expand=True, padx=5, pady=5)
            self.category_notebooks[category] = category_notebook
            
            # Track if we added any tables to this category
            tables_added = False
            
            # Add tabs for each table in this category
            for table_name in category_tables:
                if table_name in table_names:
                    tab = TableFrame(category_notebook, self.db_manager, table_name, category)
                    # Use prettier display name for the tab
                    display_name = TABLE_DISPLAY_NAMES.get(table_name, table_name.capitalize())
                    category_notebook.add(tab, text=display_name)
                    tables_added = True
                    print(f"Added table {table_name} to category {category}")
                else:
                    print(f"Table {table_name} not found in database")
            
            # If no tables were added to this category, add a message
            if not tables_added:
                message_frame = ttk.Frame(category_notebook)
                ttk.Label(message_frame, text=f"No tables found for {category} category", 
                          font=("Segoe UI", 12)).pack(expand=True, pady=50)
                category_notebook.add(message_frame, text="Information")
            
            # Bind tab selection event to load data when tab is selected
            category_notebook.bind("<<NotebookTabChanged>>", self.on_tab_selected)
        
        # Create a tab for custom queries
        query_tab = QueryFrame(self.notebook, self.db_manager)
        self.notebook.add(query_tab, text="Custom Queries")
        
        # Bind the main notebook tab change event
        self.notebook.bind("<<NotebookTabChanged>>", self.on_main_tab_selected)
        
        # Create status bar
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill="x", padx=10, pady=5)
        
        # Add version label to status bar
        version_label = ttk.Label(status_frame, text="Version 0.1", font=("Segoe UI", 8))
        version_label.pack(side="right", padx=10)
        
        # Add status message to status bar
        self.status_label = ttk.Label(status_frame, text="Ready", font=("Segoe UI", 8))
        self.status_label.pack(side="left", padx=10)
    
    def on_main_tab_selected(self, event):
        # Get the selected tab
        tab_id = self.notebook.index("current")
        if tab_id < 0 or tab_id >= self.notebook.index("end"):
            return
            
        selected_tab = self.notebook.nametowidget(self.notebook.select())
        
        # If it's a category frame, get the notebook and selected tab within it
        if isinstance(selected_tab, ttk.Frame):
            # Find the category notebook
            for category, notebook in self.category_notebooks.items():
                if notebook.winfo_parent() == selected_tab.winfo_pathname(selected_tab.winfo_id()):
                    category_notebook = notebook
                    break
                
            # Load data for the selected tab
            self.on_tab_selected(None, category_notebook)
    
    def on_tab_selected(self, event, notebook=None):
        # Get the notebook that triggered the event
        if notebook is None:
            notebook = event.widget
            
        # Get the selected tab widget
        tab_id = notebook.index("current")
        if tab_id < 0 or tab_id >= notebook.index("end"):
            return
            
        selected_tab = notebook.nametowidget(notebook.select())
        
        # If it's a TableFrame and data hasn't been loaded yet, load it
        if isinstance(selected_tab, TableFrame) and not selected_tab.data_loaded:
            selected_tab.load_data()

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()



    
