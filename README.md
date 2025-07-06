# ⛽ Gas Station Queueing Simulation

This project simulates a gas station queueing system using a **discrete-event simulation** approach in Python. It evaluates the performance of three fuel pumps (Pump 95, Pump 90, and Gas) serving three car types (A, B, C), across 100 runs with 30 cars per run.

---

## 📌 Executive Summary

- **Primary Insight**: The Gas pump is a major bottleneck due to high demand from Type C cars (46.1% of traffic).
- **Key Metric**: Type C cars experience an average waiting time of **12.63 minutes**.
- **Main Recommendation**: Add a **second Gas pump** to reduce congestion and improve service times.

---

## 🧪 Simulation Design

- **Car Types**:
  - 🚗 Type A: Uses Pump 95
  - 🚙 Type B: Prefers Pump 90 (may switch to Pump 95)
  - 🚐 Type C: Prefers Gas (may switch to Pump 90)

- **Logic**:
  - Reassign Type B if Pump 90 queue > 3 (60% chance)
  - Reassign Type C if Gas queue > 4 (40% chance)

- **Distributions**:
  - **Inter-Arrival Time**: 0–3 minutes (discrete)
  - **Service Time**:
    - Type A/B: 1–3 minutes
    - Type C: 3–7 minutes

- **Iterations**: 100 runs × 30 cars
- **Tools Used**: `numpy`, `pandas`, `matplotlib`

---

## 📊 Key Results (Average Over 100 Runs)

| Metric                                | Value            |
|---------------------------------------|------------------|
| Experimental Avg. Service Time        | 3.81 minutes     |
| Theoretical Avg. Service Time         | 3.75 minutes     |
| Avg. Waiting Time (Pump 95)           | 0.20 minutes     |
| Avg. Waiting Time (Pump 90)           | 0.78 minutes     |
| **Avg. Waiting Time (Gas)**           | **12.63 minutes**|
| Total Avg. Waiting Time               | 4.53 minutes     |
| Max Queue Length (Gas)                | 5.90 cars        |
| Probability of Waiting (Gas)          | 0.86             |
| Idle Time % (Pump 95 / 90 / Gas)      | 80.78% / 57.32% / 12.24% |
| Car Type Distribution (A / B / C)     | 20% / 33.9% / 46.1% |

---

## 📈 Visualizations

The simulation includes two key histograms:

- **Inter-Arrival Time Distribution**
- **Average Waiting Time for All Cars**

> _*You can include them by uploading:_ `inter_arrival_time.png`, `average_waiting_time.png`_

---

## 📌 Analysis Highlights

- **Validation**: Experimental results closely match theoretical expectations.
- **Bottleneck**: Gas pump is overwhelmed due to long service times and high Type C car volume.
- **Utilization**:
  - Gas pump shows the lowest idle time (12.24%) → overutilized.
  - Pumps 95 and 90 are underutilized.

---

## ✅ Recommendations

1. **Add a Second Gas Pump**
   - Would dramatically reduce Type C waiting time from 12.63 minutes.

2. **Tweak Reassignment Probability**
   - Increase the chance of redirecting Type C to Pump 90 (currently 40%).

3. **Optimize Service Efficiency**
   - Explore faster fueling methods for Gas.

---

## 📅 Conclusion

This simulation (run on **July 6, 2025**) effectively models gas station dynamics. The data supports actionable improvements, primarily focused on Gas pump overload. Future work may simulate **dynamic scheduling** or more advanced **multi-pump logic** for further optimization.

---



