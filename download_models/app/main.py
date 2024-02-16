from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
  print("home")
  return {"Hello": "World"}


@app.get("/multilingual-e5-large-onnx.zip")
def get_model():
  print("Download model")
  return FileResponse(
    path="./app/multilingual-e5-large-onnx.zip",
    filename="multilingual-e5-large-onnx.zip",
  )
