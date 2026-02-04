import uvicorn
from fastapi import FastAPI

app = FastAPI(title="Family Tree")

if __name__ == "__main__":
    uvicorn.run("familytree.main:app", host="0.0.0.0", port=8000, reload=True)