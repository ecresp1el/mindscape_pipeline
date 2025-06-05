# workflow/scripts/create_project.py
import os
import yaml
from pathlib import Path
from datetime import datetime

def main(config_path):
    with open(config_path) as f:
        config = yaml.safe_load(f)

    date = datetime.today().strftime("%Y-%m-%d")
    project_name = config["project_name"]
    experimenter = config["experimenter"]
    turbo = Path(config["shared_turbo_directory"])
    full_name = f"{project_name}-{experimenter}-{date}"
    project_path = turbo / full_name

    # Create directory structure
    for subdir in ["data", "results", "logs", "config"]:
        (project_path / subdir).mkdir(parents=True, exist_ok=True)

    # Save resolved project_path into the same config for later rules
    config["project_path"] = str(project_path)
    with open(project_path / "config/config.yaml", "w") as out:
        yaml.dump(config, out)
    with open(config_path, "w") as out_main:
        yaml.dump(config, out_main)

    print(f"✅ Created project structure at: {project_path}")

    # Primary marker in project dir (for downstream steps)
    marker_path = project_path / "results/create_project.done"
    marker_path.parent.mkdir(parents=True, exist_ok=True)
    marker_path.touch()
    print(f"📍 Project marker created at: {marker_path}")

    # Shadow marker in GitHub results/ to satisfy Snakemake output tracking
    github_marker = Path(__file__).resolve().parents[3] / "results/create_project.done"
    github_marker.parent.mkdir(parents=True, exist_ok=True)
    github_marker.touch()
    print(f"📍 GitHub marker created at: {github_marker}")

# Entrypoint for Snakemake
main(snakemake.input[0])

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python create_project.py path/to/config.yaml")
    else:
        main(sys.argv[1])