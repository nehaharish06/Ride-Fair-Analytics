import pandas as pd
import logging
import matplotlib.pyplot as plt


# LOGGING CONFIGURATION

logging.basicConfig(
    filename="ride_engine.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# STEP 1: DATA LOADER

class DataLoader:
    def __init__(self, drivers_file, rides_file):
        self.drivers_file = drivers_file
        self.rides_file = rides_file

    def load_data(self):
        logging.info("Loading CSV files")
        # Read CSV files into pandas DataFrames
        drivers = pd.read_csv(self.drivers_file)
        rides = pd.read_csv(self.rides_file)
        logging.info("CSV files loaded successfully")
        return drivers, rides



# STEP 2: VALIDATION

class Validator:
    def __init__(self, drivers, rides):
        self.drivers = drivers
        self.rides = rides

    def validate_drivers(self):
        logging.info("Validating drivers")
        before = len(self.drivers)

        # Remove drivers with missing IDs
        self.drivers = self.drivers.dropna(subset=["driver_id"])

        # Keep only ACTIVE drivers
        active_drivers = self.drivers[self.drivers["status"] == "ACTIVE"]

        logging.info(f"Drivers before: {before}, after validation: {len(active_drivers)}")

        # Store valid driver IDs
        return set(active_drivers["driver_id"])

    def validate_rides(self, valid_driver_ids):
        logging.info("Validating rides")
        before = len(self.rides)

        # Convert ride_time to datetime (invalid to NaT)
        self.rides["ride_time"] = pd.to_datetime(self.rides["ride_time"], errors="coerce")

        # Filter valid rides based on rules
        valid_rides = self.rides[
            (self.rides["driver_id"].isin(valid_driver_ids)) &   # valid driver
            (self.rides["fare_amount"] > 0) &                   # positive fare
            (self.rides["ride_status"] == "COMPLETED") &        # completed rides
            (self.rides["ride_time"].notna())                   # valid time
        ].copy()

        logging.info(f"Rides before: {before}, after validation: {len(valid_rides)}")

        return valid_rides



# STEP 3: ANOMALY DETECTION

class AnomalyDetector:

    def __init__(self, rides):
        self.rides = rides

    def detect_high_fare(self):
        logging.info("Detecting high fare anomalies")
        # Detect rides where fare > 500
        anomalies = []
        high_fare = self.rides[self.rides["fare_amount"] > 500]

        for _, row in high_fare.iterrows():
            anomalies.append({
                "ride_id": row["ride_id"],
                "driver_id": row["driver_id"],
                "issue": "HIGH_FARE"
            })

        logging.info(f"High fare anomalies found: {len(anomalies)}")
        return anomalies

    def detect_rapid_rides(self):
        logging.info("Detecting rapid ride anomalies")
        # <2 rides within 2 minutes
        anomalies = []

        # Sort rides for proper time comparison
        rides_sorted = self.rides.sort_values(by=["driver_id", "ride_time"])

        for driver_id, group in rides_sorted.groupby("driver_id"):
            group = group.sort_values("ride_time")

            for i in range(len(group) - 2):
                t1 = group.iloc[i]["ride_time"]
                t3 = group.iloc[i + 2]["ride_time"]

                # If 3 rides happen within 2 minutes → anomaly
                if (t3 - t1).total_seconds() <= 120:
                    anomalies.append({
                        "ride_id": group.iloc[i + 2]["ride_id"],
                        "driver_id": driver_id,
                        "issue": "RAPID_RIDES"
                    })

        logging.info(f"Rapid ride anomalies found: {len(anomalies)}")
        return anomalies

    def generate_report(self):
        logging.info("Generating anomaly report")
        # Combine all anomaly detection results
        anomalies = []
        anomalies.extend(self.detect_high_fare())
        anomalies.extend(self.detect_rapid_rides())

        logging.info("Anomaly report generated")
        return pd.DataFrame(anomalies)



# STEP 4: DRIVER PERFORMANCE

class PerformanceCalculator:

    def __init__(self, rides):
        self.rides = rides

    def calculate(self):
        logging.info("Calculating driver performance")
        # Group by driver and calculate metrics
        performance = self.rides.groupby("driver_id").agg(
            total_rides=("ride_id", "count"),
            total_earnings=("fare_amount", "sum"),
            avg_fare=("fare_amount", "mean")
        ).reset_index()

        logging.info("Driver performance calculated")
        return performance



# STEP 5: MAIN ENGINE

class RideAnalyticsEngine:

    def __init__(self, drivers_file, rides_file):
        self.loader = DataLoader(drivers_file, rides_file)

    def run(self):
        logging.info("Starting Ride Analytics Engine")

        # STEP 1: Load data
        drivers, rides = self.loader.load_data()

        # STEP 2: Validate data
        validator = Validator(drivers, rides)
        valid_driver_ids = validator.validate_drivers()
        valid_rides = validator.validate_rides(valid_driver_ids)

        # STEP 3: Detect anomalies
        detector = AnomalyDetector(valid_rides)
        anomaly_df = detector.generate_report()

        # STEP 4: Calculate performance
        calculator = PerformanceCalculator(valid_rides)
        performance_df = calculator.calculate()

        # STEP 5: Save outputs
        performance_df.to_csv("driver_performance.csv", index=False)
        anomaly_df.to_csv("anomaly_report.csv", index=False)

        logging.info("Outputs saved successfully")
        logging.info("Ride Analytics Engine completed")

        return performance_df, anomaly_df


# STEP 6: VISUALIZATION 

def generate_graphs(performance_df):
    plt.figure()

    bars = plt.bar(performance_df["driver_id"], performance_df["total_earnings"])

# Add total rides
    for i, bar in enumerate(bars):
        rides = performance_df["total_rides"].iloc[i]
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"Rides: {rides}",
            ha='center',
            va='bottom'
        )

    plt.xlabel("Driver ID")
    plt.ylabel("Total Earnings")
    plt.title("Driver Earnings with Total Rides")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("driver_earnings.png")
    plt.close()

# RUN MAIN

if __name__ == "__main__":
    # Initialize engine with input files
    engine = RideAnalyticsEngine("drivers.csv", "rides.csv")

    # Run complete pipeline
    performance, anomalies = engine.run()

    # Print results
    print("Driver Performance:\n", performance)
    print("\nAnomaly Report:\n", anomalies)
    generate_graphs(performance)