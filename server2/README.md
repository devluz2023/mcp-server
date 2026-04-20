# Advertisement Scheduling Optimization

This project solves the television advertisement scheduling problem using optimization techniques.

## Problem Description

A TV network needs to allocate advertisers to available time slots to maximize total visibility. Each time slot can only have one advertiser, and each advertiser has different visibility scores for different slots based on audience demographics.

## Solution Approach

The solution uses two optimization approaches:
1. **Linear Programming** with SCIP solver
2. **Constraint Programming** with CP-SAT solver

Both approaches should give the same optimal solution for this assignment problem.

## Installation

1. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Place your visibility data in `visibilidade.csv` with:
   - Rows: Time slots
   - Columns: Advertisers
   - Values: Visibility scores

2. Run the optimization:
```bash
python otimizacao_aplicando_programacao_restricoes.py
```

## Output

The script will display:
- Visibility data summary
- Optimal allocations for both LP and CP approaches
- Total visibility achieved
- Comparison of results

## Clean Code Principles Applied

- **Single Responsibility**: Each class/method has one clear purpose
- **Descriptive Names**: Variables and functions use clear, English names
- **Type Hints**: All functions have type annotations
- **Documentation**: Comprehensive docstrings
- **Modularity**: Code organized in logical classes
- **Error Handling**: Proper handling of optimization failures