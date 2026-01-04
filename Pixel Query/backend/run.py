import uvicorn

if __name__ == "__main__":
    # "app.main:app" points to the app object inside app/main.py
    uvicorn.run("app.main:app", host="0.0.0.0", port=10000)