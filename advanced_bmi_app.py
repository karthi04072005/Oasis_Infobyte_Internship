import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
from datetime import datetime

# Import for graphing
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class BMIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced BMI Calculator")
        self.root.geometry("450x400")
        
        # Use ttk for a more modern look
        style = ttk.Style()
        style.theme_use('clam')

        # --- Main Frame ---
        main_frame = ttk.Frame(root, padding="20 20 20 20")
        main_frame.pack(expand=True, fill=tk.BOTH)

        # --- Input Frame ---
        input_frame = ttk.LabelFrame(main_frame, text="Enter Your Details", padding="15 10")
        input_frame.pack(fill="x", pady=10)
        
        # Username
        ttk.Label(input_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.username_entry = ttk.Entry(input_frame, width=30)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        # Weight
        ttk.Label(input_frame, text="Weight (kg):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.weight_entry = ttk.Entry(input_frame, width=30)
        self.weight_entry.grid(row=1, column=1, padx=5, pady=5)

        # Height
        ttk.Label(input_frame, text="Height (m):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.height_entry = ttk.Entry(input_frame, width=30)
        self.height_entry.grid(row=2, column=1, padx=5, pady=5)

        # --- Button Frame ---
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=10)

        self.calc_button = ttk.Button(button_frame, text="Calculate & Save BMI", command=self.calculate_and_save)
        self.calc_button.pack(side="left", expand=True, fill="x", padx=5)

        self.history_button = ttk.Button(button_frame, text="Show User History", command=self.show_history)
        self.history_button.pack(side="right", expand=True, fill="x", padx=5)

        # --- Result Frame ---
        result_frame = ttk.LabelFrame(main_frame, text="Result", padding="15 10")
        result_frame.pack(fill="both", expand=True, pady=10)
        
        self.result_label = ttk.Label(result_frame, text="Please enter your details and click 'Calculate'.", font=("Helvetica", 11))
        self.result_label.pack(pady=10)
        
        self.category_label = ttk.Label(result_frame, text="", font=("Helvetica", 14, "bold"))
        self.category_label.pack(pady=5)


    def calculate_and_save(self):
        """Calculates BMI, displays it, and saves it to a CSV file."""
        username = self.username_entry.get().strip()
        weight_str = self.weight_entry.get()
        height_str = self.height_entry.get()

        # --- 1. User Input Validation (Challenge 1 & 7) ---
        if not username:
            messagebox.showerror("Error", "Username cannot be empty.")
            return

        try:
            weight_kg = float(weight_str)
            height_m = float(height_str)
            
            if weight_kg <= 0 or height_m <= 0:
                messagebox.showerror("Error", "Weight and height must be positive numbers.")
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter numbers for weight and height.")
            return

        # --- 2. BMI Calculation (Challenge 2) ---
        bmi = weight_kg / (height_m ** 2)

        # --- 3. Categorization (Challenge 3) ---
        category = self.get_bmi_category(bmi)

        # --- 4. GUI Design & Display (Challenge 4 & 8) ---
        self.result_label.config(text=f"Your Calculated BMI is: {bmi:.2f}")
        self.category_label.config(text=f"Category: {category}")
        
        # Set color based on category
        color_map = {
            "Underweight": "blue",
            "Normal Weight": "green",
            "Overweight": "orange",
            "Obesity": "red"
        }
        self.category_label.config(foreground=color_map.get(category, "black"))

        # --- 5. Data Storage (Challenge 5 & 7) ---
        try:
            self.save_to_csv(username, weight_kg, height_m, bmi, category)
            messagebox.showinfo("Success", f"Data saved for user: {username}")
        except Exception as e:
            messagebox.showerror("Save Error", f"Could not save data: {e}")
            
        # Clear entries for next input
        self.weight_entry.delete(0, tk.END)
        self.height_entry.delete(0, tk.END)


    def get_bmi_category(self, bmi):
        """Returns the BMI category string."""
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 25:
            return "Normal Weight"
        elif 25 <= bmi < 30:
            return "Overweight"
        else:
            return "Obesity"

    def save_to_csv(self, username, weight, height, bmi, category):
        """Saves a single entry to the BMI data file."""
        file_name = 'bmi_data.csv'
        file_exists = os.path.isfile(file_name)
        
        date_today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data_row = [date_today, username, weight, height, round(bmi, 2), category]
        
        with open(file_name, 'a', newline='') as f:
            writer = csv.writer(f)
            # Write header only if file is new
            if not file_exists:
                writer.writerow(["Timestamp", "Username", "Weight (kg)", "Height (m)", "BMI", "Category"])
            # Write the data
            writer.writerow(data_row)


    def show_history(self):
        """Reads the CSV and displays a graph of the user's BMI history."""
        username = self.username_entry.get().strip()
        if not username:
            messagebox.showerror("Error", "Please enter a username to show history.")
            return

        file_name = 'bmi_data.csv'
        if not os.path.isfile(file_name):
            messagebox.showinfo("No Data", "No data file found. Save a calculation first.")
            return

        dates = []
        bmis = []

        # Read data from CSV
        with open(file_name, 'r') as f:
            reader = csv.reader(f)
            header = next(reader) # Skip header
            for row in reader:
                if row[1] == username: # Check if username matches
                    dates.append(datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d'))
                    bmis.append(float(row[4])) # BMI value

        if not dates:
            messagebox.showinfo("No Data", f"No historical data found for user: {username}")
            return
            
        # --- 6. Data Visualization (Challenge 6) ---
        # Create a new Toplevel window for the graph
        history_window = tk.Toplevel(self.root)
        history_window.title(f"BMI History for {username}")
        history_window.geometry("600x450")

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(dates, bmis, marker='o', linestyle='-')
        ax.set_title(f"BMI Trend for {username}")
        ax.set_xlabel("Date")
        ax.set_ylabel("BMI")
        ax.grid(True)
        
        # Rotate date labels for readability
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
        fig.tight_layout() # Adjust layout to prevent labels from being cut off

        # Embed the graph in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=history_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = BMIApp(root)
    root.mainloop()