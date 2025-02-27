# **Data Pipeline Automation**

The project focuses on automating data workflows using **Apache Airflow**, validating data with **Great Expectations**, and integrating with **Elasticsearch and Kibana**.

---

## **Project Overview**

The goal of this project is to automate a **data pipeline** that extracts data from PostgreSQL, cleans and validates it, and loads the processed data into Elasticsearch for further analysis using Kibana.

### **Key Components:**
1. **Apache Airflow** – Orchestrating the data pipeline.
2. **Great Expectations** – Performing data validation.
3. **PostgreSQL** – Storing raw and cleaned data.
4. **Elasticsearch & Kibana** – Storing and visualizing processed data.

---

## **Project Structure**

```
📂 P2-M3_nikoahakam
│── 📂 great_expectations/gx       # Data validation configs and reports
│── 📂 images                      # Screenshots of DAG and data visualizations
│── P2M3_nikoahakam_DAG.py         # Apache Airflow DAG script
│── P2M3_nikoahakam_DAG_graph.png  # DAG workflow screenshot
│── P2M3_nikoahakam_GX.ipynb       # Great Expectations validation script
│── P2M3_nikoahakam_data_clean.csv # Cleaned dataset
│── P2M3_nikoahakam_data_raw.csv   # Original raw dataset
│── P2M3_nikoahakam_ddl.txt        # DDL & DML SQL script
│── README.md                      # Project documentation
│── README_steps.md                 # Step-by-step guide
```

---

## **Dataset Information**
- **Source**: [Sample - Superstore Dataset](https://github.com/ardhiraka/DEBlitz)
- **Description**: The dataset contains order transactions, customer details, and product information.

---

## **Installation & Setup**

### **Prerequisites**
1. Install **Docker** and **Docker Compose**.
2. Clone the repository:
   ```sh
   git clone https://github.com/YOUR_GITHUB_USERNAME/P2-M3_nikoahakam.git
   cd P2-M3_nikoahakam
   ```

### **Run Services**
Start the environment using Docker:
```sh
docker-compose -f airflow_ES.yaml up -d
```

### **Access Services**
- **Airflow UI**: `http://localhost:8080`
- **PostgreSQL**: `localhost:5434`
- **Elasticsearch**: `http://localhost:9200`
- **Kibana**: `http://localhost:5601`

---

## **Data Pipeline Workflow**
The pipeline consists of **three automated tasks** in Airflow:

1. **Fetch from PostgreSQL**  
   - Extracts raw data from `table_m3` in PostgreSQL.
2. **Data Cleaning**  
   - Cleans column names, removes duplicates, handles missing values, and standardizes formats.
3. **Post to Elasticsearch**  
   - Loads the cleaned data into Elasticsearch.

### **DAG Workflow**
![DAG Workflow](images/P2M3_nikoahakam_DAG_graph.png)

---

## **Data Validation**
The dataset is validated using **Great Expectations** with the following rules:
✅ **Unique values** check  
✅ **Range constraints** for numerical values  
✅ **Data type validation**  
✅ **Regex pattern matching** for `customer_id`  

More details in [`P2M3_nikoahakam_GX.ipynb`](P2M3_nikoahakam_GX.ipynb).

---

## **Exploratory Data Analysis**
Kibana is used to analyze and visualize the cleaned dataset.  
📊 **6 Key Visualizations**:
- Horizontal & Vertical Bar Charts
- Pie Chart
- Additional Custom Charts
- Markdown for **Introduction & Conclusions**

---

## **Step-by-Step Guide**
A detailed **step-by-step guide** for setting up and running the project is available in [`README_steps.md`](README_steps.md).

---

## **DDL & DML (Database Setup)**
The SQL script for setting up the database is available in:
📄 [`P2M3_nikoahakam_ddl.txt`](P2M3_nikoahakam_ddl.txt)

---

## **Acknowledgments**
For any issues, feel free to reach out or create an **Issue** in this repository. 🚀

