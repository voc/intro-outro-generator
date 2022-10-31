import os
import make
import threading
import tarfile
import uuid
import tempfile
from typing import Union
from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def save_bin_file(location, file):
    with open(location, 'wb') as out_file:
        out_file.write(file)  # async write
#tempfile wasn't used because the tempdir method does not have a arg for disabiling deletion upon closing the programm.
def create_work_dir():
    uid = str(uuid.uuid4().int)
    path = "/tmp/" + uid
    os.mkdir(path)
    return uid, path

def thread_active(uid: int):
    for i in threading.enumerate():
        if i.name == str(uid):
            return True
    return False

def package(output_dir, source_dir):
    with tarfile.open(output_dir + ".tar.gz", "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))


#@app.get("/progress/{uid}"):
#async def progress(uid: int):
#    status = {"done": False,
#              "progess": 87,
#              "left": 167}
#    if os.path.exists(f"/tmp/{str(uid)}/tasks_left"):
#        with open(f"/tmp/{str(uid)}/tasks_left", "w") as file:
#            file
#
#    return status
        
@app.get("/download/{uid}")
async def download(uid: int):
    if not thread_active(uid) and os.path.isdir(f"/tmp/{str(uid)}"):
        package(f"/tmp/{str(uid)}/output", f"/tmp/{str(uid)}/output")

        return FileResponse(f"/tmp/{str(uid)}/output.tar.gz", media_type='application/octet-stream', filename="intros_outros.tar")
#else:
#        return {"status": "not done"}


@app.post("/generate")
async def generate(schedule: str = Form(), intro: UploadFile = Form(), outro: UploadFile = Form()):
    uid, temp_dir = create_work_dir()
    print(temp_dir)
    os.mkdir(temp_dir + "/output")
    os.mkdir(temp_dir + "/artwork")
    save_bin_file(temp_dir + "/artwork/intro.svg", intro.file.read())
    save_bin_file(temp_dir + "/artwork/outro.svg", outro.file.read())
    thread = threading.Thread(target=make.main, args=(temp_dir, schedule), name=uid)
    #thread = threading.Thread(target=make.main, args=(temp_dir, schedule, [1]), name=uid)
    thread.setDaemon(True)
    thread.start()
    return {"id": uid}

@app.get("/")
async def main():
    content = """
<body>
<form action="/generate/" enctype="multipart/form-data" method="post">
<input name="schedule" type="text">
<input name="intro" type="file">
<input name="outro" type="file">
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)

