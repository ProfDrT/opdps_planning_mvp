# OPDPS Planning MVP

## Project Description
OPDPS (Outpatient Department Planning System) is a Python-based application for resource allocation and scheduling in hospital outpatient departments. This MVP demonstrates the core functionality of resource allocation, scheduling, workload distribution, and reinforcement learning-based optimization using a Streamlit app.

## Features
- Resource allocation
- Daily schedule generation
- Workload distribution
- Reinforcement learning model for optimization
- Interactive Streamlit interface for viewing results

## Installation
1. Clone the repository
2. Create a virtual environment:
   ```
   python3 -m venv venv
   ```
3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
1. Make sure you're in the project root directory (opdps_planning_mvp)
2. Run the Streamlit app:
   ```
   streamlit run main.py
   ```
3. Your default web browser should open automatically. If it doesn't, open a web browser and navigate to the URL displayed in the terminal (usually http://localhost:8501)

## Project Structure
- `main.py`: Contains the entire Streamlit app, including core models and simulation logic
- `requirements.txt`: List of Python dependencies
- `README.md`: Project documentation

## Components
1. ResourceAllocator: Assigns staff and equipment to patients
2. Scheduler: Generates daily schedules based on allocations
3. WorkloadDistributor: Distributes tasks among available staff
4. RLModel: Simple reinforcement learning model for optimization (placeholder for future development)

## Future Improvements
- Implement more sophisticated resource allocation and scheduling algorithms
- Enhance the reinforcement learning model with more complex state and action spaces
- Integrate with real hospital data systems
- Add more interactive features to the Streamlit app, such as custom input for staff, patients, and equipment
- Implement data persistence and historical analysis
- Add visualization of resource utilization and efficiency metrics

## License
[Add your chosen license here]

## Contributors
[Add contributor information here]