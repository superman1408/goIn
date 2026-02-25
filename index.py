import simpy
import random
import pandas as pd


result = []


def ship(env, name, machine):
    arrival_time = env.now
    print(f"{arrival_time} time {name} arriving at the machine")
    
    with machine.request() as request:
        yield request
        
        start_time = env.now
        waiting_time = start_time - arrival_time
        print(f"{name} started at {start_time} after waiting for {waiting_time} time units")
        
        duration = random.randint(5, 10)
        yield env.timeout(duration)
        
        finish_time = env.now
        process_time = finish_time - start_time
        total_time = finish_time - arrival_time
        
        
        print(f"{name} finished at {finish_time} after processing for {process_time} time units and total time in system is {total_time} time units")
        
        # Store Statistics
        result.append({
            "Ship": name,
            "Arrival Time": arrival_time,
            "Start Time": start_time,
            "Finish Time": finish_time,
            "Waiting Time": waiting_time,
            "Processing Time": process_time,
            "Total Time in System": total_time
        })
        
    print(f"Current Machine Utilization: {sum([r['Processing Time'] for r in result]) / env.now:.2f}")
    print(result)




env = simpy.Environment()

machine = simpy.Resource(env, capacity=2)

for i in range(5):
    env.process(ship(env, f"Ship-{i+1}", machine))
    
env.run()





# -----------Real time  simulation with data collection-------------
# we must collect
# Waiting time
# Processing time
# Total time in system
# Resource utilization
# Throughput

# Inputs Required:
# Number of ships
# Arrival times of ships
# start time and finish time of each ship
# Finish Time of the simulation


# Calculations:
# Waiting times = start time - arrival time
# Processing times = finish time - start time
# Total time in system = finish time - arrival time
# Resource utilization = total processing time / total simulation time
# Throughput = number of ships processed / total simulation time


# Convert to a DataFrame for better visualization and analysis:

df = pd.DataFrame(result)

total_processing_time = df["Processing Time"].sum()
simulation_time = env.now

utilization = total_processing_time / simulation_time

print("Machine Utilization:", round(utilization, 2))
print("\n-------Simulation Results-------")
print(df)

# Calculate and display overall statistics
average_waiting_time = df["Waiting Time"].mean()
average_processing_time = df["Processing Time"].mean()
total_processing_time = df["Processing Time"].sum()
total_simulation_time = df["Finish Time"].max()
resource_utilization = total_processing_time / total_simulation_time if total_simulation_time > 0 else 0
throughput = len(df) / total_simulation_time if total_simulation_time > 0 else 0

total_processing_time = df["Processing Time"].sum()
simulation_time = env.now
utilization = total_processing_time / simulation_time

print("Machine Utilization:", utilization)

print(f"\nAverage Waiting Time: {average_waiting_time:.2f}")
print(f"Average Processing Time: {average_processing_time:.2f}")
print(f"Resource Utilization: {resource_utilization:.2f}")
print(f"Throughput: {throughput:.2f} ships per time unit")

print("\n-------Detailed Ship Statistics-------")
print("Average Total time:", df["Total Time in System"].mean())