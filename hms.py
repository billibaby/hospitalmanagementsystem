import tkinter as tk
from tkinter import ttk, Entry, Text
from typing import List

import mysql.connector

# MySQL Configuration
mysql_config = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "Billiondollar1$",  # Replace with your MySQL password
    "database": "hospital_management_system",  # Replace with your actual database name
}

# Create a MySQL connection
connection = mysql.connector.connect(**mysql_config)
cursor = connection.cursor()


# Function to save patient data
def save_patient_data():
    # Extracting data from input fields
    patient_data = [entry.get() for entry in input_fields]
    gender = gender_var.get()
    patient_data.append(gender)

    # Insert data into the MySQL database
    cursor.execute("""
        INSERT INTO patientinformation (Name, ResidentialAddress, DateOfBirth, UnderlyingHealthConditions, IDNumber, Gender, PhoneNumber)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, tuple(patient_data))

    # Commit changes
    connection.commit()


# Function to save hospital attendance data
def save_attendance_data():
    # Extracting data from input fields
    attendance_data = [entry.get() for entry in input_fields]
    prescriptions = prescriptions_entry.get("1.0", "end-1c")  # Extracting text from Text widget
    attendance_data.append(prescriptions)

    # Insert data into the MySQL database
    cursor.execute("""
        INSERT INTO hospitalattendance (PatientID, DateOfVisitation, DiagnosisResult, Prescriptions, Dosage, Doctor, InpatientRecord)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, tuple(attendance_data))

    # Commit changes
    connection.commit()


# Function to search patient data
def search_patient_data():
    # Extracting search name from entry
    search_name = search_name_entry.get()

    # Search for patient data in the MySQL database
    cursor.execute("""
        SELECT * FROM patientinformation WHERE Name = %s
    """, (search_name,))
    search_result = cursor.fetchall()

    # Displaying search results in the text widget
    result_text.delete(1.0, tk.END)  # Clear previous results
    for row in search_result:
        result_text.insert(tk.END, f"{row}\n")


# GUI setup
root = tk.Tk()
root.title("Hospital Management System")

# Create notebook
notebook = ttk.Notebook(root)
notebook.pack(pady=10)

# Tab 1: Patient Information
patient_info_frame = ttk.Frame(notebook)
notebook.add(patient_info_frame, text="Patient Information")

# Define input fields and labels for general patient data
input_fields: List[Entry] = []
labels = ["Name", "Residential Address", "Date of Birth", "Underlying Health Conditions", "ID Number", "Phone Number"]
gender_var = tk.StringVar()
gender_var.set("Male")  # Default gender value

for i, label_text in enumerate(labels):
    label = tk.Label(patient_info_frame, text=label_text + ":")
    label.grid(row=i, column=0, sticky="e", padx=10, pady=5)
    entry = tk.Entry(patient_info_frame)
    entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
    input_fields.append(entry)

# Create a radio button for gender selection
gender_frame = ttk.LabelFrame(patient_info_frame, text="Gender")
gender_frame.grid(row=len(labels), column=0, columnspan=2, pady=10, padx=10, sticky="w")

male_radio = tk.Radiobutton(gender_frame, text="Male", variable=gender_var, value="Male")
female_radio = tk.Radiobutton(gender_frame, text="Female", variable=gender_var, value="Female")

male_radio.grid(row=0, column=0, padx=5)
female_radio.grid(row=0, column=1, padx=5)

# Save button for patient information
save_info_button = tk.Button(patient_info_frame, text="Save Patient Info", command=save_patient_data, bg="green",
                             fg="white")
save_info_button.grid(row=len(labels) + 1, column=0, columnspan=2, pady=10)

# Tab 2: Hospital Attendance
hospital_attendance_frame = ttk.Frame(notebook)
notebook.add(hospital_attendance_frame, text="Hospital Attendance Record")

attendance_labels = ["Date of Visitation", "Diagnosis Result", "Prescriptions", "Dosage", "Doctor", "Inpatient Record"]

for i, label_text in enumerate(attendance_labels):
    label = tk.Label(hospital_attendance_frame, text=label_text + ":")
    label.grid(row=i, column=0, sticky="e", padx=10, pady=5)
    entry = tk.Entry(hospital_attendance_frame)
    entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
    input_fields.append(entry)

# Create a text widget for prescriptions
prescriptions_label = tk.Label(hospital_attendance_frame, text="Prescriptions:")
prescriptions_label.grid(row=len(attendance_labels), column=0, sticky="ne", padx=10, pady=5)

prescriptions_entry = Text(hospital_attendance_frame, height=5, width=30)
prescriptions_entry.grid(row=len(attendance_labels), column=1, padx=10, pady=5, sticky="nw")

# Save button for hospital attendance
save_attendance_button = tk.Button(hospital_attendance_frame, text="Save Attendance Record",
                                   command=save_attendance_data, bg="green", fg="white")
save_attendance_button.grid(row=len(attendance_labels) + 1, column=0, columnspan=2, pady=10)

# Tab 3: Search and View Patient Data
search_view_frame = ttk.Frame(notebook)
notebook.add(search_view_frame, text="Search & View Patient Data")

# Search label and entry
search_label = tk.Label(search_view_frame, text="Search by Name:")
search_label.grid(row=0, column=0, sticky="e", padx=10, pady=5)
search_name_entry = tk.Entry(search_view_frame)
search_name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

# Search button
search_button = tk.Button(search_view_frame, text="Search", command=search_patient_data)
search_button.grid(row=0, column=2, pady=5)

# Text widget to display the search results
result_text = tk.Text(search_view_frame, height=10, width=60)
result_text.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

root.mainloop()
