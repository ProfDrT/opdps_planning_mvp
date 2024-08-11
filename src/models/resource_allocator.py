from typing import List
from src.data.staff import Staff
from src.data.patient import Patient
from src.data.equipment import Equipment

class ResourceAllocator:
    def allocate_resources(self, staff: List[Staff], patients: List[Patient], equipment: List[Equipment]):
        # Simple allocation algorithm (can be improved with more complex logic)
        allocations = []
        
        for patient in patients:
            allocated_staff = self._find_available_staff(staff)
            allocated_equipment = self._find_available_equipment(equipment)
            
            if allocated_staff and allocated_equipment:
                allocations.append({
                    'patient': patient,
                    'staff': allocated_staff,
                    'equipment': allocated_equipment
                })
                allocated_staff.availability = False
                allocated_equipment.availability = False
            else:
                # Handle case when resources are not available
                allocations.append({
                    'patient': patient,
                    'staff': None,
                    'equipment': None
                })
        
        return allocations

    def _find_available_staff(self, staff: List[Staff]):
        for s in staff:
            if s.availability:
                return s
        return None

    def _find_available_equipment(self, equipment: List[Equipment]):
        for e in equipment:
            if e.availability:
                return e
        return None