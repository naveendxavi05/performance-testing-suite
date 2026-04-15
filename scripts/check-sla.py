import csv
import json
import sys
import numpy

def check_sla(jtl_path):
    # 1. Parse JTL file
    rows = []
    with open(jtl_path, encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    if not rows:
        print("ERROR: JTL file is empty")
        sys.exit(1)

    # 2. Compute metrics
    elapsed = [int(r['elapsed']) for r in rows]
    p95 = numpy.percentile(elapsed, 95)

    timestamps = [int(r['timeStamp']) for r in rows]
    duration_seconds = (max(timestamps) - min(timestamps)) / 1000.0
    throughput = len(rows) / duration_seconds

    # 'success' column contains strings 'true'/'false' — NOT Python booleans
    failed_count = sum(1 for r in rows if r['success'] == 'false')
    error_rate = (failed_count / len(rows)) * 100

    print(f"Results:")
    print(f"  Total requests : {len(rows)}")
    print(f"  p95 response   : {p95:.2f} ms")
    print(f"  Error rate     : {error_rate:.2f}%")
    print(f"  Throughput     : {throughput:.2f} req/sec")

    # 3. Check SLA thresholds
    failed = False

    if p95 >= 500:
        print(f"FAIL: p95 {p95:.2f}ms >= 500ms threshold")
        failed = True
    else:
        print(f"PASS: p95 {p95:.2f}ms < 500ms")

    if error_rate >= 1.0:
        print(f"FAIL: error rate {error_rate:.2f}% >= 1% threshold")
        failed = True
    else:
        print(f"PASS: error rate {error_rate:.2f}% < 1%")

    if throughput <= 50:
        print(f"FAIL: throughput {throughput:.2f} req/sec <= 50 req/sec threshold")
        failed = True
    else:
        print(f"PASS: throughput {throughput:.2f} req/sec > 50 req/sec")

    # 4. Compare against baseline
    baseline_path = 'scripts/baseline.json'
    try:
        with open(baseline_path) as f:
            baseline = json.load(f)

        baseline_p95 = baseline['p95']
        baseline_error_rate = baseline['error_rate']

        p95_regression = ((p95 - baseline_p95) / baseline_p95) * 100
        error_regression = error_rate - baseline_error_rate

        print(f"\nBaseline comparison:")
        if p95_regression > 20:
            print(f"FAIL: p95 regressed {p95_regression:.1f}% vs baseline ({baseline_p95}ms)")
            failed = True
        else:
            print(f"PASS: p95 regression {p95_regression:.1f}% within 20% threshold")

        if error_regression > 0.5:
            print(f"FAIL: error rate regressed {error_regression:.2f}% vs baseline ({baseline_error_rate}%)")
            failed = True
        else:
            print(f"PASS: error rate regression {error_regression:.2f}% within 0.5% threshold")

    except FileNotFoundError:
        print(f"\nINFO: No baseline.json found — skipping baseline comparison")
        print(f"Suggested baseline values:")
        print(f"  {{\"p95\": {p95:.0f}, \"error_rate\": {error_rate:.2f}, \"throughput\": {throughput:.0f}}}")

    # 5. Exit code
    if failed:
        print("\nSLA CHECK FAILED")
        sys.exit(1)
    else:
        print("\nSLA CHECK PASSED")
        sys.exit(0)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python scripts/check-sla.py <path-to-jtl>")
        sys.exit(1)
    check_sla(sys.argv[1])
