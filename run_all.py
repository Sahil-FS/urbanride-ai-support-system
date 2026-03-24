import subprocess
import sys
import os
import signal
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SERVICES = [
    {
        "name": "Chatbot Service (port 8000)",
        "cmd": [sys.executable, "-m", "uvicorn", "main:app",
                "--port", "8000", "--reload"],
        "cwd": BASE_DIR,
    },
    {
        "name": "Mock Intent API (port 8001)",
        "cmd": [sys.executable, "-m", "uvicorn", "mock_intent_api:app",
                "--port", "8001", "--reload"],
        "cwd": os.path.join(BASE_DIR, "mocks"),
    },
    {
        "name": "Mock NLP API (port 8002)",
        "cmd": [sys.executable, "-m", "uvicorn", "mock_nlp_api:app",
                "--port", "8002", "--reload"],
        "cwd": os.path.join(BASE_DIR, "mocks"),
    },
]

def main():
    processes = []
    print("\n" + "="*55)
    print("  Urban Black Taxi — Customer Support AI Stack")
    print("="*55)
    for svc in SERVICES:
        print(f"\n  Starting {svc['name']} ...")
        proc = subprocess.Popen(svc["cmd"], cwd=svc["cwd"])
        processes.append(proc)
        time.sleep(1)
    print("\n" + "="*55)
    print("  All services running!")
    print("-"*55)
    print("  Chatbot API  ->  http://localhost:8000/docs")
    print("  Intent API   ->  http://localhost:8001/docs")
    print("  NLP API      ->  http://localhost:8002/docs")
    print("-"*55)
    print("  Press Ctrl+C to stop all")
    print("="*55 + "\n")

    def shutdown(sig, frame):
        print("\nShutting down...")
        for proc in processes:
            proc.terminate()
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)
    for proc in processes:
        proc.wait()

if __name__ == "__main__":
    main()
