'''
执行 pytest + Allure
'''

import os
import subprocess
import time

def run_pytest_with_allure():
    """
    执行 pytest 并生成 Allure 报告
    """
    report_dir = "allure-results"
    os.makedirs(report_dir, exist_ok=True)

    # 执行 pytest
    cmd = [
        "pytest",
        "-vs",
        "--alluredir", report_dir,
        "--clean-alluredir"
    ]

    start = time.time()
    result = subprocess.run(cmd)
    duration = round(time.time() - start, 2)

    return {
        "return_code": result.returncode,
        "duration": duration,
        "report_dir": report_dir,
        "status": "success" if result.returncode == 0 else "failed"
    }

if __name__ == "__main__":
    run_pytest_with_allure()