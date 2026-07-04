from prefect import flow, task
import yaml
import subprocess

def load_config():
    with open("config/pipeline.yaml", "r") as f:
        return yaml.safe_load(f)

@task
def run_sql(script_path):
    print(f"Executing {script_path}")
    # Replace with Snowflake CLI or Python connector
    subprocess.run(["snowsql", "-f", script_path], check=True)

@flow
def bureau_pipeline():
    config = load_config()
    for step in config["steps"]:
        run_sql(step["script"])
    print("Pipeline finished")

if __name__ == "__main__":
    bureau_pipeline()
