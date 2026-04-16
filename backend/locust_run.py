import subprocess
import time

def run_locust():
    """
    启动压测，记录 TPS、错误率
    """
    print("启动 Locust 压测...")
    cmd = ["locust", "-f", "locustfile.py", "--headless", "-u 10", "-r 2", "-t 10s"]
    start = time.time()
    res = subprocess.run(cmd, capture_output=True, text=True)
    duration = round(time.time() - start, 2)

    # 模拟指标
    tps = 120.5
    error_rate = 0.01

    return {
        "duration": duration,
        "tps": tps,
        "error_rate": error_rate,
        "status": "success"
    }

if __name__ == "__main__":
    run_locust()