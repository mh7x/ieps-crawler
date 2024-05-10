# Web Data Extraction

This project demonstrates three different approaches for structured data extraction from HTML web pages:

- **A. Regular Expression (Regex) Extraction**
- **B. XPath Extraction**
- **C. Automatic Web Extraction Algorithm**

## Getting Started

To run the code, follow the steps below:

### Prerequisites

- Python 3.x
- Required Python packages: `lxml`, `beautifulsoup4`, `scikit-learn`

Install the required packages using pip:

```bash
pip install lxml beautifulsoup4 scikit-learn
```

## Running the Code
1. Clone this repository to you local machine
2. Navigate to pa2/implementation-extraction.
3. Run the script 'run-extraction.py' with the desired algorithm type as the argument. For example:

```bash
python run-extraction.py A
```
Replace 'A' with 'B' or 'C' to test the respective algorithms.

## Output
The extracted data will be printed to the standard output for all the web pages used in the test.

## File Structure
The project structure is as follows:

```plaintext
.
├── pa2/
│   ├── README.md
│   ├── report-extraction.pdf
│   ├── implementation-extraction/
│   │   ├── main.py
│   │   └── run-extraction.py
│   └── input-extraction/
│       ├── rtvslo.si/
│       ├── overstock.com/
│       ├── 24ur.com/
│       └── kosarka.si/
```

- 'main.py': Contains the implementations of the extraction methods.
- 'run-extraction.py': Script to run and test the extraction methods.
- 'wepbages/': Directory containing pre-rendered HTML web pages for testing.

## Authors
[Tadej Lenart, ]