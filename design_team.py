import os
from crewai import Agent, Task, Crew, LLM

# 1. STOP CREWAI FROM LOOKING FOR OPENAI
os.environ["OPENAI_API_KEY"] = "NA"

# 2. CONFIGURE THE LOCAL BRAIN (Ollama)
# We use the CrewAI LLM class directly - this is the most reliable way.
my_local_brain = LLM(
    model="ollama/phi3",
    base_url="http://localhost:11434"
)

# 3. DEFINE THE EXPERTS
doctor = Agent(
  role='Medical Ventilator Specialist',
  goal='Define the required air pressure (PEEP/PIP) for a patient.',
  backstory='Expert in pulmonary medicine. You ensure settings are safe for lungs.',
  llm=my_local_brain, # Use the local brain
  verbose=True,
  allow_delegation=False
)

engineer = Agent(
  role='Pneumatic Engineer',
  goal='Select mechanical parts (valves/sensors) based on medical rules.',
  backstory='Expert in medical hardware and sensors.',
  llm=my_local_brain, # Use the local brain
  verbose=True,
  allow_delegation=False
)

# 4. DEFINE THE TASKS
task1 = Task(
  description='Analyze the ventilator rules and define PEEP and PIP limits.',
  expected_output='A report with PEEP (5 cmH2O) and PIP (max 40 cmH2O) limits.',
  agent=doctor
)

task2 = Task(
  description='Pick a sensor like MPX5010DP that fits these pressure limits.',
  expected_output='A technical recommendation of a sensor.',
  agent=engineer
)

# 5. START THE TEAM WORK
crew = Crew(
  agents=[doctor, engineer],
  tasks=[task1, task2]
)

print("--- Level 2: Design Team is starting work (Local Only) ---")
result = crew.kickoff()
print("\n########################\n## FINAL DESIGN OUTPUT ##\n########################\n")
print(result)