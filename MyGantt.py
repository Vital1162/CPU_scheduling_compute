# CPU scheduling
import matplotlib.pyplot as plt
import numpy as np


import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import heapq
# Process class
class Process:
    def __init__(self,pid,arrival_time,burst_time,completion_time=0,priority=None, first_exe=None):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.completion_time  = completion_time
        self.priority = priority #some time they have it
        self.first_exe = first_exe

# Gantt entry
class GanttEntry:
    def __init__(self,start,end, process):
        self.start = start
        self.end = end
        self.process = process

# avg TAT, RT and WT
# TAT = CT - AT
# WT = TAT - BT
# RT = FIRST TIME PR - AT
def compute_avg_turnaround_time(processes):
    return sum(process.completion_time -  process.arrival_time for process in processes)/len(processes)

def compute_avg_waiting_time(processes):
    return sum(process.completion_time -  process.arrival_time - process.burst_time for process in processes)/len(processes)

def compute_avg_response_time(processes):
    return sum(process.first_exe - process.arrival_time for process in processes)/len(processes)


#algo
def fcfs(processes):
    current_time = 0
    gantt_chart = []
    for process in processes:
        process.completion_time = max(current_time, process.arrival_time) + process.burst_time
        process.first_exe = max(current_time, process.arrival_time)
        gantt_chart.append((current_time, process.completion_time, process.pid))
        current_time = process.completion_time
    return processes, gantt_chart





def draw_gantt_chart(gantt_chart, avg_turnaround_time, avg_waiting_time, avg_response_time):
    fig, gnt = plt.subplots()
    gnt.set_xlabel('Time')
    gnt.set_ylabel('Processes')
    for gantt_entry in gantt_chart:
        gnt.broken_barh([(gantt_entry[0], gantt_entry[1] - gantt_entry[0])], (gantt_entry[2] - 0.4, 0.8))

    plt.title(f'Average Turnaround Time: {avg_turnaround_time:.2f}\nAverage Waiting Time: {avg_waiting_time:.2f}\nAverage Response Time: {avg_response_time:.2f}')

    # Set the step size of each axis to 1
    gnt.set_xticks(np.arange(0, max(gantt_chart, key=lambda x: x[1])[1] + 1, 1))
    gnt.set_yticks(np.arange(0, len(gantt_chart) + 1, 1))

    plt.show()

def add_process():
    pid = int(pid_entry.get())
    arrival_time = float(arrival_time_entry.get())
    burst_time = float(burst_time_entry.get())
    
    # some var need to have for some case
    time_quantum = float(time_quantum_entry.get())
    priority = float(priority_entry.get())
    

    process = Process(pid, arrival_time, burst_time, priority=priority)
    processes.append(process)
    if priority:
        processes_listbox.insert(tk.END, f"PID: {pid}, Arrival Time: {arrival_time}, Burst Time: {burst_time}, Priority: {priority}")
    else:
        processes_listbox.insert(tk.END, f"PID: {pid}, Arrival Time: {arrival_time}, Burst Time: {burst_time}")


    # Clear input fields after adding process
    pid_entry.delete(0, tk.END)
    arrival_time_entry.delete(0, tk.END)
    burst_time_entry.delete(0, tk.END)
    priority_entry.delete(0,tk.END)

def run_fcfs():
    global processes
    processes, gantt_chart = fcfs(processes)
    avg_turnaround_time = compute_avg_turnaround_time(processes)
    avg_waiting_time = compute_avg_waiting_time(processes)
    avg_response_time = compute_avg_response_time(processes)
    draw_gantt_chart(gantt_chart, avg_turnaround_time, avg_waiting_time, avg_response_time)





# SJF Preemptive algorithm
def sjf_preemptive(processes):
    current_time = 0
    remaining_processes = processes[:]
    ready_queue = []  # Priority queue to store processes based on remaining burst time
    gantt_chart = []

    while remaining_processes or ready_queue:
        # Add arriving processes to the ready queue
        for process in remaining_processes:
            if process.arrival_time <= current_time:
                heapq.heappush(ready_queue, (process.burst_time, process.pid, process))
                remaining_processes.remove(process)

        if ready_queue:
            burst_time, pid, selected_process = heapq.heappop(ready_queue)
            if selected_process.first_exe is None:  # Assign first_exe if it's None
                selected_process.first_exe = max(current_time, selected_process.arrival_time)
            start_time = max(current_time, selected_process.arrival_time)
            end_time = start_time + 1  # Execute the process for 1 unit time
            gantt_chart.append((start_time, end_time, pid))
            selected_process.burst_time -= 1

            if selected_process.burst_time > 0:
                heapq.heappush(ready_queue, (selected_process.burst_time, pid, selected_process))
            else:
                selected_process.completion_time = end_time
            current_time = end_time
        else:
            current_time += 1

    return processes, gantt_chart


def run_sjf_preemptive():
    global processes
    processes, gantt_chart = sjf_preemptive(processes)
    avg_turnaround_time = compute_avg_turnaround_time(processes)
    avg_waiting_time = compute_avg_waiting_time(processes)
    avg_response_time = compute_avg_response_time(processes)
    draw_gantt_chart(gantt_chart, avg_turnaround_time, avg_waiting_time, avg_response_time)


# Round robin
def round_robin(processes, time_quantum):
    gantt_chart = []
    remaining_processes = processes[:]
    current_time = 0
    while remaining_processes:
        for process in remaining_processes[:]:  # Using slicing to allow removal of elements from the list while iterating
            if process.arrival_time <= current_time:
                start_time = max(current_time, process.arrival_time)
                if process.first_exe is None:
                    process.first_exe = start_time
                # Execute the process for the time quantum or until it finishes
                if process.burst_time <= time_quantum:
                    end_time = start_time + process.burst_time
                    process.burst_time = 0
                else:
                    end_time = start_time + time_quantum
                    process.burst_time -= time_quantum
                gantt_chart.append((start_time, end_time, process.pid))
                current_time = end_time
                if process.burst_time == 0:
                    process.completion_time = end_time
                    remaining_processes.remove(process)
            else:
                current_time += 1
    return processes, gantt_chart


def run_round_robin():
    global processes
    time_quantum = float(time_quantum_entry.get())
    processes, gantt_chart = round_robin(processes, time_quantum)
    avg_turnaround_time = compute_avg_turnaround_time(processes)
    avg_waiting_time = compute_avg_waiting_time(processes)
    avg_response_time = compute_avg_response_time(processes)
    draw_gantt_chart(gantt_chart, avg_turnaround_time, avg_waiting_time, avg_response_time)



def priority_preemptive(processes):
    current_time = 0
    remaining_processes = processes[:]
    ready_queue = []  # Priority queue to store processes based on priority
    gantt_chart = []

    while remaining_processes or ready_queue:
        # Add arriving processes to the ready queue
        for process in remaining_processes:
            if process.arrival_time <= current_time:
                heapq.heappush(ready_queue, (process.priority, process.pid, process))
                remaining_processes.remove(process)

        if ready_queue:
            priority, pid, selected_process = heapq.heappop(ready_queue)
            if selected_process.first_exe is None:  # Assign first_exe if it's None
                selected_process.first_exe = max(current_time, selected_process.arrival_time)
            start_time = max(current_time, selected_process.arrival_time)
            end_time = start_time + 1  # Execute the process for 1 unit time
            gantt_chart.append((start_time, end_time, pid))
            selected_process.burst_time -= 1

            if selected_process.burst_time > 0:
                heapq.heappush(ready_queue, (priority, pid, selected_process))
            else:
                selected_process.completion_time = end_time
            current_time = end_time
        else:
            current_time += 1

    return processes, gantt_chart


def run_priority_preemptive():
    global processes
    processes, gantt_chart = priority_preemptive(processes)
    avg_turnaround_time = compute_avg_turnaround_time(processes)
    avg_waiting_time = compute_avg_waiting_time(processes)
    avg_response_time = compute_avg_response_time(processes)
    draw_gantt_chart(gantt_chart, avg_turnaround_time, avg_waiting_time, avg_response_time)


def reset_all():
    # Clear all input
    pid_entry.delete(0, tk.END)
    arrival_time_entry.delete(0, tk.END)
    burst_time_entry.delete(0, tk.END)
    time_quantum_entry.delete(0, tk.END)
    time_quantum_entry.insert(0,2)
    priority_entry.delete(0,tk.END)
    # Clear processes list
    processes.clear()
    processes_listbox.delete(0, tk.END)


processes = []

# interface
root = tk.Tk()
root.title("CPU Scheduling")
root.resizable(False, False) 

frame = ttk.Frame(root)
frame.grid(row=0, column=0, padx=10, pady=10)

pid_label = ttk.Label(frame, text="PID:")
pid_label.grid(row=0, column=0, padx=5, pady=5)
pid_entry = ttk.Entry(frame)
pid_entry.grid(row=0, column=1, padx=5, pady=5)

arrival_time_label = ttk.Label(frame, text="Arrival Time:")
arrival_time_label.grid(row=1, column=0, padx=5, pady=5)
arrival_time_entry = ttk.Entry(frame)
arrival_time_entry.grid(row=1, column=1, padx=5, pady=5)

burst_time_label = ttk.Label(frame, text="Burst Time:")
burst_time_label.grid(row=2, column=0, padx=5, pady=5)
burst_time_entry = ttk.Entry(frame)
burst_time_entry.grid(row=2, column=1, padx=5, pady=5)


# optional var
time_quantum_label = ttk.Label(frame, text="Time quantum (RR):")
time_quantum_label.grid(row=3, column=0, padx=5, pady=5)
time_quantum_entry = ttk.Entry(frame)
time_quantum_entry.grid(row=3, column=1, padx=5, pady=5)
# make default for RR is 2 ms
time_quantum_entry.insert(0,2)

priority_label = ttk.Label(frame, text="Priority (priority preemptive):")
priority_label.grid(row=4, column=0, padx=5, pady=5)
priority_entry = ttk.Entry(frame)
priority_entry.grid(row=4, column=1, padx=5, pady=5)



# Button
add_button = ttk.Button(frame, text="Add Process", command=add_process)
add_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

processes_listbox = tk.Listbox(frame, width=60)
processes_listbox.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

run_fcfs_button = ttk.Button(frame, text="Run FCFS", command=run_fcfs)
run_fcfs_button.grid(row=7, column=0, columnspan=2, padx=5, pady=5)


run_sjf_button = ttk.Button(frame, text="Run SJF", command=run_sjf_preemptive)
run_sjf_button.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

run_rr_button = ttk.Button(frame, text="Round robin", command=run_round_robin)
run_rr_button.grid(row=9, column=0, columnspan=2, padx=5, pady=5)


run_pr_button = ttk.Button(frame, text="Priority preemptive", command=run_priority_preemptive)
run_pr_button.grid(row=10, column=0, columnspan=2, padx=5, pady=5)


reset_button = ttk.Button(frame, text="Reset All", command=reset_all)
reset_button.grid(row=11, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()