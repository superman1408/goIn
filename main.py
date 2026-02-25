# 1. Create environment
# 2. Create resource
# 3. Define process
# 4. Store metrics
# 5. Run simulation
# 6. Convert to DataFrame
# 7. Calculate statistics
# 8. Print results

import simpy
import pandas as pd
import random



result = []



def ship_sim(env, name, stage):
    arrival_time = env.now
    print(f"At {arrival_time} units time {name} arriving at stage")
    
    with stage.request() as req:
        yield req
        
        start_time = env.now
        waiting_time = start_time - arrival_time
        print(f"{name} started at {start_time} unit time after waiting for {waiting_time} units time")
        
        duration = random.randint(5, 10)
        yield env.timeout(duration)
        
        finish_time = env.now
        process_time = finish_time - start_time
        total_time = finish_time - arrival_time
        print(f"{name} finished at {finish_time} units time after processing for {process_time} units time and total time in system is {total_time} units time")
        result.append({
            "Ship": name,
            "Arrival Time": arrival_time,
            "Start Time": start_time,
            "Waiting Time": waiting_time,
            "finish Time": finish_time,
            "Processing Time": process_time,
            "Total Time in System": total_time
        })
        

env = simpy.Environment()
stage = simpy.Resource(env, capacity=1)


def generator(env, stage, n):
    for i in range(n):
        yield env.timeout(random.randint(1, 5)) # Random arrival time
        env.process(ship_sim(env, f"Ship-{i+1}", stage))
        

env.process(generator(env, stage, 5))
    
env.run()


# Convert results to DataFrame
print("-------------Simulation Results:------------------------")
print(result)
df = pd.DataFrame(result)
print(df)