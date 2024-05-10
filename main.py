from fastapi import FastAPI


app = FastAPI(title="Fitness Club")


@app.get("/")
def root():
    return {"page": "root"}
