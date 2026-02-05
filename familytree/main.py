import uvicorn
from fastapi import FastAPI

from familytree.routers import person

app = FastAPI(title="Family Tree")

app.include_router(person.router)

if __name__ == "__main__":
    uvicorn.run("familytree.main:app", host="0.0.0.0", port=8000, reload=True)
