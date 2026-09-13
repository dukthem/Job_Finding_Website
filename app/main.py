from fastapi import FastAPI

app = FastAPI(title = "CareerPlus")

@app.get("/")
def root():
    return {"message": "CareerPluse API is up and running!"}