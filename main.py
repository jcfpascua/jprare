import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import mysql.connector
from mysql.connector import Error
import re

TAB_CATEGORIES = {
    "Location": ["city", "barangay", "street", "address"],
    "Customers": ["customer", "customer_order", "customer_order_details", "contact_details", "contact_type"],
    "Inventory": ["item"],
    "Merchants": ["merchant", "merchant_order", "merchant_order_details"],
    "Expenses": ["expense", "expense_type", "expense_details"],
    "Suppliers": ["supplier"]
}

TABLE_DISPLAY_NAMES = {
    "city": "City",
    "barangay": "Barangay",
    "street": "Street",
    "address": "Address",
    
    "customer": "Customers",
    "customer_order": "Customer Orders",
    "customer_order_details": "Customer Order Details",
    "contact_details": "Contact Details",
    "contact_type": "Contact Types",
    
    "item": "Inventory Items",
    
    "merchant": "Merchant",
    "merchant_order": "Merchant Orders",
    "merchant_order_details": "Merchabnt Order Details",
    
    "expense": "Expenses",
    "expense_type": "Expense Types",
    "expense_details": "Expense Details",
    
    "supplier": "Suppliers"
}

COLUMN_DISPLAY_NAMES = {
    "cityID": "City ID",
    "cityName": "City Name",
    "barangayID": "Barangay ID",
    "barangayName": "Barangay Name",
    "streetID": "Street ID",
    "streetName": "Street Name",
    "customerID": "Customer ID",
    "customerName": "Customer Name",
    "orderID": "Order ID",
    "totalAmount": "Total Amount",
    "createdAt": "Created At",
    "updatedAt": "Last Updated"
}


class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.foreign_key_cache = {}  
        self.column_cache = {}  
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
    
    def get_primary_key(self, table):
        query = f"""
        SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = 'jprare_database'
        AND TABLE_NAME = '{table}'
        AND COLUMN_KEY = 'PRI'
        """
        result = self.fetch_data(query)

        if not result:
            print(f"ERROR: No primary key found for table {table}")
            return None

        print(f"DEBUG: Primary key for table {table} is {result[0][0]}") 
        return result[0][0]


    
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
        if table in self.column_cache:
            return self.column_cache[table]
            
        query = f"SHOW COLUMNS FROM {table}"
        result = self.fetch_data(query)
        columns = [column[0] for column in result]
        
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
        # """Convert database column names to prettier display names"""
        if column_name in COLUMN_DISPLAY_NAMES:
            return COLUMN_DISPLAY_NAMES[column_name]
        
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
    
    def setup_ui(self):
        main_container = ttk.Frame(self, padding="10")
        main_container.pack(fill="both", expand=True)
        
        form_title = TABLE_DISPLAY_NAMES.get(self.table_name, self.table_name.capitalize())
        form_frame = ttk.LabelFrame(main_container, text=f"{form_title} Form", padding="10")
        form_frame.pack(fill="x", pady=10)
        
        self.form_entries = {}
        
        fields_frame = ttk.Frame(form_frame)
        fields_frame.pack(fill="x", expand=True, padx=5, pady=5)
        
        fields_frame.columnconfigure(0, weight=1)
        fields_frame.columnconfigure(1, weight=3)
        
        row = 0
        for column in self.columns:
            field_frame = ttk.Frame(fields_frame)
            field_frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=2)
            
            field_frame.columnconfigure(0, weight=1)
            field_frame.columnconfigure(1, weight=3)
            
            pretty_column = self.db_manager.get_pretty_column_name(column)
            ttk.Label(field_frame, text=f"{pretty_column}:", width=20).grid(row=0, column=0, sticky="w", padx=5)
            
            if column in self.foreign_keys:
                ref_table, ref_column = self.foreign_keys[column]
                query = f"SELECT {ref_column} FROM {ref_table}"  # fetch id for dropdown
                values = self.db_manager.fetch_data(query)

                # id dropdown
                formatted_values = [str(row[0]) for row in values]

                combo = ttk.Combobox(field_frame, values=formatted_values, state="readonly", width=30)
                combo.grid(row=0, column=1, sticky="ew", padx=5)
                self.form_entries[column] = combo

            else:
                entry = ttk.Entry(field_frame, width=30)
                entry.grid(row=0, column=1, sticky="ew", padx=5)
                self.form_entries[column] = entry
            
            row += 1
        
        buttons_frame = ttk.Frame(form_frame)
        buttons_frame.pack(fill="x", pady=10)
        
        style = ttk.Style()
        style.configure('Action.TButton', font=('Segoe UI', 9))
        
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
        
        table_title = TABLE_DISPLAY_NAMES.get(self.table_name, self.table_name.capitalize())
        table_frame = ttk.LabelFrame(main_container, text=f"{table_title}", padding="10")
        table_frame.pack(fill="both", expand=True, pady=10)
        
        tree_container = ttk.Frame(table_frame)
        tree_container.pack(fill="both", expand=True)
        
        style.configure("Treeview", font=('Segoe UI', 9))
        style.configure("Treeview.Heading", font=('Segoe UI', 9, 'bold'))
        
        self.tree = ttk.Treeview(tree_container, columns=self.columns, show="headings", style="Treeview")
        
        for i, column in enumerate(self.columns):
            pretty_column = self.db_manager.get_pretty_column_name(column)
            self.tree.heading(column, text=pretty_column, anchor="center")
            
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
        
        vsb = ttk.Scrollbar(tree_container, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_container, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        tree_container.rowconfigure(0, weight=1)
        tree_container.columnconfigure(0, weight=1)
        
        self.tree.tag_configure('oddrow', background='#f5f5f5')
        self.tree.tag_configure('evenrow', background='#ffffff')
        
        self.tree.bind("<<TreeviewSelect>>", self.on_record_select)
        
        search_frame = ttk.Frame(table_frame)
        search_frame.pack(fill="x", pady=5)
        
        ttk.Label(search_frame, text="Search:").pack(side="left", padx=5)
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side="left", padx=5)
        ttk.Button(search_frame, text="Search", command=self.search_records).pack(side="left", padx=5)
        ttk.Button(search_frame, text="Clear Search", command=self.load_data).pack(side="left", padx=5)
        
        self.search_entry.bind("<Return>", lambda event: self.search_records())
    
    def search_records(self):
        search_term = self.search_entry.get().strip()
        if not search_term:
            self.load_data()
            return
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        search_columns = []
        for column in self.columns:
            if not column.endswith('ID'):
                search_columns.append(f"{column} LIKE '%{search_term}%'")
        
        if search_columns:
            query = f"SELECT * FROM {self.table_name} WHERE " + " OR ".join(search_columns)
            records = self.db_manager.fetch_data(query)
            
            for i, record in enumerate(records):
                tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                self.tree.insert("", "end", values=record, tags=(tag,))
    
    def load_data(self):
        self.clear_form()
        self.data_loaded = True
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        query = f"SELECT * FROM {self.table_name} LIMIT 100"
        records = self.db_manager.fetch_data(query)
        
        for i, record in enumerate(records):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            
            display_record = list(record)  # Convert tuple to list for modification

            for col_index, column in enumerate(self.columns):
                if column in self.foreign_keys:  # If this column is a foreign key
                    ref_table, ref_column = self.foreign_keys[column]  
                    key_id = record[col_index]  # The foreign key ID

                    if key_id is not None:
                        print(f"DEBUG: Fetching value for Table={ref_table}, Column={ref_column}, Key ID={key_id}")  # Debugging
                        
                        # description instead of id
                        foreign_value = self.get_foreign_key_value(ref_table, ref_column, key_id)

                        # replace id with actual value
                        display_record[col_index] = foreign_value

            self.tree.insert("", "end", values=display_record, tags=(tag,))
            

    def refresh_dropdowns(self):
        """Refresh foreign key dropdowns with the latest IDs in ascending order"""
        for column in self.foreign_keys:
            ref_table, ref_column = self.foreign_keys[column]

            query = f"SELECT {ref_column} FROM {ref_table} ORDER BY {ref_column} ASC"
            values = self.db_manager.fetch_data(query)

            formatted_values = sorted([str(row[0]) for row in values], key=int)

            if column in self.form_entries:
                self.form_entries[column]['values'] = formatted_values  
    
    def on_record_select(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        
        values = self.tree.item(selected_item[0], "values")
        
        self.clear_form()
        
        for i, column in enumerate(self.columns):
            if column in self.foreign_keys:
                self.form_entries[column].set(values[i])
            else:
                self.form_entries[column].insert(0, values[i])
    
    def add_record(self):
        data = {}
        for column, entry in self.form_entries.items():
            if column.endswith("ID") and column != self.columns[0]:  
                if isinstance(entry, ttk.Combobox):
                    value = entry.get().strip()
                    if value.isdigit():  
                        value = int(value)
                    else:
                        print(f"Invalid Foreign Key Value: {value} for column {column}")
                        messagebox.showerror("Error", f"Invalid value for {column}")
                        return  
                else:
                    value = entry.get()
            else:
                value = entry.get().strip()

            print(f"Column: {column}, Value: {value} (Type: {type(value)})")  

            if value:
                data[column] = value

        if data:
            last_id = self.db_manager.insert_data(self.table_name, data)
            if last_id:
                messagebox.showinfo("Success", f"Record added successfully with ID: {last_id}")
                self.clear_form()
                self.load_data()
    
    def update_record(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a record to update")
            return
        
        data = {}
        for column, entry in self.form_entries.items():
            if column == self.columns[0]:  
                continue
            
            if isinstance(entry, ttk.Combobox):
                value = entry.get()
            else:
                value = entry.get()
            
            if value:  
                data[column] = value
        
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
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a record to delete")
            return
        
        if not messagebox.askyesno("Confirm", "Are you sure you want to delete this record?"):
            return
        
        primary_key = self.columns[0]
        primary_key_value = self.tree.item(selected_item[0], "values")[0]
        condition = f"{primary_key} = {primary_key_value}"
        
        affected_rows = self.db_manager.delete_data(self.table_name, condition)
        if affected_rows:
            messagebox.showinfo("Success", f"Record deleted successfully")
            self.clear_form()
            self.load_data()
    
    def clear_form(self):
        for entry in self.form_entries.values():
            if isinstance(entry, ttk.Combobox):
                entry.set("")
            else:
                entry.delete(0, "end")
    
    # def get_foreign_key_values(self, table, column):
    #     cache_key = f"{table}_{column}"
    #     if cache_key in self.db_manager.foreign_key_cache:
    #         return self.db_manager.foreign_key_cache[cache_key]
            
    #     query = f"SELECT {column} FROM {table}"
    #     result = self.db_manager.fetch_data(query)
    #     values = sorted([str(row[0]) for row in result], key=int)
        
    #     self.db_manager.foreign_key_cache[cache_key] = values
    #     return values
    # def get_foreign_key_value(self, table, column, key_id):
    #     if key_id is None:
    #         return "N/A"  # Handle NULL values

    #     query = f"SELECT {column} FROM {table} WHERE id = %s LIMIT 1"
    #     result = self.db_manager.fetch_data(query, (key_id,))

    #     if not result:
    #         print(f"WARNING: No match found for {table}.{column} with id={key_id}")  # Debugging
        
    #     return result[0][0] if result else f"Unknown ({key_id})"

    def get_foreign_key_value(self, table, column, key_id):
        if key_id is None:
            return "N/A"  # Handle null values

        primary_key = self.db_manager.get_primary_key(table)

        if not primary_key:
            print(f"ERROR: No primary key found for table {table}")
            return f"Unknown ({key_id})"

        # Get all column names for this table
        query = f"SHOW COLUMNS FROM {table}"
        columns = [col[0] for col in self.db_manager.fetch_data(query)]

        # Prioritize the most likely descriptive columns
        possible_columns = [
            "name", "title", "description", "full_name", "label",
            f"{table}Name", f"{table}_name", f"{table}Title", f"{table}_title",
            "details", "remarks", "amount", "date"
        ]

        display_column = next((col for col in possible_columns if col in columns), None)

        if not display_column or display_column == primary_key:
            non_id_columns = [col for col in columns if col not in [primary_key, column]]
            display_column = non_id_columns[0] if non_id_columns else primary_key

        query = f"SELECT {display_column} FROM {table} WHERE {primary_key} = %s LIMIT 1"
        print(f"Executing query: {query} with key_id={key_id}")  # Debugging

        result = self.db_manager.fetch_data(query, (key_id,))
        
        if not result:
            print(f"WARNING: No match found for {table}.{display_column} WHERE {primary_key}={key_id}")
        
        return result[0][0] if result else f"Unknown ({key_id})"

class QueryFrame(ttk.Frame):
    def __init__(self, parent, db_manager):
        super().__init__(parent)
        self.db_manager = db_manager
        
        self.setup_ui()
    
    def setup_ui(self):
        main_container = ttk.Frame(self, padding="10")
        main_container.pack(fill="both", expand=True)
        
        query_frame = ttk.LabelFrame(main_container, text="Custom SQL Query", padding="10")
        query_frame.pack(fill="both", expand=True, pady=10)
        
        instructions = "Enter your SQL query below. Examples:\n" + \
                      "- SELECT * FROM Customer\n" + \
                      "- SELECT c.customer_name, a.description FROM Customer c JOIN Address a ON c.addressID = a.addressID\n" + \
                      "- INSERT INTO City (cityName) VALUES ('New City')"
        
        instruction_label = ttk.Label(query_frame, text=instructions, justify="left", wraplength=700)
        instruction_label.pack(fill="x", pady=5)
        
        query_container = ttk.Frame(query_frame)
        query_container.pack(fill="both", expand=True, pady=5)
        
        self.query_text = scrolledtext.ScrolledText(query_container, height=8, font=('Consolas', 10))
        self.query_text.pack(fill="both", expand=True)
        
        self.query_text.configure(bg='#f0f0f0', fg='#000080', insertbackground='#000000')
        
        button_frame = ttk.Frame(query_frame)
        button_frame.pack(fill="x", pady=10)
        
        execute_button = ttk.Button(button_frame, text="Execute Query", command=self.execute_query)
        execute_button.pack(side="left", padx=5)
        
        clear_button = ttk.Button(button_frame, text="Clear Query", command=lambda: self.query_text.delete(1.0, tk.END))
        clear_button.pack(side="left", padx=5)
        
        results_frame = ttk.LabelFrame(main_container, text="Query Results", padding="10")
        results_frame.pack(fill="both", expand=True, pady=10)
        
        results_container = ttk.Frame(results_frame)
        results_container.pack(fill="both", expand=True)
        
        self.results_text = scrolledtext.ScrolledText(results_container, height=12, font=('Consolas', 10))
        self.results_text.pack(fill="both", expand=True)
        
        self.results_text.configure(bg='#ffffff', fg='#000000')
    
    def execute_query(self):
        query = self.query_text.get("1.0", "end-1c").strip()
        if not query:
            messagebox.showwarning("Warning", "Please enter a SQL query")
            return
        
        try:
            if re.match(r'^\s*SELECT', query, re.IGNORECASE):
                results = self.db_manager.fetch_data(query)
                
                self.results_text.delete("1.0", "end")
                if results:
                    cursor = self.db_manager.execute_query(query)
                    columns = [column[0] for column in cursor.description]
                    cursor.close()
                    
                    header = " | ".join(columns)
                    separator = "-" * len(header)
                    
                    self.results_text.insert("end", header + "\n")
                    self.results_text.insert("end", separator + "\n")
                    
                    for row in results:
                        self.results_text.insert("end", " | ".join(str(value) for value in row) + "\n")
                    
                    self.results_text.insert("end", f"\n{len(results)} row(s) returned.")
                else:
                    self.results_text.insert("end", "No results found.")
            else:
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
        self.title("JP Rare Database Management System")
        self.geometry("1200x800")
        self.minsize(800, 600)
        
        self.state('zoomed')
        
        self.db_manager = DatabaseManager()
        
        self.setup_ui()
        
        self.protocol("WM_DELETE_WINDOW", self.destroy)
    
    def setup_ui(self):
        try:
            self.iconbitmap("icon.ico")
        except:
            pass
        
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True)
        
        header_frame = ttk.Frame(main_frame, style="Header.TFrame")
        header_frame.pack(fill="x", padx=10, pady=10)
        
        header_label = ttk.Label(header_frame, text="JP Rare Database Management System", 
                                font=("Segoe UI", 16, "bold"))
        header_label.pack(side="left", padx=10)
        
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)
        
        tables = self.db_manager.fetch_data(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'jprare_database'"
        )
        table_names = [table[0] for table in tables]
        
        print(f"Tables found in database: {table_names}")
        
        self.category_notebooks = {}
        
        for category, category_tables in TAB_CATEGORIES.items():
            category_frame = ttk.Frame(self.notebook)
            self.notebook.add(category_frame, text=category)
            
            category_notebook = ttk.Notebook(category_frame)
            category_notebook.pack(fill="both", expand=True, padx=5, pady=5)
            self.category_notebooks[category] = category_notebook
            
            tables_added = False
            
            for table_name in category_tables:
                if table_name in table_names:
                    tab = TableFrame(category_notebook, self.db_manager, table_name, category)
                    display_name = TABLE_DISPLAY_NAMES.get(table_name, table_name.capitalize())
                    category_notebook.add(tab, text=display_name)
                    tables_added = True
                    print(f"Added table {table_name} to category {category}")
                else:
                    print(f"Table {table_name} not found in database")
            
            if not tables_added:
                message_frame = ttk.Frame(category_notebook)
                ttk.Label(message_frame, text=f"No tables found for {category} category", 
                          font=("Segoe UI", 12)).pack(expand=True, pady=50)
                category_notebook.add(message_frame, text="Information")
            
            category_notebook.bind("<<NotebookTabChanged>>", self.on_tab_selected)
        
        # query_tab = QueryFrame(self.notebook, self.db_manager)
        # self.notebook.add(query_tab, text="Custom Queries")
        
        # self.notebook.bind("<<NotebookTabChanged>>", self.on_main_tab_selected)
        
        # status_frame = ttk.Frame(main_frame)
        # status_frame.pack(fill="x", padx=10, pady=5)
        
        # version_label = ttk.Label(status_frame, text="Version 0.1", font=("Segoe UI", 8))
        # version_label.pack(side="right", padx=10)
        
        # self.status_label = ttk.Label(status_frame, text="Ready", font=("Segoe UI", 8))
        # self.status_label.pack(side="left", padx=10)
    
    def on_main_tab_selected(self, event):
        tab_id = self.notebook.index("current")
        if tab_id < 0 or tab_id >= self.notebook.index("end"):
            return
            
        selected_tab = self.notebook.nametowidget(self.notebook.select())

        if isinstance(selected_tab, ttk.Frame):
            for category, notebook in self.category_notebooks.items():
                if notebook.winfo_parent() == selected_tab.winfo_pathname(selected_tab.winfo_id()):
                    category_notebook = notebook
                    break

            self.refresh_all_tables()  # Refresh all dropdowns when changing main tabs
            self.on_tab_selected(None, category_notebook)

    
    def on_tab_selected(self, event, notebook=None):
        if notebook is None:
            notebook = event.widget

        tab_id = notebook.index("current")
        if tab_id < 0 or tab_id >= notebook.index("end"):
            return

        selected_tab = notebook.nametowidget(notebook.select())

        if isinstance(selected_tab, TableFrame):
            selected_tab.refresh_dropdowns()  # refresh dropdowns when changing tabs
            if not selected_tab.data_loaded:
                selected_tab.load_data()  # load data only if not already loaded


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()