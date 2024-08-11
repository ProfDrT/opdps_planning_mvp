from typing import List, Dict
from datetime import datetime, timedelta
from src.data.schedule import Schedule

class Scheduler:
    def generate_daily_schedule(self, resources: List[Dict], appointments: List[Dict]):
        # Simple scheduling algorithm (can be improved with more complex logic)
        daily_schedule = []
        current_time = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)  # Start at 9:00 AM
        end_time = current_time.replace(hour=17, minute=0)  # End at 5:00 PM

        for appointment in appointments:
            if current_time >= end_time:
                break

            patient = appointment['patient']
            staff = self._find_available_resource(resources, 'staff', current_time)
            equipment = self._find_available_resource(resources, 'equipment', current_time)

            if staff and equipment:
                duration = timedelta(minutes=30)  # Assume 30-minute appointments
                daily_schedule.append({
                    'time': current_time,
                    'patient': patient,
                    'staff': staff,
                    'equipment': equipment
                })
                current_time += duration
                self._update_resource_availability(staff, current_time, duration)
                self._update_resource_availability(equipment, current_time, duration)
            else:
                # Handle case when resources are not available
                daily_schedule.append({
                    'time': current_time,
                    'patient': patient,
                    'staff': None,
                    'equipment': None
                })
                current_time += timedelta(minutes=15)  # Move to next 15-minute slot

        return Schedule(datetime.now().date(), daily_schedule)

    def _find_available_resource(self, resources: List[Dict], resource_type: str, current_time: datetime):
        for resource in resources:
            if resource['type'] == resource_type and self._is_resource_available(resource, current_time):
                return resource
        return None

    def _is_resource_available(self, resource: Dict, current_time: datetime):
        return resource['availability'].get(current_time.strftime('%H:%M'), True)

    def _update_resource_availability(self, resource: Dict, start_time: datetime, duration: timedelta):
        end_time = start_time + duration
        current = start_time
        while current < end_time:
            resource['availability'][current.strftime('%H:%M')] = False
            current += timedelta(minutes=15)