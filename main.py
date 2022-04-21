from fastapi import FastAPI, File, UploadFile, File
import pandas as pd

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/")
async def root(input: UploadFile = File(...)):

    df = pd.read_csv(input.file)

    print(df.head())
    
    return {"file_name": input.filename}