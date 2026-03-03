# AHSAN-DDOS V1.0 🚀

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-Active-brightgreen.svg)

**AHSAN-DDOS** is an ultra-high performance, multi-threaded load testing and DDoS simulation tool. Engineered for security professionals and network stress-testing, it utilizes `pycurl` (libcurl) for maximum Requests Per Second (RPS) and features advanced bypass techniques.

---

## ⚡ Key Features

- **Extreme Performance**: Uses `pycurl` (libcurl) C-bindings for near-native network throughput.
- **Advanced Header Rotation**: Dynamically generates unique `User-Agent`, `X-Forwarded-For`, `X-Real-IP`, and `Via` headers for every request.
- **Multi-Vector Attacks**: Supports both **GET floods** and **POST payload floods** to exhaust both bandwidth and server-side processing.
- **Deep Cache-Busting**: Multi-layer randomized query parameters bypass CDNs and server-side caching (Varnish, Nginx, Cloudflare).
- **Hacker-Dashboard UI**: Modern, real-time monitoring dashboard with live RPS, success rates, and mission progress.
- **Automatic Dependencies**: Self-healing engine that automatically detects and installs missing Python packages.

---

## 🛠️ Installation & Setup

### 1. Requirements
- **Python 3.8+**
- **pip** (Python package manager)
- **libcurl** (Optional, for `pycurl` performance boost)

### 2. Quick Start
Clone the repository and run the script:

```bash
git clone https://github.com/YOUR_USERNAME/ahsan-ddos.git
cd ahsan-ddos
python ahsan-ddos.py
```

---

## 🚀 Usage Guide

1. **Launch**: Start the tool using `python ahsan-ddos.py`.
2. **Configure Target**: Enter the full URL (e.g., `https://example.com`).
3. **Set Intensity**:
   - **Target RPS**: Recommended `10000+` for stress testing.
   - **Duration**: Set the mission length in seconds.
   - **CPU Threads**: Auto-detected, but can be manually tuned for maximum load.
4. **Monitor**: Watch the real-time Mission Status Dashboard for live performance metrics.

---

## ⚠️ Disclaimer

**Educational Purposes Only.**
This tool is intended for legal stress testing and security research on networks you own or have explicit permission to test. Unauthorized use of this tool against third-party servers is illegal and strictly prohibited. The developer (AHSAN) assumes no liability for misuse or damage caused by this tool.

---

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Created by AHSAN. Our democracy has been hacked.**
