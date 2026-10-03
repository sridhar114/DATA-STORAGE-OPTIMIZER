import argparse
import json
import threading
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

PLANS_FILE = Path(__file__).with_name("plans.json")
PLANS_LOCK = threading.Lock()


def knapsack(files, capacity):
    n = len(files)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        _, size, importance = files[i - 1]
        for weight in range(capacity + 1):
            if size > weight:
                dp[i][weight] = dp[i - 1][weight]
            else:
                dp[i][weight] = max(
                    dp[i - 1][weight],
                    importance + dp[i - 1][weight - size],
                )

    selected_files = []
    weight = capacity
    for i in range(n, 0, -1):
        if dp[i][weight] != dp[i - 1][weight]:
            selected_files.append(files[i - 1])
            weight -= files[i - 1][1]

    selected_files.reverse()
    return dp[n][capacity], selected_files


def optimize_payload(payload):
    if not isinstance(payload, dict):
        raise ValueError("Request body must be a JSON object.")

    capacity = payload.get("capacity")
    files = payload.get("files")
    if type(capacity) is not int or capacity < 0:
        raise ValueError("Capacity must be a non-negative whole number.")
    if not isinstance(files, list):
        raise ValueError("Files must be a list.")

    normalized_files = []
    for index, item in enumerate(files, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"File {index} must be an object.")
        name = item.get("name")
        size = item.get("size")
        importance = item.get("importance")
        if not isinstance(name, str) or not name.strip():
            raise ValueError(f"File {index} needs a name.")
        if type(size) is not int or size <= 0:
            raise ValueError(f"Size for {name.strip()} must be a positive whole number.")
        if type(importance) is not int or importance < 0:
            raise ValueError(f"Importance for {name.strip()} must be a non-negative whole number.")
        normalized_files.append((name.strip(), size, importance))

    maximum_importance, selected_files = knapsack(normalized_files, capacity)
    total_size = sum(size for _, size, _ in selected_files)
    return {
        "maximumImportance": maximum_importance,
        "selectedFiles": [
            {"name": name, "size": size, "importance": importance}
            for name, size, importance in selected_files
        ],
        "totalSize": total_size,
        "remainingStorage": capacity - total_size,
        "capacity": capacity,
    }


def load_plans():
    with PLANS_LOCK:
        if not PLANS_FILE.exists():
            return []
        plans = json.loads(PLANS_FILE.read_text(encoding="utf-8"))
        if not isinstance(plans, list):
            raise ValueError("plans.json must contain a JSON array.")
        return plans


def save_plan(payload, result):
    plan = {
        "id": datetime.now(timezone.utc).isoformat(),
        "capacity": payload["capacity"],
        "files": payload["files"],
        "result": result,
    }
    with PLANS_LOCK:
        if PLANS_FILE.exists():
            plans = json.loads(PLANS_FILE.read_text(encoding="utf-8"))
            if not isinstance(plans, list):
                raise ValueError("plans.json must contain a JSON array.")
        else:
            plans = []
        plans.append(plan)
        temporary_file = PLANS_FILE.with_suffix(".json.tmp")
        temporary_file.write_text(json.dumps(plans, indent=2) + "\n", encoding="utf-8")
        temporary_file.replace(PLANS_FILE)
    return plan


class OptimizerHandler(BaseHTTPRequestHandler):
    def _send_json(self, status, body):
        encoded = json.dumps(body).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self):
        if self.path == "/api/plans":
            try:
                self._send_json(200, {"plans": load_plans()})
            except (OSError, json.JSONDecodeError, ValueError) as error:
                self._send_json(500, {"error": f"Could not read plans.json: {error}"})
            return

        if self.path not in ("/", "/index.html"):
            self._send_json(404, {"error": "Not found."})
            return

        page = Path(__file__).with_name("index.html")
        try:
            content = page.read_bytes()
        except OSError:
            self._send_json(500, {"error": "Frontend file index.html is missing."})
            return

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_POST(self):
        if self.path != "/api/optimize":
            self._send_json(404, {"error": "Not found."})
            return

        try:
            content_length = int(self.headers.get("Content-Length", "0"))
            if content_length <= 0 or content_length > 1_000_000:
                raise ValueError("Request body must be between 1 byte and 1 MB.")
            payload = json.loads(self.rfile.read(content_length))
            result = optimize_payload(payload)
            plan = save_plan(payload, result)
            result["planId"] = plan["id"]
            self._send_json(200, result)
        except (OSError, ValueError, json.JSONDecodeError) as error:
            self._send_json(400, {"error": str(error)})

    def log_message(self, format_string, *args):
        print(f"{self.address_string()} - {format_string % args}")


def run_cli():
    print("DIGITAL FILE STORAGE OPTIMIZER")
    capacity = int(input("\nEnter available storage capacity (GB): "))
    count = int(input("Enter number of files: "))
    files = []

    for index in range(count):
        print(f"\nFile {index + 1}")
        name = input("File name: ")
        size = int(input("File size (GB): "))
        importance = int(input("File importance: "))
        files.append((name, size, importance))

    maximum_importance, selected_files = knapsack(files, capacity)
    total_size = sum(size for _, size, _ in selected_files)
    print("\nSelected files:")
    for name, size, importance in selected_files:
        print(f"  {name}: {size} GB, importance {importance}")
    print(f"Storage used: {total_size}/{capacity} GB")
    print(f"Remaining storage: {capacity - total_size} GB")
    print(f"Maximum importance: {maximum_importance}")


def main():
    parser = argparse.ArgumentParser(description="Digital file storage optimizer")
    parser.add_argument("--cli", action="store_true", help="use the interactive terminal interface")
    parser.add_argument("--port", type=int, default=8000, help="web interface port (default: 8000)")
    args = parser.parse_args()

    if args.cli:
        run_cli()
        return

    server = ThreadingHTTPServer(("127.0.0.1", args.port), OptimizerHandler)
    print(f"Digital File Storage Optimizer running at http://127.0.0.1:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()