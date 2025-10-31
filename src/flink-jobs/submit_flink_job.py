"""
Submit Flink SQL job to running Flink cluster
"""
import requests
import time

FLINK_REST_URL = "http://localhost:8082"

def check_flink_health():
    """Check if Flink cluster is healthy"""
    try:
        response = requests.get(f"{FLINK_REST_URL}/overview")
        if response.status_code == 200:
            data = response.json()
            print(f"Flink Cluster Status:")
            print(f"  Task Managers: {data['taskmanagers']}")
            print(f"  Slots Total: {data['slots-total']}")
            print(f"  Slots Available: {data['slots-available']}")
            return True
    except Exception as e:
        print(f"Error connecting to Flink: {e}")
        return False

def list_jobs():
    """List running Flink jobs"""
    try:
        response = requests.get(f"{FLINK_REST_URL}/jobs")
        if response.status_code == 200:
            jobs = response.json()['jobs']
            print(f"\nRunning Jobs: {len(jobs)}")
            for job in jobs:
                print(f"  - {job['id']}: {job['status']}")
            return jobs
    except Exception as e:
        print(f"Error listing jobs: {e}")
        return []

if __name__ == "__main__":
    print("Checking Flink cluster...")
    if check_flink_health():
        print("\n✓ Flink cluster is healthy!")
        list_jobs()
        print("\nFlink UI: http://localhost:8082")
        print("\nNote: For SQL jobs, use Flink SQL Client in the container:")
        print("  docker exec -it flink-jobmanager ./bin/sql-client.sh")
    else:
        print("\n✗ Cannot connect to Flink cluster")
        print("  Make sure Flink is running: docker ps | grep flink")
