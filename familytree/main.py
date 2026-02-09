import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from familytree.routes import person, tree

app = FastAPI(title="Family Tree")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(person.router)
app.include_router(tree.router)

if __name__ == "__main__":
    uvicorn.run("familytree.main:app", host="0.0.0.0", port=8000, reload=True)
