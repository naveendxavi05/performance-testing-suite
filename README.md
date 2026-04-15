# 🚀 Performance Testing Suite

![CI](https://github.com/naveendxavi05/performance-testing-suite/actions/workflows/ci.yml/badge.svg)
![Java](https://img.shields.io/badge/Java-21-orange?logo=openjdk)
![JMeter](https://img.shields.io/badge/JMeter-5.6.3-red?logo=apachejmeter)
![InfluxDB](https://img.shields.io/badge/InfluxDB-1.8-blue?logo=influxdb)
![Grafana](https://img.shields.io/badge/Grafana-Dashboard-orange?logo=grafana)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker)

> **Project 4 of 5** in a FAANG-targeted QA Automation Portfolio  
> End-to-end performance testing framework using Apache JMeter with real-time monitoring via InfluxDB + Grafana, automated SLA validation, and full CI/CD integration via GitHub Actions.

---

## 🎯 What This Project Demonstrates

| Skill | Implementation |
|-------|---------------|
| Performance Test Design | Load, Stress, Spike, and Soak test plans |
| Real-time Observability | InfluxDB + Grafana monitoring stack |
| SLA Validation | Automated Python script with pass/fail against baseline |
| CI/CD Integration | GitHub Actions pipeline with Docker Compose |
| Containerisation | Custom Restful Booker Docker image |
| Baseline Management | JSON-driven SLA thresholds committed to repo |

---

## 🧪 Test Plans

| Test Plan | VUs | Duration | Purpose |
|-----------|-----|----------|---------|
| `load-test.jmx` | 100 | 5 min | Validate normal traffic behaviour |
| `stress-test.jmx` | 200 | 5 min | Find the breaking point |
| `spike-test.jmx` | 0 → 150 → 0 | 3 min | Simulate sudden traffic surges |
| `soak-test.jmx` | 50 | 30 min | Detect memory leaks / degradation over time |

---

## 📊 Baseline Results (Load Test — 100 VUs)

| Metric | Result | SLA Threshold | Status |
|--------|--------|---------------|--------|
| p95 Response Time | **4 ms** | < 500 ms | ✅ Pass |
| Error Rate | **0.38%** | < 1% | ✅ Pass |
| Throughput | **296 req/s** | > 50 req/s | ✅ Pass |

---

## 🏗️ Project Structure

```
performance-testing-suite/
├── test-plans/
│   ├── load-test.jmx
│   ├── stress-test.jmx
│   ├── spike-test.jmx
│   └── soak-test.jmx
├── results/
│   └── (generated JTL files and HTML reports)
├── scripts/
│   └── check-sla.py          # Automated SLA validator
├── docker/
│   └── docker-compose.yml    # InfluxDB + Grafana stack
├── grafana/
│   └── dashboards/
│       └── jmeter-dashboard.json  # Importable Grafana dashboard
├── baseline.json              # SLA thresholds
└── .github/
    └── workflows/
        └── ci.yml             # GitHub Actions pipeline
```

---

## ⚙️ Tech Stack

- **Apache JMeter 5.6.3** — test execution engine
- **InfluxDB 1.8** — time-series metrics storage
- **Grafana** — real-time dashboard visualisation
- **Docker Compose** — monitoring stack orchestration
- **Python 3** — SLA validation script
- **GitHub Actions** — CI/CD pipeline
- **Java 21 (Amazon Corretto)** — runtime environment
- **Restful Booker** — containerised REST API under test

---

## 🚀 Getting Started

### Prerequisites
- Docker Desktop
- JMeter 5.6.3
- Java 21
- Python 3

### 1. Start the monitoring stack

```bash
docker compose -f docker/docker-compose.yml up -d
```

Grafana will be available at `http://localhost:3000` (admin / admin)

### 2. Import the Grafana dashboard

1. Open Grafana → **Dashboards → Import**
2. Upload `grafana/dashboards/jmeter-dashboard.json`
3. Select **InfluxDB** as the data source

### 3. Run a test plan

```bash
jmeter -n \
  -t test-plans/load-test.jmx \
  -l results/load-test-results.jtl \
  -e -o results/load-test-report
```

### 4. Validate SLA

```bash
python3 scripts/check-sla.py
```

Expected output:
```
✅ p95 PASS: 4ms < 500ms
✅ error_rate PASS: 0.38% < 1%
✅ throughput PASS: 296 req/s > 50 req/s
All SLA checks passed.
```

---

## 🔄 CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/ci.yml`) automatically:

1. Spins up the Restful Booker container
2. Starts the InfluxDB + Grafana monitoring stack
3. Executes the load test plan via JMeter CLI
4. Runs `check-sla.py` and fails the build if any SLA is breached
5. Publishes the JMeter HTML report as a pipeline artifact

---

## 📦 Restful Booker Docker Image

A custom image built from source and pushed to Docker Hub:

```
docker pull naveendxavi/restful-booker
```

Used to eliminate rate-limiting issues present on the public hosted instance, ensuring stable and reproducible test runs.

---

## 🔗 Portfolio

This is **Project 4 of 5** in my QA Automation Portfolio:

| # | Project | Focus |
|---|---------|-------|
| P1 | [ecommerce-ui-automation](https://github.com/naveendxavi05/ecommerce-ui-automation) | Selenium 4 + TestNG + ExtentReports |
| P2 | [api-security-suite](https://github.com/naveendxavi05/api-security-suite) | RestAssured + OWASP + Cucumber |
| P3 | *(coming soon)* | CI/CD + Docker + SonarCloud |
| **P4** | **performance-testing-suite** | **JMeter + Grafana + InfluxDB** |
| P5 | *(coming soon)* | BDD Framework |

---

## 👤 Author

**Naveen D**  
QA Automation Engineer  
📧 naveendxavi@gmail.com  
🔗 [GitHub](https://github.com/naveen-d-xavi) · [LinkedIn](https://linkedin.com/in/naveen-d-xavi)
