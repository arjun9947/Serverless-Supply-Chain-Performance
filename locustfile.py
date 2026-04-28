import random
import uuid
from locust import HttpUser, task, between, events

class SupplyChainBenchmarker(HttpUser):
    # --- CONFIGURATION ---
    # This is your AWS API Gateway Invoke URL
    host = "https://xom49kg0n9.execute-api.ap-south-1.amazonaws.com"
    
    # Mimics real-world supply chain order intervals (1-2 seconds between tasks)
    wait_time = between(1, 2)

    @task
    def place_order(self):
        """
        Sends a POST request with a randomized payload. 
        We use random SKUs to force DynamoDB to perform actual I/O 
        rather than relying on cached results.
        """
        order_payload = {
            "sku": f"PROD-{random.randint(100, 999)}",
            "qty": random.randint(1, 100),
            "trace_id": str(uuid.uuid4())
        }

        # We use a context manager (with...) to catch the response 
        # and validate the success/failure manually for our report.
        with self.client.post(
            "/place-order", 
            json=order_payload, 
            name="POST_Order_Scale_Test",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                # OPTIONAL: You can parse the JSON to get internal AWS latency
                # data = response.json()
                # print(f"AWS Internal Latency: {data.get('total_ms')}ms")
                response.success()
            else:
                response.failure(f"Scaling Limit Reached: {response.status_code}")

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    print("--- BENCHMARK STARTED: Monitoring for Cold Starts and Throttle Points ---")