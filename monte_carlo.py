#---------Now running the simulation for 1000 times to get more accurate statistics-----------------
import simpy
import pandas as pd
import random



def run_simulation():
    result = []
    
    def ship_sim(env, name, machine):
        arrival_time = env.now
        
        with machine.request() as req:
            yield req
            
            start_time = env.now
            waiting_time = start_time - arrival_time
            
            duration = random.randint(5, 10)
            yield env.timeout(duration)
            
            finish_time = env.now
            process_time = finish_time - start_time
            total_time = (finish_time - arrival_time) #--------or (waiting_time + process_time)
            
            result.append({
                "Ship": name,
                "Arrival time": arrival_time,
                "Start time": start_time,
                "Waiting time": waiting_time,
                "Finish time": finish_time,
                "Process time": process_time,
                "Total time": total_time
            })
            
            
    env = simpy.Environment()
    machine = simpy.Resource(env, capacity=2)
    
    # for i in range(5):
    #     env.process(ship_sim(env, f"Ship-{i+1}", machine))
    
    
    def generator(env, machine, n):
        for i in range(n):
            yield env.timeout(random.randint(5, 10))
            env.process(ship_sim(env, f"Ship-{i+1}", machine))
            
            
    env.process(generator(env, machine, 5))
    
    env.run()
    
    
    # ---------------Data Framework-----------------
    df = pd.DataFrame(result)
    
    #----------Calculation statistics for this RUN----------
    avg_wait = df["Waiting time"].mean()
    avg_total = df["Total time"].mean()
    total_processing = df["Process time"].sum()
    simulation_time = env.now
    utilization = total_processing / simulation_time
    throughput = len(df) / simulation_time
    
    return avg_wait, avg_total, utilization, throughput


runs = 100

all_avg_wait = []
all_avg_total = []
all_utilization = []
all_throughput = []


for i in range(runs):
    avg_wait, avg_total, utilization, throughput = run_simulation()
    
    all_avg_wait.append(avg_wait)
    all_avg_total.append(avg_total)
    all_utilization.append(utilization)
    all_throughput.append(throughput)
    


print("After 1000 Runs:")
print("Mean Waiting Time:", sum(all_avg_wait)/runs)
print("Mean Total Time:", sum(all_avg_total)/runs)
print("Mean Utilization:", sum(all_utilization)/runs)
print("Mean Throughput:", sum(all_throughput)/runs)
            