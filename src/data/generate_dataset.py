import pandas as pd
import random

tests = []

modules = [
    "PCIe",
    "Memory",
    "Boot",
    "Power",
    "USB",
    "Clock",
    "Thermal",
    "Network",
    "Reset",
    "DMA",
    "Interrupt",
    "Voltage",
    "Cache",
    "IO",
    "Firmware"
]

for i in range(200):

    module = random.choice(modules)

    runtime_sec = random.randint(50, 1000)

    previous_failures = random.randint(0, 10)

    run_count = random.randint(5, 100)

    severity_score = random.randint(1, 10)

    # Failure logic
    risk = (
        previous_failures * 0.4 +
        severity_score * 0.3 +
        runtime_sec / 1000
    )

    failed = 1 if risk > 4 else 0

    tests.append({
        "test_name": f"{module}_test_{i}",
        "module": module,
        "runtime_sec": runtime_sec,
        "previous_failures": previous_failures,
        "run_count": run_count,
        "severity_score": severity_score,
        "failed": failed
    })

df = pd.DataFrame(tests)

df.to_csv("data/test_history.csv", index=False)

print("Synthetic dataset created successfully!")
print(df.head())