# File Cleaner & Duplicate Detector

A highly efficient standalone command-line Python application designed to inspect system directories, identify duplicate files using accurate SHA-1 digital fingerprint signatures, find temporary files via Regex patterns, and safely optimize disk storage space.

And this application natively utilizes explicit UTF-8 character encoding for cross-platform file handling and JSON serialization.

## Technical Elements Implemented

- **OOP Architecture & Inheritance:** Modular code design built on an advanced object hierarchy featuring a common base scanner (`BaseScanner`) and distinct specialized child classes (`DuplicateDetector` and `TempCleaner`).
- **Control Statements & Operators:** Comprehensive user input loops (`while`, `for`, `if`), safe state evaluations, and short-circuit logical boundaries.
- **Functions & Lambdas:** Custom modular parsing routines combined with a lambda-driven (`lambda path_str: ...`) multi-parameter sorting optimization that organizes duplicate file structures by directory depth.
- **Custom Decorator:** `@safe_execution` implements an active permission gatekeeping layer to protect systemic resources by validating OS rights before executing nested operations.
- **Collections & Comprehensions:** Optimized dictionary mapping tracking, explicit set operations to prevent double-deletion bugs, and dynamic filtering comprehensions.
- **Generators:** Utilizes specialized `yield` statements inside directory scans to safely iterate through massive system folders lazily without memory footprint spikes.
- **File Handling, Context Managers & Serialization:** Parses target directories via context-managed expressions (`with`) and dumps a structured log's to (`report.json`).
- **Regular Expressions:** Pre-compiled regex patterns to rapidly index and flag volatile system cache layers like `.tmp` and `.log` formats.
- **Error & Exception Handling:** Multi-tier catch matrices resolving locked resource states using a custom subclass exception (`CriticalFileAccessError`) providing clean, informative terminal alerts.

## Installation & Dependencies

- Python 3.10 or higher installed on your system.
- This project primarily uses Python's built-in standard libraries. However, it supports enhanced ASCII art for the user interface if `pyfiglet` is available.

To install optional visual dependencies, run:
```bash
pip install pyfiglet
```

### Execution Steps
1. Extract the project contents into your preferred working folder.
2. Open your terminal or command prompt inside the project root folder.
3. Launch the application by running:
```bash
python main.py
```

## Running Instructions

Select option 1 or 2. If you choose 2, enter your absolute folder path.

Review the Storage Density Report to see what percentage of your storage is occupied by different file size categories (Tiny, Small, Medium, Large).

The system will prompt you: » Queue these files for erase permanently? (y/n):. Type y to select temp files for deletion.

Next, review the discovered duplicate groups. The application uses a smart sorting algorithm to preserve the shortest file path as the 'Original' and marks the rest as redundant replicas. Type y to queue them.

To execute the data destruction protocol, type yes when prompted.

After completion, check your directory root for a newly generated ```report.json``` file to view your structural log.