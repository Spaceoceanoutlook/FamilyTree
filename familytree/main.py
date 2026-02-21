import uvicorn
from fastapi import FastAPI

from familytree.routes import auth, feedback, frontend, person, tree

app = FastAPI(title="Family Tree")

app.include_router(auth.router)
app.include_router(person.router)
app.include_router(feedback.router)
app.include_router(tree.router)
app.include_router(frontend.router)

if __name__ == "__main__":
    uvicorn.run("familytree.main:app", host="0.0.0.0", port=8000, reload=True)
