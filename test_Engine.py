import unittest
import pandas as pd
from main import RideAnalyticsEngine


class TestRideAnalyticsEngine(unittest.TestCase):

    def test_invalid_driver_rejected(self):
        drivers = pd.DataFrame({
            "driver_id": [1],
            "status": ["ACTIVE"]
        })

        rides = pd.DataFrame({
            "ride_id": [101],
            "driver_id": [2],  # invalid
            "fare_amount": [100],
            "ride_time": ["2024-01-01 10:00:00"],
            "ride_status": ["COMPLETED"]
        })

        drivers.to_csv("test_driver.csv", index=False)
        rides.to_csv("test_rider.csv", index=False)

        engine = RideAnalyticsEngine("test_driver.csv", "test_rider.csv")
        perf, _ = engine.run()

        self.assertTrue(perf.empty)


    def test_blocked_driver_rejected(self):
        drivers = pd.DataFrame({
            "driver_id": [1],
            "status": ["BLOCKED"]
        })

        rides = pd.DataFrame({
            "ride_id": [101],
            "driver_id": [1],
            "fare_amount": [100],
            "ride_time": ["2024-01-01 10:00:00"],
            "ride_status": ["COMPLETED"]
        })

        drivers.to_csv("test_driver.csv", index=False)
        rides.to_csv("test_rider.csv", index=False)

        engine = RideAnalyticsEngine("test_driver.csv", "test_rider.csv")
        perf, _ = engine.run()

        self.assertTrue(perf.empty)


    def test_negative_fare_ignored(self):
        drivers = pd.DataFrame({
            "driver_id": [1],
            "status": ["ACTIVE"]
        })

        rides = pd.DataFrame({
            "ride_id": [101],
            "driver_id": [1],
            "fare_amount": [-50],
            "ride_time": ["2024-01-01 10:00:00"],
            "ride_status": ["COMPLETED"]
        })

        drivers.to_csv("test_driver.csv", index=False)
        rides.to_csv("test_rider.csv", index=False)

        engine = RideAnalyticsEngine("test_driver.csv", "test_rider.csv")
        perf, _ = engine.run()

        self.assertTrue(perf.empty)


    def test_high_fare_flag(self):
        drivers = pd.DataFrame({
            "driver_id": [1],
            "status": ["ACTIVE"]
        })

        rides = pd.DataFrame({
            "ride_id": [101],
            "driver_id": [1],
            "fare_amount": [600],  #>500
            "ride_time": ["2024-01-01 10:00:00"],
            "ride_status": ["COMPLETED"]
        })

        drivers.to_csv("test_driver.csv", index=False)
        rides.to_csv("test_rider.csv", index=False)

        engine = RideAnalyticsEngine("test_driver.csv", "test_rider.csv")
        _, anomalies = engine.run()

        self.assertIn("HIGH_FARE", anomalies["issue"].values)


    def test_rapid_rides_flag(self):
        drivers = pd.DataFrame({
            "driver_id": [1],
            "status": ["ACTIVE"]
        })

        rides = pd.DataFrame({
            "ride_id": [1, 2, 3],
            "driver_id": [1, 1, 1],
            "fare_amount": [100, 120, 130],
            "ride_time": [
                "2024-01-01 10:00:00",
                "2024-01-01 10:01:00",
                "2024-01-01 10:01:30"
            ],
            "ride_status": ["COMPLETED", "COMPLETED", "COMPLETED"]
        })

        drivers.to_csv("test_driver.csv", index=False)
        rides.to_csv("test_rider.csv", index=False)

        engine = RideAnalyticsEngine("test_driver.csv", "test_rider.csv")
        _, anomalies = engine.run()

        self.assertIn("RAPID_RIDES", anomalies["issue"].values)


    def test_driver_earnings_calculation(self):
        drivers = pd.DataFrame({
            "driver_id": [1],
            "status": ["ACTIVE"]
        })

        rides = pd.DataFrame({
            "ride_id": [1, 2],
            "driver_id": [1, 1],
            "fare_amount": [100, 200],
            "ride_time": ["2024-01-01 10:00:00", "2024-01-01 11:00:00"],
            "ride_status": ["COMPLETED", "COMPLETED"]
        })

        drivers.to_csv("test_driver.csv", index=False)
        rides.to_csv("test_rider.csv", index=False)

        engine = RideAnalyticsEngine("test_driver.csv", "test_rider.csv")
        perf, _ = engine.run()

        self.assertEqual(perf.iloc[0]["total_earnings"], 300)


if __name__ == "__main__":
    unittest.main()