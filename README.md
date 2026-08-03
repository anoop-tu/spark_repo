# Learning PySpark

A learning repository documenting self-study of Apache Spark and PySpark, organized as a series of Jupyter Notebooks covering progressively deeper concepts from fundamentals through advanced data processing techniques.

## Stack
- **Language(s):** Python (via Jupyter Notebooks)
- **Framework / runtime:** Apache Spark / PySpark
- **Notable libraries:** PySpark (Spark's Python API)

## Repository Structure

### Root-Level Reference Files
Architecture and workflow visuals related to Spark/YARN execution:
- `hdi-yarn-architecture.png` - HDInsight YARN architecture diagram
- `yarn_job_submission_flow.png` - YARN job submission flow
- `yarn_hdfs_full_cluster_map.svg` - Cluster and HDFS mapping visual

### week4practice - RDDs and Basic Spark Operations
Covers RDD fundamentals, caching strategies, repartitioning, and join operations:
- `spark_basics-*.ipynb` - Introduction to Spark core concepts
- `rdd_cache.ipynb` - RDD caching and performance optimization
- `repart_coaelesce.ipynb` - Data partitioning techniques
- `spark_joins_*.ipynb` - Join operations
- `week4-assignments-*.ipynb` - Practice assignments

### week5 practice - DataFrames and Transformations
Explores DataFrame API and data transformations:
- `week5lessons*.ipynb` - Lesson notebooks on DataFrame operations
- `week5_assignment-*.ipynb` - Practice assignments

### week6practice - Spark SQL and Query Optimization
Focuses on Spark SQL and query optimization:
- `week6lesson*.ipynb` - SQL fundamentals and optimization techniques
- `week6_assignement-*.ipynb` - Practice assignments

### week7practice - Advanced Topics
Covers specialized and advanced Spark concepts:
- `week7lesson*.ipynb` - Advanced topics and patterns
- `week7Assignment*.ipynb` - Practice assignments

### week8practice - Extended Practice and Advanced Workflows
Adds additional lesson and assignment notebooks for continued Spark practice:
- `week8lesson*.ipynb` - Week 8 lessons
- `week8assignment*.ipynb` - Week 8 assignments

## How to Run

Open individual `.ipynb` files in Jupyter Notebook or JupyterLab:

```bash
# Using Jupyter Notebook
jupyter notebook

# Or using JupyterLab
jupyter lab
```

Then navigate to any week's folder and open the notebook of your choice.

### Prerequisites
- Python 3.x
- Jupyter Notebook or JupyterLab
- PySpark: `pip install pyspark`

## Learning Path

The repository follows a structured progression:
1. **Week 4** - Master RDD fundamentals, caching, and join operations
2. **Week 5** - Learn DataFrame API and transformations
3. **Week 6** - Study Spark SQL and query optimization
4. **Week 7** - Explore advanced topics and patterns
5. **Week 8** - Continue with advanced lessons and applied practice
