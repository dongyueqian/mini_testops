'''
测开核心：测试执行引擎
'''
import time
import uuid
from backend import models
from backend.database import SessionLocal

class TestEngine:
    def __init__(self):
        """
        生成一个唯一的任务 ID，比如 task_a1b2c3d4
        这样即使同时跑多个任务，也不会搞混
        uuid：非常重要。在并发测试中，你必须知道哪条日志属于哪个任务，ID 就是关键。
        """
        self.task_id = f"task_{uuid.uuid4().hex[:8]}"
        # 拿到数据库连接，用来存执行结果
        self.db = SessionLocal()

    def run_cases(self, case_ids: list = None):
        """
        执行测试用例（测开灵魂）
        作用：任务刚开始，先在数据库里占个坑。
        意义：前端页面可以轮询数据库，看到状态变成了“运行中”，给用户一个反馈
        """
        start = time.time()
        print(f"任务 {self.task_id} 开始执行")

        # 1. 记录任务开始
        record = models.TaskRecord(
            task_id=self.task_id,
            status="running"
        )
        self.db.add(record)
        self.db.commit()

        # 2. 模拟执行 ，假装测了 5 个用例，这里目前是写死的逻辑，以后会替换成真正的 requests 请求
        # 未来这里会变成一个循环，遍历 case_ids，根据数据库里的 url 和 method 发送真实的 HTTP 请求，然后对比返回结果。
        total = len(case_ids) if case_ids else 5
        passed = 4
        failed = 1
        duration = round(time.time() - start, 2)

        # 3. 更新结果，作用：把统计结果写回数据库。
        # 这里直接修改了刚才创建的 record 对象并再次 commit，这是 SQLAlchemy 的更新操作。
        record.status = "done"
        record.total = total
        record.passed = passed
        record.failed = failed
        record.duration = duration
        self.db.commit()

        print(f"任务完成：总用例{total}，通过{passed}，失败{failed}，耗时{duration}s")
        self.db.close()
        return {
            "task_id": self.task_id,
            "total": total,
            "passed": passed,
            "failed": failed,
            "duration": duration
        }

# 测试执行
if __name__ == "__main__":
    engine = TestEngine()
    engine.run_cases()