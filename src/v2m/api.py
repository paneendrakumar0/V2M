import os
import uuid
import threading
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
from v2m.core.preprocessor import Preprocessor
from v2m.core.reconstructor import Reconstructor
from v2m.core.exporter import Exporter
from v2m.utils.logger import setup_logger

logger = setup_logger(__name__)

app = FastAPI(title="V2M API", description="Video to Mesh Industrial Pipeline API", version="0.1.0")

# In-memory storage for task statuses
# States: PENDING, PREPROCESSING, TRAINING, EXPORTING, COMPLETED, FAILED
task_status_db = {}

DATA_ROOT = Path("data/api_runs")
DATA_ROOT.mkdir(parents=True, exist_ok=True)

def run_pipeline_sync(task_id: str, video_path: str):
    base_output_dir = DATA_ROOT / task_id
    processed_data_dir = base_output_dir / "processed_data"
    training_output_dir = base_output_dir / "training"
    mesh_output_path = base_output_dir / "mesh" / "model.obj"
    
    try:
        task_status_db[task_id] = "PREPROCESSING"
        preprocessor = Preprocessor(str(processed_data_dir))
        if not preprocessor.process_video(video_path):
            task_status_db[task_id] = "FAILED"
            return
            
        task_status_db[task_id] = "TRAINING"
        reconstructor = Reconstructor(str(processed_data_dir), str(training_output_dir))
        if not reconstructor.train(method="splatfacto"):
            task_status_db[task_id] = "FAILED"
            return
            
        task_status_db[task_id] = "EXPORTING"
        config_files = list(training_output_dir.rglob("config.yml"))
        if not config_files:
            task_status_db[task_id] = "FAILED"
            return
            
        exporter = Exporter(str(config_files[0]), str(mesh_output_path))
        if not exporter.export_mesh():
            task_status_db[task_id] = "FAILED"
            return
            
        task_status_db[task_id] = "COMPLETED"
    except Exception as e:
        logger.error(f"Task {task_id} failed with error: {e}")
        task_status_db[task_id] = "FAILED"

@app.post("/upload-video")
async def upload_video(file: UploadFile = File(...)):
    if not file.filename.endswith((".mp4", ".mov", ".avi")):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a video.")
        
    task_id = str(uuid.uuid4())
    task_dir = DATA_ROOT / task_id
    task_dir.mkdir(parents=True, exist_ok=True)
    
    video_path = task_dir / file.filename
    with open(video_path, "wb") as buffer:
        buffer.write(await file.read())
        
    task_status_db[task_id] = "PENDING"
    
    # Run pipeline in a background thread to not block the API
    thread = threading.Thread(target=run_pipeline_sync, args=(task_id, str(video_path)))
    thread.start()
    
    return {"message": "Video uploaded successfully. Pipeline started.", "task_id": task_id}

@app.get("/status/{task_id}")
async def get_status(task_id: str):
    if task_id not in task_status_db:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"task_id": task_id, "status": task_status_db[task_id]}

@app.get("/download-mesh/{task_id}")
async def download_mesh(task_id: str):
    if task_id not in task_status_db:
        raise HTTPException(status_code=404, detail="Task not found")
        
    if task_status_db[task_id] != "COMPLETED":
        raise HTTPException(status_code=400, detail="Mesh is not ready yet.")
        
    mesh_path = DATA_ROOT / task_id / "mesh" / "model.obj"
    if not mesh_path.exists():
        raise HTTPException(status_code=404, detail="Mesh file missing")
        
    return FileResponse(path=mesh_path, filename=f"v2m_{task_id}.obj")
