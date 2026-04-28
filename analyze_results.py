import pandas as pd
import matplotlib.pyplot as plt

def generate_report(csv_file):
    df = pd.read_csv(csv_file)
    
    plt.figure(figsize=(10, 6))
    plt.plot(df['User Count'], df['Median Response Time'], label='Median Latency')
    plt.plot(df['User Count'], df['95%'], label='P95 (Tail Latency)', linestyle='--')
    
    plt.title('Supply Chain API: Latency vs. Concurrency')
    plt.xlabel('Number of Concurrent Users')
    plt.ylabel('Response Time (ms)')
    plt.legend()
    plt.grid(True)
    plt.savefig('scalability_results.png')
    print("Report saved as scalability_results.png")

# Run this after your Locust test finishes
# generate_report('your_locust_stats_history.csv')