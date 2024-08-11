from flask import Flask, jsonify
from src.api.routes import api
from src.ui.views import ui
from src.models.resource_allocator import ResourceAllocator
from src.models.scheduler import Scheduler
from src.models.workload_distributor import WorkloadDistributor
from src.models.rl_model import RLModel
from src.data.staff import Staff
from src.data.patient import Patient
from src.data.equipment import Equipment
import random
import logging
from logging.handlers import RotatingFileHandler
import os

app = Flask(__name__)
app.register_blueprint(api)
app.register_blueprint(ui)

# Set up logging
if not os.path.exists('logs'):
    os.mkdir('logs')
file_handler = RotatingFileHandler('logs/opdps.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.logger.info('OPDPS startup')

# Initialize models
resource_allocator = ResourceAllocator()
scheduler = Scheduler()
workload_distributor = WorkloadDistributor()
rl_model = RLModel(state_size=1000, action_size=10)  # Adjust sizes as needed

# Simulate data
staff = [Staff(i, f"Staff {i}", "Doctor" if i % 3 == 0 else "Nurse", True) for i in range(10)]
patients = [Patient(i, f"Patient {i}", f"2023-05-{i+1:02d} 09:00") for i in range(20)]
equipment = [Equipment(i, f"Equipment {i}", True) for i in range(5)]

@app.route('/simulate')
def simulate():
    try:
        # 1. Allocate resources
        allocations = resource_allocator.allocate_resources(staff, patients, equipment)
        app.logger.info(f"Resources allocated: {len(allocations)} allocations made")

        # 2. Generate schedule
        schedule = scheduler.generate_daily_schedule(allocations, [{'patient': p} for p in patients])
        app.logger.info(f"Schedule generated: {len(schedule.assignments)} assignments")

        # 3. Distribute workload
        tasks = [{'id': i, 'duration': random.randint(1, 4)} for i in range(len(patients))]
        distributed_tasks = workload_distributor.distribute_workload(staff, tasks)
        app.logger.info(f"Workload distributed: {len(distributed_tasks)} tasks assigned")

        # 4. Use RL model to optimize (simplified for demonstration)
        state = {
            'staff_available': sum(1 for s in staff if s.availability),
            'patients_waiting': len(patients)
        }
        action = rl_model.predict(state)
        app.logger.info(f"RL model prediction: action {action}")

        return jsonify({
            'allocations': [{'patient': a['patient'].name, 'staff': a['staff'].name if a['staff'] else None, 'equipment': a['equipment'].type if a['equipment'] else None} for a in allocations],
            'schedule': [{'time': s['time'].strftime('%H:%M'), 'patient': s['patient'].name, 'staff': s['staff']['name'] if s['staff'] else None, 'equipment': s['equipment']['type'] if s['equipment'] else None} for s in schedule.assignments],
            'distributed_tasks': [{'task_id': dt['task']['id'], 'assigned_to': dt['assigned_to'].name if dt['assigned_to'] else None} for dt in distributed_tasks],
            'rl_action': action
        })
    except Exception as e:
        app.logger.error(f"An error occurred during simulation: {str(e)}")
        return jsonify({'error': 'An internal error occurred'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)