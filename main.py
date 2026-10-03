from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class FileItem(BaseModel):
    name: str
    size: float
    importance: float

class OptimizeRequest(BaseModel):
    capacity: float
    files: list[FileItem]

@app.post("/optimize")
def optimize(data: OptimizeRequest):
    # 0/1 knapsack
    capacity = int(data.capacity)
    files = data.files

    dp = [0] * (capacity + 1)
    selected = [[] for _ in range(capacity + 1)]

    for file in files:
        size = int(file.size)
        value = file.importance

        for c in range(capacity, size - 1, -1):
            new_value = dp[c - size] + value

            if new_value > dp[c]:
                dp[c] = new_value
                selected[c] = selected[c - size] + [file.name]

    best_capacity = max(range(capacity + 1), key=lambda c: dp[c])

    return {
        "selected": selected[best_capacity],
        "total_size": sum(
            f.size for f in files
            if f.name in selected[best_capacity]
        ),
        "total_importance": dp[best_capacity]
    }
