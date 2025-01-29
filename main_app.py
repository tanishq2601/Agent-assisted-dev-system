
from fastapi import FastAPI

app = FastAPI()

@app.get("/fibonacci")
def get_fibonacci():
    fib_series = []
    a, b = 0, 1
    while b <= 100:
        if b >= 1:
            fib_series.append(b)
        a, b = b, a + b
    return {"fibonacci_series": fib_series}
