## Gradio-Infinity

### Introduction to `main.py`

The `main.py` file defines a singleton class `InfinityDatabaseSingleton` for interacting with the Infinity database. Here's a brief overview of its usage:

#### 1. Initialization
```python
from main import InfinityDatabaseSingleton

db_name = "my_db"
table_name = "my_table"
table_columns = {
    "chunk_text": {"type": "varchar", "default": ""},
    "file_uuid": {"type": "varchar", "default": ""},
    "filename": {"type": "varchar", "default": ""},
    "vector": {"type": "vector, 4, float"},
}
address = "/mnt/d/pycharmProject/infinity/TMP"
singleton = InfinityDatabaseSingleton(db_name, table_name, table_columns, address)
```
This code initializes a singleton instance of the database connection. If the database or table does not exist, it will be created.

#### 2. Data Insertion
```python
data = [
    {
        "chunk_text": r"unnecessary and harmful",
        "vector": [1.0, 1.2, 0.8, 0.9],
        "filename": "test1.txt",
        "file_uuid": "1234567890"
    },
    # more data...
]
singleton.insert_data(data)
```
This inserts data into the table. Note that the `num` field in the data will be removed before insertion.

#### 3. Index Creation
```python
singleton.create_indexes()
```
This creates a full - text index on the `chunk_text` column.

#### 4. Query Execution
```python
questions = [
    r"blooms",
    r"Bloom filter",
    # more questions...
]
query_results = singleton.perform_queries(questions)
```
This performs text matching queries on the `chunk_text` column and returns the results.

#### 5. Dense Vector Search
```python
singleton.match_dense("vector", [1.0, 1.2, 0.8, 0.9], "float", "l2", 100)
```
This performs a dense vector search on the `vector` column.

#### 6. Data Deletion
```python
singleton.delete_by_condition("filename = 'test1.txt'")
```
This deletes data that meets the specified condition.

#### 7. Listing Data by Filename
```python
singleton.list_all_by_filename()
```
This groups data by `filename` and aggregates some information.

#### 8. Table Deletion
```python
singleton.delete_table(table_name)
```
This deletes the specified table.


### Introduction to `index.py`

The `index.py` file creates a Gradio interface for interacting with the Infinity database using the `InfinityDatabaseSingleton` class from `main.py`.

#### 1. Initialization
```python
from main import InfinityDatabaseSingleton
import pandas as pd

db_name = "my_db"
table_name = "my_table"
table_columns = {
    "chunk_text": {"type": "varchar", "default": ""},
    "file_uuid": {"type": "varchar", "default": ""},
    "filename": {"type": "varchar", "default": ""},
    "vector": {"type": "vector, 4, float"},
}
address = "/mnt/d/pycharmProject/infinity/TMP"
db_singleton = InfinityDatabaseSingleton(db_name, table_name, table_columns, address)
```
This initializes the database singleton instance and inserts some sample data and creates an index.

#### 2. Gradio Interface
The Gradio interface provides the following functions:
- **Insert Data**: Enter `file_uuid`, `filename`, `chunk_text`, and `vector`, then click the button to insert data.
- **Delete Data**: Enter a deletion condition and click the button to delete data.
- **Search Data**: Enter a search vector, `filename`, and the number of results to return, then click the button to perform a search.
- **Delete Table**: Click the button to delete the table.
- **Delete Work Place**: Click the button to delete the work directory.
- **List All Data**: Click the button to list all data in the table.

```python
import gradio as gr

with gr.Blocks() as demo:
    gr.Markdown("### Infinity 数据库操作界面")
    # Tabs and buttons...
    demo.launch()
```
This code launches the Gradio interface, allowing users to interact with the database through a graphical user interface.


# Detailed Introduction to Infinity Database

Infinity is a high - performance database focusing on vector data processing. It combines the capabilities of traditional databases with advanced indexing technologies, making it suitable for large - scale vector retrieval and hybrid search scenarios. The following is an in - depth introduction from the aspects of core functions, indexing capabilities, unique advantages, algorithm references, and limitations:

## I. Core Functions of Traditional Databases
Infinity retains the basic operation capabilities of relational databases, supporting multi - dimensional data management:
- **Basic Data Operations**:
    It provides Create, Read, Update, and Delete (CRUD) operations at the **database/table/column** granularity, which is compatible with the conventional processing logic of structured data.
- **Data Processing Capabilities**:
    It supports data grouping, pagination, and keyword highlighting, meeting the requirements of complex queries and data presentation.

## II. Index Support Capabilities
### 2.1 Diverse Index Types
Infinity supports a variety of indexing technologies, adapting to different data forms and business scenarios:
- **Vector Indexes**:
    - **HNSW**: It supports hyperparameter tuning (such as the number of connections `M` and the number of candidate neighbors `ef_construction`), optimizing the retrieval efficiency of high - dimensional vectors.
    - **IVF**: It supports scalar quantization and product quantization, providing storage optimizations such as `int8/uint8/float16/bfloat16` to reduce memory usage.
- **Text Indexes**:
    - **FullText**: It integrates multi - language analyzers (Standard analyzer, RAGFLOW tokenizer, IK tokenizer, etc.) and supports boolean expression search (similar to Elasticsearch), adapting to complex text queries.
- **Structured Indexes**:
    - **Secondary**: It is suitable for standard structured data tables, accelerating equal - value/range queries.
    - **BMP**: It is a relational index based on bitmap storage, optimizing the performance of multi - condition filtering scenarios.

### 2.2 Multi - level Indexing and Optimization
- It supports **multi - level index combinations** (such as vector index + text index), enabling efficient queries in hybrid retrieval scenarios.
- It provides an automatic index optimization mechanism, dynamically adjusting index parameters according to data distribution and query patterns, reducing the cost of manual tuning.

## III. Core Advantage Features
### 3.1 Flexible Filtering and Fusion Capabilities
- **Filter Capability**: It supports complex conditional filtering (such as numerical range, text matching), accurately screening the target data subset.
- **Fusion Capability**: It has built - in algorithms such as **RRF (Re - ranking with Reciprocal Rank Fusion)** and **Weighted Sum** for sorting, integrating the retrieval results of multiple indexes to improve the accuracy of hybrid search.

### 3.2 Deep Integration of Re - ranking Technology
- It supports **fine - grained re - ranking (Rerank)** based on Transformer - Tensor, seamlessly integrating deep learning models (such as BERT, Sentence - BERT) to optimize the relevance of retrieval results.

### 3.3 Diverse Deployment and Invocation Methods
- **Deployment Modes**: It supports both embedded and HTTP service modes, adapting to edge devices (embedded) and distributed clusters (HTTP) scenarios.
- **Client Support**: It provides native Python interfaces and HTTP APIs, facilitating multi - language development and cross - platform invocation.
- **Distributed Expansion**: It supports a horizontally scalable architecture to handle high - concurrency retrieval requirements for data at the scale of hundreds of millions.

### 3.4 Comprehensive Performance Evaluation
- It provides detailed **Benchmark reports** (see [Infinity Evaluation Documentation](https://infiniflow.org/docs/benchmark)), validating performance based on public datasets such as SIFT1M.
- Actual measurement data: After vectorizing 1 million 128 - dimensional vector data, the disk space only expands by **1.34 times**, leading in storage efficiency.

## IV. Search Algorithm Selection Reference
According to the deployment environment (device energy consumption), search scenario (real - time/accuracy requirements), and downstream tasks (recommendation, Q&A, etc.), you can refer to the following resources to select algorithms:
- [Multi - Retrieval Algorithm Evaluation of Infinity](https://infiniflow.org/blog/multi - way - retrieval - evaluations - on - infinity - database): It analyzes the performance of algorithms such as HNSW and IVF on different datasets.
- [Hybrid Search Optimization Practice](https://techcommunity.microsoft.com/t5/ai - azure - ai - services - blog/azure - ai - search - outperforming - vector - search - with - hybrid/ba - p/3929167#searchconfiguration): Learn from Microsoft's engineering experience in hybrid retrieval (vector + text).

## V. Limitations and Precautions
### 5.1 Platform Compatibility Limitations
- **Only Supports Linux**: It does not support Windows/macOS for now. You need to manually compile it to adapt to non - Linux environments (see [Issue #1286](https://github.com/infiniflow/infinity/issues/1286)).

### 5.2 Query Optimization Depends on Manual Work
- It lacks an automatic query optimizer. In complex business scenarios, developers need to optimize table structures and SQL statements, which is not suitable for complex queries with high - performance requirements.

### 5.3 Lack of Logs in Embedded Mode
- The Embedded mode does not have a built - in logging system. External tools need to be additionally integrated for fault troubleshooting and performance monitoring.

### 5.4 Low Community Activity
- The open - source community is currently less active. The speed of feature iteration and problem response may be limited, which is more suitable for teams with strong independent technical capabilities.

## Conclusion
Infinity database performs excellently in vector retrieval and hybrid search scenarios, especially suitable for scenarios with requirements for storage efficiency, index flexibility, and deep learning integration. Despite limitations such as platform compatibility and query optimization, its technical architecture and performance evaluation still provide important references for similar products. It is recommended to choose the deployment mode according to the specific business scale and technology stack, and pay attention to the community dynamics for continuous optimization support. 