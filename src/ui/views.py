from flask import Blueprint, render_template, current_app
import requests

ui = Blueprint('ui', __name__)

@ui.route('/schedule')
def view_schedule():
    try:
        # Make a request to the /simulate endpoint
        response = requests.get('http://localhost:5000/simulate')
        data = response.json()

        # Render the template with the simulation data
        return render_template('simulation_results.html',
                               allocations=data['allocations'],
                               schedule=data['schedule'],
                               distributed_tasks=data['distributed_tasks'],
                               rl_action=data['rl_action'])
    except Exception as e:
        current_app.logger.error(f"An error occurred while fetching simulation data: {str(e)}")
        return render_template('simulation_results.html', error="An error occurred while fetching simulation data.")

@ui.route('/')
def index():
    return render_template('index.html')