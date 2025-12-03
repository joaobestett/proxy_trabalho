import csv
import matplotlib.pyplot as plt

timestamps = []
rtts = []
jitters = []
throughputs = []
goodputs = []
retrans = []
cwnds = []

with open("logs/metrics.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        timestamps.append(float(row["timestamp"]))
        rtts.append(float(row["rtt"]))
        jitters.append(float(row["jitter"]))
        throughputs.append(float(row["throughput"]))
        goodputs.append(float(row["goodput"]))
        retrans.append(float(row["retransmissions"]))
        cwnds.append(float(row["cwnd"]))

def plot(title, values, ylabel):
    plt.figure()
    plt.plot(timestamps, values)
    plt.title(title)
    plt.xlabel("Tempo")
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.show()

plot("RTT", rtts, "ms")
plot("Jitter", jitters, "ms")
plot("Throughput", throughputs, "bytes/s")
plot("Goodput", goodputs, "bytes")
plot("Retransmissions", retrans, "count")
plot("CWND Estimada", cwnds, "packets")
