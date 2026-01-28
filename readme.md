# CDP-Lite

**CDP-Lite** is a prototype system for integrating, unifying, and analyzing customer data, with visualization of RFM segmentation results. This project was developed as a student group project.

## Project Goal
- Collect customer data from multiple sources (CSV, JSON)  
- Unify customer profiles and remove duplicates  
- Perform RFM (Recency, Frequency, Monetary) segmentation analysis  
- Visualize analysis results using Power BI dashboards  

## Responsibilities / Contributions
- System architecture design and module planning
- GUI development and data import functionality
- Docker Compose setup for MySQL
- Code refactoring and final improvements  

Team members:  
- Julia – `processdata.py` module  
- Daniel – `rfmanalysis.py` module and Power BI report  

## Technologies
- Python 3.10+ (GUI: `ttkbootstrap`)  
- MySQL (Docker Compose)  
- Power BI Desktop  
- Python libraries: `pandas`, etc.  
- Docker  

## Architecture
- **Presentation Layer (GUI):** central data management panel (`app.py`)  
- **Business Layer:** modules for data processing (`importfiles.py`, `processdata.py`, `rfmanalysis.py`, `openreport.py`, `viewlogs.py`)  
- **Data Layer:** MySQL database, `db.py` interface, CSV output files  
- **Configuration Layer:** `config.py` (paths, environment variables, logging)  

## Features
- **Import data:** select and import CSV/JSON files, verify formats, assign unique filenames, log operations  
- **Process data:** validate, normalize, unify data, remove duplicates, save to MySQL database  
- **RFM Analysis:** calculate RFM indicators and save results to CSV  
- **Open Power BI report:** open prepared dashboard to visualize analysis results  
- **Processing history:** view log of executed operations 

## Installation & Usage
1. Install Python 3.10+  
2. Install Docker Desktop (with Docker Compose support)  
3. Install Power BI Desktop  
4. Install Python dependencies:  
    ```bash
    pip install -r requirements.txt
    ```
5. Start MySQL database in Docker:
    ```bash
    docker compose up -d
    ```
6. Launch the application:
    ```bash
    python app.py
    ```
7. Use the GUI buttons in order: Import Data -> Process Data -> RFM Analysis -> Open Power BI Report -> Processing History.

## Project Folder Structure
- **staging/** – imported source files
- **processed/** – archived source files
- **rfm_analysis/** – RFM analysis results
- **report/** - Power BI report
- **logs/** – operation logs

## Screenshots

### GUI:
![GUI](/docs/gui.png)

### Power BI report:
![Power BI report](/docs/report.png)