from fastapi import FastAPI

app = FastAPI(title="Questify API")


@app.get("/")
def read_root():
    return {"message": "Welcome to Questify API"}
