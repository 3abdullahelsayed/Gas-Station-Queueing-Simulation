import numpy as np
import matplotlib.pyplot as plt
import random as random
import pandas as pd

def simulation(num_cars, print_table=False):
    # Set random seed for reproducibility (commented out as in original)
    # random.seed(100)
   
    # Calculate type and service time for the first car
    random_value_type = random.random()
    if random_value_type > 0.55:
        car_type = 'A'
    elif random_value_type > 0.2:
        car_type = 'B'
    else:
        car_type = 'C'  
    
    # Determine service time for the first car based on its type
    random_value_service = random.random()
    if car_type == 'C':
        if random_value_service > 0.50:
            service_duration = 7
        elif random_value_service > 0.20:
            service_duration = 5
        else:
            service_duration = 3            
    else:
        if random_value_service > 0.50:
            service_duration = 3
        elif random_value_service > 0.20:
            service_duration = 2
        else:
            service_duration = 1

    # Initialize lists to store simulation data
    car_types = [car_type]
    inter_arrival_times = [0]
    clock_times = [0]
    service_times = [service_duration]
    pump95_starts = [0]
    pump95_ends = []
    pump90_starts = [0]
    pump90_ends = []
    gas_starts = [0]
    gas_ends = []
    waiting_times_pump95 = [0]
    cars_in_queue_pump95 = []
    waiting_times_pump90 = [0]
    cars_in_queue_pump90 = []
    waiting_times_gas = [0]
    cars_in_queue_gas = []
    idle_times_pump95 = [0]
    idle_times_pump90 = [0]
    idle_times_gas = [0]
    gas_iterations = [0]
    pump95_iterations = [0]
    pump90_iterations = [0]
    count_car_a = 0
    count_car_b = 0
    count_car_c = 0

    # Handle first car's pump assignment and queue
    if car_type == 'A':
        count_car_a += 1
        pump95_ends.append(service_duration)
        pump90_ends.append(0)
        gas_ends.append(0)
        cars_in_queue_pump95.append(1)
        cars_in_queue_pump90.append(0)
        cars_in_queue_gas.append(0)
    elif car_type == 'B':
        count_car_b += 1
        pump95_ends.append(0)
        pump90_ends.append(service_duration)
        gas_ends.append(0)
        cars_in_queue_pump95.append(0)
        cars_in_queue_pump90.append(1)
        cars_in_queue_gas.append(0)
    else:
        count_car_c += 1
        pump95_ends.append(0)
        pump90_ends.append(0)
        gas_ends.append(service_duration)        
        cars_in_queue_pump95.append(0)
        cars_in_queue_pump90.append(0)
        cars_in_queue_gas.append(1)

    # Simulate remaining cars
    i = 1
    while i < num_cars:
        # Determine car type
        random_value_type = random.random()
        if random_value_type > 0.55:
            car_types.append('C')
            count_car_c += 1
        elif random_value_type > 0.2:
            car_types.append('B')
            count_car_b += 1
        else:
            car_types.append('A')
            count_car_a += 1    

        # Calculate inter-arrival time
        random_value_arrival = random.random()
        if random_value_arrival > 0.65:
            inter_arrival_times.append(3)
        elif random_value_arrival > 0.40:
            inter_arrival_times.append(2)
        elif random_value_arrival > 0.17:
            inter_arrival_times.append(1)
        else:
            inter_arrival_times.append(0)

        # Update clock time
        clock_times.append(clock_times[i-1] + inter_arrival_times[-1])

        # Determine service time based on car type
        random_value_service = random.random()
        if car_types[-1] == 'C':
            if random_value_service > 0.50:
                service_times.append(7)
            elif random_value_service > 0.20:
                service_times.append(5)
            else:
                service_times.append(3)            
        else:
            if random_value_service > 0.50:
                service_times.append(3)
            elif random_value_service > 0.20:
                service_times.append(2)
            else:
                service_times.append(1)

        # Assign pump 95 start time
        random_value_pump = random.random()
        if car_types[-1] == 'A':
            pump95_starts.append(max(clock_times[i], max(pump95_ends)))
        elif car_types[-1] == 'B' and cars_in_queue_pump90[i-1] > 3:
            if random_value_pump > 0.4:
                pump95_starts.append(max(clock_times[i], max(pump95_ends)))  
            else:
                pump95_starts.append(0)
        else:
            pump95_starts.append(0)            

        # Calculate pump 95 end time
        if pump95_starts[i] > 0 and i > 1:
            pump95_ends.append(pump95_starts[i] + service_times[i])
        else:
            pump95_ends.append(pump95_ends[i-1])

        # Assign pump 90 start time
        random_value_pump90 = random.random()
        if car_types[-1] == 'B':
            if cars_in_queue_pump90[-1] > 3:
                if random_value_pump <= 0.4:
                    pump90_starts.append(max(clock_times[i], max(pump90_ends)))
                else:
                    pump90_starts.append(0)
            else:
                pump90_starts.append(max(clock_times[i], max(pump90_ends)))
        elif car_types[-1] == 'C':
            if cars_in_queue_gas[-1] > 4:
                if random_value_pump90 > 0.60:
                    pump90_starts.append(max(clock_times[i], max(pump90_ends)))
                else:
                    pump90_starts.append(0)
            else:
                pump90_starts.append(0)  
        else:
            pump90_starts.append(0)              

        # Calculate pump 90 end time
        if pump90_starts[-1] > 0 and i > 1:
            pump90_ends.append(pump90_starts[-1] + service_times[-1])
        else:
            pump90_ends.append(pump90_ends[i-1])

        # Assign gas pump start time
        if car_types[i] == 'C':
            if cars_in_queue_gas[i-1] > 4:
                if random_value_pump90 <= 0.6:
                    gas_starts.append(max(clock_times[i], max(gas_ends)))
                else:
                    gas_starts.append(0)
            else:
                gas_starts.append(max(clock_times[i], max(gas_ends)))
        else:
            gas_starts.append(0)        

        # Calculate gas pump end time
        if gas_starts[-1] > 0:
            gas_ends.append(gas_starts[-1] + service_times[-1])
        else:
            gas_ends.append(gas_ends[i-1])

        # Calculate waiting time in pump 95 queue
        if pump95_starts[-1] > 0:
            waiting_times_pump95.append(pump95_starts[-1] - clock_times[-1])
        else:
            waiting_times_pump95.append(0)

        # Calculate waiting time in pump 90 queue
        if pump90_starts[-1] > 0:
            waiting_times_pump90.append(pump90_starts[-1] - clock_times[-1])
        else:
            waiting_times_pump90.append(0)

        # Calculate waiting time in gas queue
        if gas_starts[-1] > 0:
            waiting_times_gas.append(gas_starts[i] - clock_times[i])
        else:
            waiting_times_gas.append(0)

        # Calculate number of cars in pump 95 queue
        if waiting_times_pump95[i] > 1:
            if waiting_times_pump95[i] > service_times[pump95_iterations[-1]]:
                remaining_time = waiting_times_pump95[i]
                queue_count = 0
                offset = 1
                while remaining_time > 0 and i - offset > 0:
                    if pump95_starts[i-offset] > 0:
                        remaining_time -= service_times[i-offset]
                        if remaining_time >= 0:
                            queue_count += 1
                        offset += 1
                    else:
                        offset += 1
                cars_in_queue_pump95.append(queue_count + 2)
            else:
                cars_in_queue_pump95.append(cars_in_queue_pump95[i-1] + 1)    
        elif pump95_starts[i] > 0:
            cars_in_queue_pump95.append(1)
        else:
            cars_in_queue_pump95.append(0)

        # Calculate number of cars in pump 90 queue
        if waiting_times_pump90[i] > 1:
            if waiting_times_pump90[i] > service_times[pump90_iterations[-1]]:
                remaining_time = waiting_times_pump90[i]
                queue_count = 0
                offset = 1
                while remaining_time > 0 and i - offset > 0:
                    if pump90_starts[i-offset] > 0:
                        remaining_time -= service_times[i-offset]
                        if remaining_time >= 0:
                            queue_count += 1
                        offset += 1
                    else:
                        offset += 1
                cars_in_queue_pump90.append(queue_count + 2)
            else:
                cars_in_queue_pump90.append(cars_in_queue_pump90[i-1] + 1)
        elif pump90_starts[i] > 0:
            cars_in_queue_pump90.append(1)
        else:
            cars_in_queue_pump90.append(0)

        # Calculate number of cars in gas queue
        if waiting_times_gas[i] > 1:
            if waiting_times_gas[i] > service_times[gas_iterations[-1]]:
                remaining_time = waiting_times_gas[i]
                queue_count = 0
                offset = 1
                while remaining_time > 0 and i - offset > 0:
                    if gas_starts[i-offset] > 0:
                        remaining_time -= service_times[i-offset]
                        if remaining_time >= 0:
                            queue_count += 1
                        offset += 1
                    else:
                        offset += 1
                cars_in_queue_gas.append(queue_count + 2)
            else:
                cars_in_queue_gas.append(cars_in_queue_gas[i-1] + 1)
        elif gas_starts[i] > 0:
            cars_in_queue_gas.append(1)
        else:
            cars_in_queue_gas.append(0)

        # Calculate idle time for pump 95
        if pump95_starts[i] == 0:
            idle_times_pump95.append(0)
        else:
            idle_times_pump95.append(pump95_starts[i] - pump95_ends[i-1])

        # Calculate idle time for pump 90
        if pump90_starts[i] == 0:
            idle_times_pump90.append(0)
        else:
            idle_times_pump90.append(pump90_starts[i] - pump90_ends[i-1])

        # Calculate idle time for gas pump
        if gas_starts[i] == 0:
            idle_times_gas.append(0)
        else:
            idle_times_gas.append(gas_starts[i] - gas_ends[i-1])

        # Track iterations for gas pump
        if car_types[i] == 'C':
            gas_iterations.append(i)
        else:
            gas_iterations.append(gas_iterations[i-1])        

        # Track iterations for pump 95
        if car_types[i] == 'A':
            pump95_iterations.append(i)
        else:
            pump95_iterations.append(pump95_iterations[i-1])        

        # Track iterations for pump 90
        if car_types[i] == 'B':
            pump90_iterations.append(i)
        else:
            pump90_iterations.append(pump90_iterations[i-1])        

        i += 1

    # Generate and save table if print_table is True
    if print_table:
        table = pd.DataFrame()
        table['CarType'] = car_types
        table['Service Time'] = service_times
        table['IAT'] = inter_arrival_times
        table['Clock Time'] = clock_times
        table['p95begins'] = pump95_starts
        table['p95Ends'] = pump95_ends
        table['p90begins'] = pump90_starts
        table['p90Ends'] = pump90_ends
        table['pgasbegins'] = gas_starts
        table['pgasEnds'] = gas_ends
        table['WTInQ95'] = waiting_times_pump95
        table['#OfcarsInQ95'] = cars_in_queue_pump95
        table['WTInQ90'] = waiting_times_pump90
        table['#OfcarsInQ90'] = cars_in_queue_pump90
        table['WTInQgas'] = waiting_times_gas
        table['#OfcarsInQgas'] = cars_in_queue_gas
        table['idle95'] = idle_times_pump95
        table['idle90'] = idle_times_pump90
        table['idle Time gas'] = idle_times_gas
    
        # Remove truncation limits for large dataframes
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        file_name = input("Enter the name of csv file: ")
        table.to_csv(file_name + ".csv", index=False)

    # Calculate metrics for the simulation run
    pump95_count = np.count_nonzero(pump95_starts)
    if pump95_count == 0:
        pump95_count = 1

    average_service_time = np.mean(service_times)
    average_waiting_time_pump95 = sum(waiting_times_pump95) / pump95_count
    average_waiting_time_pump90 = sum(waiting_times_pump90) / np.count_nonzero(pump90_starts)
    average_waiting_time_gas = sum(waiting_times_gas) / np.count_nonzero(gas_starts)
    total_average_waiting_time = (average_waiting_time_pump95 + average_waiting_time_pump90 + average_waiting_time_gas) / 3
    max_queue_length_pump95 = max(cars_in_queue_pump95)
    max_queue_length_pump90 = max(cars_in_queue_pump90)
    max_queue_length_gas = max(cars_in_queue_gas)
    probability_wait_pump95 = np.count_nonzero(waiting_times_pump95) / pump95_count
    probability_wait_pump90 = np.count_nonzero(waiting_times_pump90) / np.count_nonzero(pump90_starts)
    probability_wait_gas = np.count_nonzero(waiting_times_gas) / np.count_nonzero(gas_starts)
    portion_idle_time_pump95 = (np.count_nonzero(idle_times_pump95) / pump95_count) * 100
    portion_idle_time_pump90 = (np.count_nonzero(idle_times_pump90) / np.count_nonzero(pump90_starts)) * 100
    portion_idle_time_gas = (np.count_nonzero(idle_times_gas) / np.count_nonzero(gas_starts)) * 100
    average_inter_arrival_time = np.mean(inter_arrival_times)
    percent_car_a = (count_car_a / num_cars) * 100
    percent_car_b = (count_car_b / num_cars) * 100
    percent_car_c = (count_car_c / num_cars) * 100

    return {
        'AST': average_service_time,
        'AWT95': average_waiting_time_pump95,
        'AWT90': average_waiting_time_pump90,
        'AWTgas': average_waiting_time_gas,
        'TAWT': total_average_waiting_time,
        'MQ95': max_queue_length_pump95,
        'MQ90': max_queue_length_pump90,
        'MQgas': max_queue_length_gas,
        'PCW95': probability_wait_pump95,
        'PCW90': probability_wait_pump90,
        'PCWgas': probability_wait_gas,
        'PIT95': portion_idle_time_pump95,
        'PIT90': portion_idle_time_pump90,
        'PITgas': portion_idle_time_gas,
        'AEAT': average_inter_arrival_time,
        'carA': percent_car_a,
        'carB': percent_car_b,
        'carC': percent_car_c,
    }

# Run simulation multiple times and collect results
num_runs = int(input("Enter number of runs to perform: "))
num_cars = int(input("Enter number of cars for each run: "))
total_runs = num_runs

average_service_times = []
average_waiting_times_pump95 = []
average_waiting_times_pump90 = []
average_waiting_times_gas = []
total_average_waiting_times = []
max_queue_lengths_pump95 = []
max_queue_lengths_pump90 = []
max_queue_lengths_gas = []
probabilities_wait_pump95 = []
probabilities_wait_pump90 = []
probabilities_wait_gas = []
portions_idle_pump95 = []
portions_idle_pump90 = []
portions_idle_gas = []
average_inter_arrival_times = []
percentages_car_a = []
percentages_car_b = []
percentages_car_c = []

while num_runs > 0:
    result = simulation(num_cars)
    average_service_times.append(result['AST'])
    average_waiting_times_pump95.append(result['AWT95'])
    average_waiting_times_pump90.append(result['AWT90'])
    average_waiting_times_gas.append(result['AWTgas'])
    total_average_waiting_times.append(result['TAWT'])
    max_queue_lengths_pump95.append(result['MQ95'])
    max_queue_lengths_pump90.append(result['MQ90'])
    max_queue_lengths_gas.append(result['MQgas'])
    probabilities_wait_pump95.append(result['PCW95'])
    probabilities_wait_pump90.append(result['PCW90'])
    probabilities_wait_gas.append(result['PCWgas'])
    portions_idle_pump95.append(result['PIT95'])
    portions_idle_pump90.append(result['PIT90'])
    portions_idle_gas.append(result['PITgas'])
    average_inter_arrival_times.append(result['AEAT'])
    percentages_car_a.append(result['carA'])
    percentages_car_b.append(result['carB'])
    percentages_car_c.append(result['carC'])
    num_runs -= 1    

# Calculate averages across all runs
avg_service_time = sum(average_service_times) / total_runs
avg_waiting_time_pump95 = sum(average_waiting_times_pump95) / total_runs
avg_waiting_time_pump90 = sum(average_waiting_times_pump90) / total_runs
avg_waiting_time_gas = sum(average_waiting_times_gas) / total_runs
avg_total_waiting_time = sum(total_average_waiting_times) / total_runs
avg_max_queue_pump95 = sum(max_queue_lengths_pump95) / total_runs
avg_max_queue_pump90 = sum(max_queue_lengths_pump90) / total_runs
avg_max_queue_gas = sum(max_queue_lengths_gas) / total_runs
avg_prob_wait_pump95 = sum(probabilities_wait_pump95) / total_runs
avg_prob_wait_pump90 = sum(probabilities_wait_pump90) / total_runs
avg_prob_wait_gas = sum(probabilities_wait_gas) / total_runs
avg_portion_idle_pump95 = sum(portions_idle_pump95) / total_runs
avg_portion_idle_pump90 = sum(portions_idle_pump90) / total_runs
avg_portion_idle_gas = sum(portions_idle_gas) / total_runs
avg_inter_arrival_time = sum(average_inter_arrival_times) / total_runs
avg_percent_car_a = sum(percentages_car_a) / total_runs
avg_percent_car_b = sum(percentages_car_b) / total_runs
avg_percent_car_c = sum(percentages_car_c) / total_runs

# Theoretical values for comparison
theoretical_service_time = 3.75
theoretical_inter_arrival_time = 1.78

# Print simulation results
print('The Experimental average service time of cars in the three categories:', avg_service_time)
print('The Theoretical average service time of cars in the three categories:', theoretical_service_time)    
print("The average waiting time in the queues for pump 95:", avg_waiting_time_pump95)
print("The average waiting time in the queues for pump 90:", avg_waiting_time_pump90)
print('The average waiting time in the queues for pump gas:', avg_waiting_time_gas)    
print("The average waiting time for all cars:", avg_total_waiting_time)
print("The maximum queue length for pump 95:", avg_max_queue_pump95)
print('The maximum queue length for pump 90:', avg_max_queue_pump90)    
print("The maximum queue length for pump gas:", avg_max_queue_gas)
print("The probability that a car waits for pump 95:", avg_prob_wait_pump95)
print('The probability that a car waits for pump 90:', avg_prob_wait_pump90)    
print("The probability that a car waits for pump gas:", avg_prob_wait_gas)
print("The portion of idle time of pump 95:", avg_portion_idle_pump95, "%")
print('The portion of idle time of pump 90:', avg_portion_idle_pump90, "%")    
print("The portion of idle time of pump gas:", avg_portion_idle_gas, "%")
print("Experimental Average inter-arrival time:", avg_inter_arrival_time)
print('Theoretical average inter-arrival time:', theoretical_inter_arrival_time)
print('The portion of Car A in all cars:', avg_percent_car_a, "%")
print('The portion of Car B in all cars:', avg_percent_car_b, "%")
print('The portion of Car C in all cars:', avg_percent_car_c, "%")
print('Based on The portion of Car C in all cars which is:', avg_percent_car_c, '%', 
      'the biggest portion and The average waiting time in the queues for pump gas which is:', avg_waiting_time_gas,
      'which cause this value of total average waiting time:', avg_total_waiting_time, 
      "and the service time may be 7m or 5m or 3m", 
      "so if we want to minimize total average waiting time we need to add pump gas")

# Plot histograms for key metrics
plt.hist(average_inter_arrival_times, bins=10)
plt.title('Inter-Arrival Time')
plt.show()

plt.hist(average_service_times, bins=10)
plt.title('Service Time')
plt.show()

plt.hist(total_average_waiting_times, bins=10)
plt.title('Average Waiting Time for All Cars')
plt.show()