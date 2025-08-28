# Bitcoin Blockchain Transaction Scraper and Analysis

A simple tool to scrape Bitcoin transcation data on Blockchain and analyze anomalies transactions.

## Prerequisites

- Python 3.10 or higher

## Installation

1. **Clone the repository** and navigate to the project folder:
   ```bash
   git clone https://github.com/billycemerson/Bitcoin-Blockchain
   cd Bitcoin-Blockchain
   ```

2. **Install dependencies**:
   
   **Using pip**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Navigate to the source folder**:
   ```bash
   cd src
   ```

2. **Run the scraper**:
   ```bash
   python extract.py
   ```

3. **Run the transform**:
   ```bash
   python transform.py
   ```

4. **Run the model**:
   ```bash
   python model.py
   ```

## File Structure

```
Bitcoin-Blockchain/
├── src/
│   ├── extract.py            # Main scraper script
│   ├── transform.py          # Example for transform data
│   ├── model.py              # Code for anomalies dtection
│   └── analyze.ipynb         # Notebook for EDA and simple transaction plot (graph)
├── data/
│   ├── data.json             # Output scraping
│   ├── data_transform.json   # Output transform
│   ├── result.json           # Output modelling
│   ├── result.csv            # Output modelling
│   └── variable.json         # Output the importance of variable
└── README.md                 # This file
```