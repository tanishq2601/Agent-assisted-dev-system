
from fastapi import FastAPI
from typing import List

# Create a FastAPI app instance
app = FastAPI()

# Define a function to calculate the Fibonacci series up to a maximum value
def generate_fibonacci(max_value: int) -> List[int]:
    fib_sequence = []
    a, b = 0, 1
    while b <= max_value:
        fib_sequence.append(b)
        a, b = b, a + b
    return fib_sequence

# Define a route to get the Fibonacci series from 1 to 100
@app.get("/fibonacci")
def get_fibonacci():
    fib_sequence = generate_fibonacci(100)
    return {"fibonacci_sequence": fib_sequence}
