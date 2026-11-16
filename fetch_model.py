import os
import shutil
import mlflow
from mlflow.tracking import MlflowClient

mlflow.set_tracking_uri(os.environ["MLFLOW_TRACKING_URI"])
client = MlflowClient()

exp = client.get_experiment_by_name("RandomForest_V1.0.1")
runs = client.search_runs([exp.experiment_id], order_by=["attributes.start_time DESC"], max_results=1)
run_id = runs[0].info.run_id

model_dir = next(a.path for a in client.list_artifacts(run_id) if a.is_dir)
mlflow.artifacts.download_artifacts(run_id=run_id, artifact_path=model_dir, dst_path="/tmp/dl")
shutil.move(f"/tmp/dl/{model_dir}", "model")
print("Model fetched from run", run_id)
