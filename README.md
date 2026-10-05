# 📦 Digital File Storage Optimizer

### Optimizing Limited Storage Using 0/1 Knapsack & Dynamic Programming

[![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)](https://www.python.org/)
[![Algorithm](https://img.shields.io/badge/Algorithm-0%2F1%20Knapsack-orange)]()
[![Technique](https://img.shields.io/badge/Technique-Dynamic%20Programming-green)]()
[![Project](https://img.shields.io/badge/DAA-Hackathon-purple)]()

A **Design and Analysis of Algorithms (DAA) Hackathon project** that solves a practical storage optimization problem using the **0/1 Knapsack algorithm with Dynamic Programming**.

The system selects the most valuable combination of files while ensuring that the total storage used never exceeds the available capacity.

---

## 🎯 Problem Statement

Digital devices have limited storage, but users often have multiple files with different sizes and levels of importance.

The challenge is:

> **How can we select the most important combination of files without exceeding the available storage capacity?**

Each file has:

* 📄 **Name**
* 💾 **Size**
* ⭐ **Importance**

The system determines the optimal subset of files that maximizes total importance within the storage limit.

---

## 💡 Core Idea

The problem is modeled as a **0/1 Knapsack Problem**.

| Knapsack Concept | Storage Optimizer        |
| ---------------- | ------------------------ |
| Item             | Digital File             |
| Weight           | File Size                |
| Value            | File Importance          |
| Capacity         | Available Storage        |
| Optimal Value    | Maximum Total Importance |

Each file has only two possible decisions:

```text
0 → Don't select the file
1 → Select the complete file
```

Partial selection of a file is not allowed.

---

## 🧠 Algorithm

### Dynamic Programming

We define:

```text
dp[i][w]
```

as the maximum importance achievable using the first `i` files with a storage capacity of `w`.

For every file, the algorithm considers two choices:

### 1. Exclude the file

```text
dp[i-1][w]
```

### 2. Include the file

```text
value[i] + dp[i-1][w-weight[i]]
```

Therefore:

```text
dp[i][w] =
max(
    dp[i-1][w],
    value[i] + dp[i-1][w-weight[i]]
)
```

If the file does not fit:

```text
dp[i][w] = dp[i-1][w]
```

---

## 🔄 System Workflow

```text
              USER INPUT
                  │
                  ▼
       ┌─────────────────────┐
       │ Storage Capacity    │
       │ File Name           │
       │ File Size           │
       │ File Importance     │
       └──────────┬──────────┘
                  │
                  ▼
          0/1 KNAPSACK
                  │
                  ▼
       DYNAMIC PROGRAMMING
                  │
                  ▼
        OPTIMAL SELECTION
                  │
                  ▼
       ┌─────────────────────┐
       │ Selected Files      │
       │ Storage Used        │
       │ Remaining Storage   │
       │ Maximum Importance  │
       └─────────────────────┘
```

---

## 🧪 Example

### Available Storage

```text
10 GB
```

### Input

| File   | Size | Importance |
| ------ | ---: | ---------: |
| File A | 2 GB |         30 |
| File B | 3 GB |         40 |
| File C | 4 GB |         50 |
| File D | 5 GB |         70 |

### Optimal Selection

```text
File A + File B + File D
```

### Result

```text
Storage Used       : 10 GB
Remaining Storage  : 0 GB
Maximum Importance : 140
```

The algorithm determines that this combination provides the maximum total importance without exceeding the 10 GB capacity.

---

## 🖥️ Sample Output

```text
============================================================
       DIGITAL FILE STORAGE OPTIMIZER
          0/1 KNAPSACK - DYNAMIC PROGRAMMING
============================================================

Enter available storage capacity (GB): 10
Enter number of files: 4

Selected Files:
  ✓ File A   Size: 2 GB   Importance: 30
  ✓ File B   Size: 3 GB   Importance: 40
  ✓ File D   Size: 5 GB   Importance: 70

------------------------------------------------------------
Total Storage Capacity : 10 GB
Total Storage Used     : 10 GB
Remaining Storage      : 0 GB
Maximum Importance     : 140
------------------------------------------------------------

Optimization Completed Successfully!
```

---

## 🛠️ Tech Stack

* **Language:** Python 3
* **Algorithm:** 0/1 Knapsack
* **Approach:** Dynamic Programming
* **IDE:** Visual Studio Code
* **Version Control:** Git & GitHub

### Dependencies

No external Python libraries are required.

---

## 📂 Project Structure

```text
Digital-File-Storage-Optimizer/
│
├── main.py
└── README.md
```

| File        | Description                                                   |
| ----------- | ------------------------------------------------------------- |
| `main.py`   | Complete implementation of the storage optimization algorithm |
| `README.md` | Project documentation                                         |

---

## ⚙️ Installation & Execution

### Prerequisites

Install **Python 3.x** on your system.

Verify the installation:

```bash
python --version
```

### Clone the Repository

```bash
git clone <YOUR-REPOSITORY-URL>
```

### Navigate to the Project

```bash
cd Digital-File-Storage-Optimizer
```

### Run the Application

```bash
python main.py
```

On Windows, you can also use:

```bash
py main.py
```

---

## 📊 Complexity Analysis

Let:

* `n` = number of files
* `W` = available storage capacity

| Metric           | Complexity   |
| ---------------- | ------------ |
| Time Complexity  | **O(n × W)** |
| Space Complexity | **O(n × W)** |
| Optimized Space  | **O(W)**     |

The standard implementation uses a two-dimensional DP table. The space complexity can be reduced to `O(W)` using a one-dimensional DP array.

---

## 🌍 Real-World Applications

The algorithm can be adapted to:

* 💻 Laptop and desktop storage optimization
* 📱 Smartphone storage management
* ☁️ Cloud storage allocation
* 💾 Backup file selection
* 🗄️ Data archiving
* 🖥️ Server storage management
* 📊 Dataset selection
* 🔄 Resource allocation systems

---

## 🚀 Future Enhancements

The current implementation focuses on the core algorithm. Future versions could include:

* 🌐 Web-based graphical interface
* 📁 Automatic file and folder scanning
* 💾 Real file metadata extraction
* ☁️ Cloud storage integration
* 🔍 Duplicate file detection
* 📈 Storage analytics and visualization
* ⭐ Automatic file-importance scoring
* 🤖 AI-assisted file prioritization
* 📱 Responsive interface for mobile devices

---

## 🎓 DAA Concepts Demonstrated

This project demonstrates practical application of:

* Algorithm Design
* 0/1 Knapsack
* Dynamic Programming
* Optimal Substructure
* Overlapping Subproblems
* Recurrence Relations
* Time Complexity
* Space Complexity
* Optimization Techniques

---

## 🏆 Project Objective

The primary objective is to demonstrate how a classical **Dynamic Programming algorithm** can be transformed into a practical solution for a real-world **resource optimization problem**.

> **Limited Storage → Intelligent Selection → Maximum Value**

---

## 🤝 Team Project

Developed as a **team project for a DAA Hackathon**.

The project focuses on algorithmic problem solving, optimization, and practical implementation of the **0/1 Knapsack problem**.

---

## 📜 License

This project is created for **educational and academic purposes** as part of a DAA Hackathon.
