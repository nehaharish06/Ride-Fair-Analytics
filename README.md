# Ride-Fair-Analytics


##  Overview

This project processes ride and driver data to validate records, detect anomalies, and calculate driver performance metrics. It ensures that only valid and completed ride data is used for accurate analysis.

---

##  Objectives

* Filter invalid drivers and rides
* Detect suspicious ride patterns
* Generate driver performance reports
* Ensure clean and reliable analytics

---

##  Input Files

### 1. drivers.csv

Contains driver details:

* driver_id
* name
* status (ACTIVE / BLOCKED)

### 2. rides.csv

Contains ride details:

* ride_id
* driver_id
* fare_amount
* ride_time
* ride_status

---

##  Processing Steps

### Step 1: Data Loading

* Read `drivers.csv` and `rides.csv` using pandas

### Step 2: Driver Validation

* Remove missing driver IDs
* Keep only ACTIVE drivers
* Ignore BLOCKED drivers

### Step 3: Ride Validation

Only keep rides where:

* driver_id is valid
* driver is ACTIVE
* fare_amount > 0
* ride_status = COMPLETED
* ride_time is valid

---

##  Anomaly Detection

### 1. High Fare Detection

* Flag rides where fare_amount > 500

### 2. Rapid Ride Detection

* Flag drivers completing more than 2 rides within 2 minutes

---

##  Driver Performance Metrics

For each driver:

* Total rides
* Total earnings
* Average fare per ride

---

##  Output Files

### 1. driver_performance.csv

Contains:

* driver_id
* total_rides
* total_earnings
* avg_fare

### 2. anomaly_report.csv

Contains:

* ride_id
* driver_id
* issue (HIGH_FARE / RAPID_RIDES)

---

##  Unit Tests

The following test cases ensure correctness:

* test_invalid_driver_rejected
* test_blocked_driver_rejected
* test_negative_fare_ignored
* test_high_fare_flag
* test_rapid_rides_flag
* test_driver_earnings_calculation

---

##  Project Structure

project/
│
├── drivers.csv
├── rides.csv
├── main.py
├── test_engine.py
├── driver_performance.csv
├── anomaly_report.csv
└── README.md

---

##  How to Run

### Step 1: Install dependencies

pip install pandas

### Step 2: Run the main program

python main.py

### Step 3: Run test cases

python -m unittest test_engine.py

---

##  Design Approach

This project uses Object-Oriented Programming (OOP):

* DataLoader → Handles file reading
* Validator → Handles data validation
* AnomalyDetector → Detects anomalies
* PerformanceCalculator → Computes metrics
* RideAnalyticsEngine → Controls workflow

###  Benefits:

* Modular design
* Easy to maintain
* Scalable
* Reusable components

---

##  Optional Enhancements

* Add data visualization (PNG graphs)
* Add logging system
* Add real-time streaming support
* Build a frontend dashboard

---

