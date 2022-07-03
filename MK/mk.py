import datetime as dt
import tkinter as tk
from dateutil.relativedelta import relativedelta as rd
from tkinter import messagebox as mb

CATEGORY_OPTIONS = {"PE": 2, "DE": 3}

def show_error(message):
    mb.showwarning("Warning", message)

def get_date_of_designation():
    date_of_designation_list = date_of_designation.get().split("/")
    if len(date_of_designation_list) != 3:
        raise Exception("Error in date of designation format")
    
    date_of_designation_list = [int(x) for x in date_of_designation_list]
    date_of_designation_list.reverse()
    temp_designation_date = dt.date(*date_of_designation_list)
    
    return temp_designation_date

def reduce_designation(designation_date):
    duration_of_service_list = duration_of_service.get().split("/")
    if len(duration_of_service_list) != 3:
        raise Exception("Error in duration of service format")
    
    years, months, days = [int(x) for x in duration_of_service_list]
    designation_date = ((designation_date - rd(years=years)) - rd(months=months)) - rd(days=days)
    
    if has_master_graduate.get() == 1 and employee_type.get() == "PE":
        designation_date = designation_date - rd(years=4)
    
    return designation_date

def calculate_mk(start_date):
    mk_value = -1
    current_date = dt.date.today()
    
    while start_date < current_date:
        start_date += rd(years=CATEGORY_OPTIONS.get(employee_type.get()))
        mk_value += 1
    
    return mk_value, start_date

def date_to_string(date):
    return str(date.day) + "/" + str(date.month) + "/" + str(date.year)

def handle_calculation_btn_click():
    try:
        temp_designation_date = get_date_of_designation()
        temp_designation_date = reduce_designation(temp_designation_date)
        mk_value, next_mk_date = calculate_mk(temp_designation_date)
        message = "Current: " + str(mk_value) + " | Next: " + date_to_string(next_mk_date)
        result.set(message)
    except Exception as exception:
        show_error(exception)

def create_gui():
    window = tk.Tk()
    window.title("MK Calculator")
    window.rowconfigure([0, 5], minsize=50)
    
    lbl_date_of_designation = tk.Label(window, text="Date of designation (DD/MM/YYYY):")
    lbl_date_of_designation.grid(row=0, column=0)
    
    global date_of_designation
    date_of_designation = tk.StringVar()
    ent_date_of_designation = tk.Entry(window, textvariable=date_of_designation)
    ent_date_of_designation.grid(row=0, column=1)
    
    lbl_duration_of_service = tk.Label(window, text="Duration of service (Y/M/D):")
    lbl_duration_of_service.grid(row=1, column=0)
    
    global duration_of_service
    duration_of_service = tk.StringVar()
    ent_duration_of_service = tk.Entry(window, textvariable=duration_of_service)
    ent_duration_of_service.grid(row=1, column=1)
    
    lbl_employee_type = tk.Label(window, text="Employee type:")
    lbl_employee_type.grid(row=2, column=0)
    
    category_types = list(CATEGORY_OPTIONS.keys())
    
    global employee_type
    employee_type = tk.StringVar()
    employee_type.set(category_types[0])
    om_employee_type = tk.OptionMenu(window, employee_type, *category_types)
    om_employee_type.grid(row=2, column=1)
    
    lbl_masters_degree = tk.Label(window, text="Master's degree:")
    lbl_masters_degree.grid(row=3, column=0)
    
    global has_master_graduate
    has_master_graduate = tk.IntVar()
    cb_master_graduate = tk.Checkbutton(window, variable=has_master_graduate)
    cb_master_graduate.grid(row=3, column=1)
    
    lbl_result = tk.Label(window, text="Result:")
    lbl_result.grid(row=4, column=0)
    
    global result
    result = tk.StringVar()
    lbl_result_text = tk.Label(window, textvariable=result, borderwidth=2, relief="solid", width=25)
    lbl_result_text.grid(row=4, column=1)
    
    btn_calculate = tk.Button(window, text="Calculate", command=handle_calculation_btn_click)
    btn_calculate.grid(row=5, column=1)
    
    window.mainloop()

if __name__ == "__main__":
    create_gui()