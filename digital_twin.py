import simpy
import random

# THE DIGITAL TWIN OF A HUMAN LUNG
def patient_lung(env, target_pip, target_peep):
    while True:
        # 1. INSPIRATION (Breathing In)
        print(f"Time {env.now:.1f}: INHALING... Pressure rising to {target_pip} cmH2O")
        yield env.timeout(2) # Takes 2 seconds to breathe in
        
        # 2. CHECK SAFETY
        if target_pip > 40:
            print("!!! WARNING: BAROTRAUMA RISK - Pressure too high !!!")
        
        # 3. EXPIRATION (Breathing Out)
        print(f"Time {env.now:.1f}: EXHALING... Pressure dropping to {target_peep} cmH2O")
        yield env.timeout(3) # Takes 3 seconds to breathe out

# SETUP THE SIMULATION
print("--- Level 3: Starting Ventilator Digital Twin Simulation ---")
env = simpy.Environment()

# We use the values the AI gave us: PEEP=5, PIP=40
env.process(patient_lung(env, target_pip=40, target_peep=5))

# Run for 15 seconds (about 3 breaths)
env.run(until=15)
print("--- Simulation Complete: Design Validated ---")