import streamlit as st
import numpy as np
import pandas as pd
from typing import List, Dict
from datetime import datetime, timedelta

# Data structures
class Staff:
    def __init__(self, id, name, role, availability):
        self.id = id
        self.name = name
        self.role = role
        self.availability = availability

class Patient:
    def __init__(self, id, name, appointment_time):
        self.id = id
        self.name = name
        self.appointment_time = appointment_time

class Equipment:
    def __init__(self, id, type, availability):
        self.id = id
        self.type = type
        self.availability = availability

class Schedule:
    def __init__(self, date, assignments):
        self.date = date
        self.assignments = assignments

# Core models
class ResourceAllocator:
    def allocate_resources(self, staff: List[Staff], patients: List[Patient], equipment: List[Equipment]):
        allocations = []
        for patient in patients:
            allocated_staff = next((s for s in staff if s.availability), None)
            allocated_equipment = next((e for e in equipment if e.availability), None)
            if allocated_staff and allocated_equipment:
                allocations.append({
                    'patient': patient,
                    'staff': allocated_staff,
                    'equipment': allocated_equipment
                })
                allocated_staff.availability = False
                allocated_equipment.availability = False
            else:
                allocations.append({
                    'patient': patient,
                    'staff': None,
                    'equipment': None
                })
        return allocations

class Scheduler:
    def generate_daily_schedule(self, resources: List[Dict], appointments: List[Dict]):
        daily_schedule = []
        current_time = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
        end_time = current_time.replace(hour=17, minute=0)

        for appointment in appointments:
            if current_time >= end_time:
                break

            patient = appointment['patient']
            staff = next((r for r in resources if r['staff'] and r['staff'].availability), None)
            equipment = next((r for r in resources if r['equipment'] and r['equipment'].availability), None)

            if staff and equipment:
                duration = timedelta(minutes=30)
                daily_schedule.append({
                    'time': current_time,
                    'patient': patient,
                    'staff': staff['staff'],
                    'equipment': equipment['equipment']
                })
                current_time += duration
                staff['staff'].availability = False
                equipment['equipment'].availability = False
            else:
                daily_schedule.append({
                    'time': current_time,
                    'patient': patient,
                    'staff': None,
                    'equipment': None
                })
                current_time += timedelta(minutes=15)

        return Schedule(datetime.now().date(), daily_schedule)

class WorkloadDistributor:
    def distribute_workload(self, staff: List[Staff], tasks: List[Dict]):
        distributed_tasks = []
        staff_workload = {s.id: 0 for s in staff}

        for task in tasks:
            available_staff = [s for s in staff if s.availability]
            if not available_staff:
                distributed_tasks.append({
                    'task': task,
                    'assigned_to': None
                })
                continue

            assigned_staff = min(available_staff, key=lambda s: staff_workload[s.id])
            distributed_tasks.append({
                'task': task,
                'assigned_to': assigned_staff
            })
            staff_workload[assigned_staff.id] += task.get('duration', 1)

            if staff_workload[assigned_staff.id] >= 8:
                assigned_staff.availability = False

        return distributed_tasks

class RLModel:
    def __init__(self, state_size: int, action_size: int):
        self.state_size = state_size
        self.action_size = action_size
        self.q_table = np.zeros((state_size, action_size))

    def predict(self, state: Dict) -> int:
        state_index = hash(frozenset(state.items())) % self.state_size
        return np.argmax(self.q_table[state_index])

# Streamlit app
st.title('OPDPS - Outpatient Department Planning System')

st.write("""
This MVP demonstrates the core functionality of resource allocation, scheduling, 
workload distribution, and reinforcement learning-based optimization for an 
outpatient department planning system.
""")

# Initialize models
resource_allocator = ResourceAllocator()
scheduler = Scheduler()
workload_distributor = WorkloadDistributor()
rl_model = RLModel(state_size=1000, action_size=10)

# Simulate data
staff = [Staff(i, f"Staff {i}", "Doctor" if i % 3 == 0 else "Nurse", True) for i in range(10)]
patients = [Patient(i, f"Patient {i}", f"2023-05-{i+1:02d} 09:00") for i in range(20)]
equipment = [Equipment(i, f"Equipment {i}", True) for i in range(5)]

if st.button('Run Simulation'):
    # 1. Allocate resources
    allocations = resource_allocator.allocate_resources(staff, patients, equipment)
    st.subheader('Resource Allocations')
    alloc_df = pd.DataFrame([(a['patient'].name, a['staff'].name if a['staff'] else 'N/A', a['equipment'].type if a['equipment'] else 'N/A') for a in allocations],
                            columns=['Patient', 'Staff', 'Equipment'])
    st.dataframe(alloc_df)

    # 2. Generate schedule
    schedule = scheduler.generate_daily_schedule(allocations, [{'patient': p} for p in patients])
    st.subheader('Daily Schedule')
    schedule_df = pd.DataFrame([(s['time'].strftime('%H:%M'), s['patient'].name, s['staff'].name if s['staff'] else 'N/A', s['equipment'].type if s['equipment'] else 'N/A') for s in schedule.assignments],
                               columns=['Time', 'Patient', 'Staff', 'Equipment'])
    st.dataframe(schedule_df)

    # 3. Distribute workload
    tasks = [{'id': i, 'duration': np.random.randint(1, 4)} for i in range(len(patients))]
    distributed_tasks = workload_distributor.distribute_workload(staff, tasks)
    st.subheader('Distributed Tasks')
    tasks_df = pd.DataFrame([(dt['task']['id'], dt['assigned_to'].name if dt['assigned_to'] else 'Unassigned') for dt in distributed_tasks],
                            columns=['Task ID', 'Assigned To'])
    st.dataframe(tasks_df)

    # 4. Use RL model to optimize (simplified for demonstration)
    state = {
        'staff_available': sum(1 for s in staff if s.availability),
        'patients_waiting': len(patients)
    }
    action = rl_model.predict(state)
    st.subheader('RL Model Action')
    st.write(f"The RL model suggested action: {action}")

st.write("""
This simulation demonstrates the basic functionality of the OPDPS. 
In a real-world scenario, the system would be more complex and would 
interact with real hospital data and systems.
""")