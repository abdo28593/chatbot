import json
import subprocess
import os
import sys
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE = os.path.join(BASE_DIR, "workspace")
OUTPUT = os.path.join(BASE_DIR, "output")

PROJECT_FILE = os.path.join(BASE_DIR, "project.json")

def load_project():
    with open(PROJECT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def ensure_dirs():
    os.makedirs(WORKSPACE, exist_ok=True)
    os.makedirs(OUTPUT, exist_ok=True)
    os.makedirs(os.path.join(OUTPUT, "gerbers"), exist_ok=True)

def run_cmd(cmd):
    print("▶", " ".join(cmd))
    subprocess.run(cmd, check=True)

def export_gerbers(pcb_file):
    run_cmd([
        "kicad-cli",
        "pcb",
        "export",
        "gerbers",
        pcb_file,
        "-o",
        os.path.join(OUTPUT, "gerbers")
    ])

def export_step(pcb_file):
    run_cmd([
        "kicad-cli",
        "pcb",
        "export",
        "step",
        pcb_file,
        "-o",
        os.path.join(OUTPUT, "board.step")
    ])

def main():
    project = load_project()
    ensure_dirs()

    # simulate project preparation steps with delays and flushes
    print("Preparing project...")
    sys.stdout.flush()
    time.sleep(1)

    print("Placing components...")
    sys.stdout.flush()
    time.sleep(1)

    print("Routing traces...")
    sys.stdout.flush()

    pcb_file = os.path.join(WORKSPACE, "board.kicad_pcb")

    if not os.path.exists(pcb_file):
        print("❌ board.kicad_pcb not found")
        sys.exit(1)

    print("✅ Project:", project["project"]["name"])
    print("⚙ Task:", project["request"]["task"])

    # perform exports with status messages
    print("Exporting Gerbers...")
    sys.stdout.flush()
    export_gerbers(pcb_file)

    print("Exporting STEP...")
    sys.stdout.flush()
    export_step(pcb_file)

    print("🎉 Done! Files generated in /output")

if __name__ == "__main__":
    main()