from typing import List, Dict
from src.data.staff import Staff

class WorkloadDistributor:
    def distribute_workload(self, staff: List[Staff], tasks: List[Dict]):
        # Simple workload distribution algorithm (can be improved with more complex logic)
        distributed_tasks = []
        staff_workload = {s.id: 0 for s in staff}

        for task in tasks:
            available_staff = [s for s in staff if s.availability]
            if not available_staff:
                # Handle case when no staff is available
                distributed_tasks.append({
                    'task': task,
                    'assigned_to': None
                })
                continue

            # Assign task to the staff member with the lowest current workload
            assigned_staff = min(available_staff, key=lambda s: staff_workload[s.id])
            distributed_tasks.append({
                'task': task,
                'assigned_to': assigned_staff
            })
            staff_workload[assigned_staff.id] += task.get('duration', 1)  # Assume default duration of 1 if not specified

            # Update staff availability based on workload
            if staff_workload[assigned_staff.id] >= 8:  # Assume 8 hours is full workload
                assigned_staff.availability = False

        return distributed_tasks

    def get_staff_workload(self, staff: List[Staff], distributed_tasks: List[Dict]):
        workload = {s.id: 0 for s in staff}
        for task in distributed_tasks:
            if task['assigned_to']:
                workload[task['assigned_to'].id] += task['task'].get('duration', 1)
        return workload