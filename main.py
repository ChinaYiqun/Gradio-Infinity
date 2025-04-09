import os
import shutil
#import infinity
import infinity_embedded as infinity
import numpy as np
import pandas as pd

class InfinityDatabaseSingleton:
    _instance = None
    _initialized = False

    def __new__(cls, db_name, table_name, table_columns,address):
        if cls._instance is None:
            cls._instance = super(InfinityDatabaseSingleton, cls).__new__(cls)
            cls._initialized = False
        return cls._instance

    def __init__(self, db_name, table_name, table_columns,address):
        if self._initialized:
            return
        self.db_name = db_name
        self.table_name = table_name
        self.table_columns = table_columns
        self.address = address
        self.infinity_object = None
        self.db_object = None
        self.table_object = None
        self.initialize()
        self._initialized = True

    def initialize(self):
        try:
            self.infinity_object = infinity.connect(self.address)
            self.db_object = self._get_or_create_database()
            self.table_object = self._get_or_create_table()
        except Exception as e:
            print(f"初始化数据库时出错: {e}")

    def _get_or_create_database(self):
        try:
            db = self.infinity_object.get_database(self.db_name)
            print(f"数据库 '{self.db_name}' 已存在")
            return db
        except Exception:
            print(f"数据库 '{self.db_name}' 不存在，正在创建...")
            try:
                db = self.infinity_object.create_database(
                    self.db_name,
                    conflict_type=infinity.common.ConflictType.Ignore
                )
                print(f"数据库 '{self.db_name}' 创建成功")
                return db
            except Exception as e:
                print(f"创建数据库 '{self.db_name}' 失败: {e}")

    def _get_or_create_table(self):
        try:
            table = self.db_object.create_table(
                self.table_name,
                self.table_columns,
                infinity.common.ConflictType.Ignore
            )
            print(f"表 '{self.table_name}' 创建成功")
            return table
        except Exception as e:
            print(f"创建表 '{self.table_name}' 失败: {e}")
    def drop_table(self):
        try:
            self.db_object.drop_table(self.table_name, infinity.common.ConflictType.Ignore)
            print(f"表 '{self.table_name}' 已删除")
        except Exception:
            print(f"表 '{self.table_name}' 不存在，无需删除")
    def insert_data(self, data):
        if self.table_object:
            try:
                # 移除数据中的 num 字段
                for item in data:
                    item.pop('num', None)
                self.table_object.insert(data)
                print("数据插入成功")
            except Exception as e:
                print(f"数据插入失败: {e}")
        else:
            print("表对象不存在，无法插入数据")

    def create_indexes(self):
        if self.table_object:
            try:
                res = self.table_object.create_index(
                    "my_index",
                    infinity.index.IndexInfo("chunk_text", infinity.index.IndexType.FullText),
                    infinity.common.ConflictType.Error,
                )
                print("索引创建成功")
            except Exception as e:
                print(f"索引创建失败: {e}")
        else:
            print("表对象不存在，无法创建索引")

    def perform_queries(self, questions):
        results = []
        if self.table_object:
            for question in questions:
                df, extra_res = (
                    self.table_object.output(["chunk_text", "_score"])
                    .match_text("chunk_text", question, 10)
                    .to_df()
                )
                results.append(df)
                print(f"question: {question}")
                print(df)
        else:
            print("表对象不存在，无法执行查询")
        return results

    def get_table(self):
        return self.table_object

    def delete_table(self, table_name):
        if self.table_object:
            try:
                self.db_object.drop_table(table_name)
                print(f"表 '{table_name}' 已删除")
                self.table_object = None
            except Exception as e:
                print(f"无法删除表 '{table_name}': {e}")
        else:
            print(f"表 '{table_name}' 不存在")

    def insert_emb(self, data):
        if self.table_object:
            try:
                if len(data.get("vector", [])) != 768:
                    print("插入数据的向量维度不是 768 维，插入失败。")
                    return
                self.table_object.insert(data)
                print("数据插入成功")
            except Exception as e:
                print(f"数据插入失败: {e}")
        else:
            print("表对象不存在，无法插入数据")

    def delete_emb(self, condition):
        if self.table_object:
            try:
                self.table_object.delete(condition)
                print("数据删除成功")
            except Exception as e:
                print(f"数据删除失败: {e}")
        else:
            print("表对象不存在，无法删除数据")

    def match_dense(self, vector_column_name, embedding_data, embedding_data_type, distance_type, topn, knn_params=None):
        if self.table_object:
            try:
                df, extra_res = self.table_object.output(["*"]).match_dense(
                    vector_column_name,
                    embedding_data,
                    embedding_data_type,
                    distance_type,
                    topn,
                    knn_params
                ).to_df()
                print("稠密向量搜索结果：")
                print(df)
                return df
            except Exception as e:
                print(f"稠密向量搜索失败: {e}")
        else:
            print("表对象不存在，无法执行稠密向量搜索")


    def delete_by_condition(self, condition):
        if self.table_object:
            try:
                self.table_object.delete(condition)
                print("数据删除成功")
            except Exception as e:
                print(f"数据删除失败: {e}")
    def list_all_by_filename(self,):
        if self.table_object:
            try:
                df, extra_res = self.table_object.output(["*"]).to_df()
                grouped = df.groupby('filename').agg({
                    'file_uuid': 'first',
                    'vector': 'count',
                    'chunk_text': lambda x: x.str.len().sum()
                }).reset_index()

                # 重命名列
                grouped.rename(columns={'chunk_text': 'char_num', 'vector': 'chunk_num'}, inplace=True)
                print("查询结果：")
                print(grouped)
                return grouped
            except Exception as e:
                print(f"查询失败: {e}")


# 使用示例
if __name__ == "__main__":
    db_name = "my_db"
    table_name = "my_table"
    table_columns = {
        "chunk_text": {"type": "varchar", "default": ""},
        "file_uuid": {"type": "varchar", "default": ""},
        "filename": {"type": "varchar", "default": ""},
        "vector": {"type": "vector, 4, float"},
    }
    address = infinity.common.LOCAL_HOST
    address = "/mnt/d/pycharmProject/infinity/TMP"
    singleton = InfinityDatabaseSingleton(db_name, table_name, table_columns,address)

    data = [
        {
            "chunk_text": r"unnecessary and harmful",
            "vector": [1.0, 1.2, 0.8, 0.9],
            "filename": "test1.txt",
            "file_uuid": "1234567890"
        },
        {
            "chunk_text": r"Office for Harmful Blooms",
            "vector": [4.0, 4.2, 4.3, 4.5],
            "filename": "test2.txt",
            "file_uuid": "1234567890"
        },
        {
            "chunk_text": r"A Bloom filter is a space - efficient probabilistic data structure, conceived by Burton Howard Bloom in 1970, that is used to test whether an element is a member of a set.",
            "vector": [4.0, 4.2, 4.3, 4.5],
            "filename": "test2.txt",
            "file_uuid": "1234567893"
        },
        {
            "chunk_text": r"The American Football Conference (AFC) harm chemical anarchism add test is one of harm chemical the two conferences of the National Football League (NFL). This add test conference and its counterpart, the National Football Conference (NFC), currently contain 16 teams each, making up the 32 teams of the NFL. The current AFC title holder is the New England Patriots.",
            "vector": [4.0, 4.2, 4.3, 4.5],
        },
    ]
    singleton.insert_data(data)
    singleton.create_indexes()

    questions = [
        r"blooms",
        r"Bloom filter",
        r'"Bloom filter"',
        r"space efficient",
        r"space\-efficient",
        r'"space\-efficient"',
        r'"harmful chemical"~10',
    ]
    query_results = singleton.perform_queries(questions)

    # 示例稠密向量搜索
    singleton.match_dense("vector", [1.0, 1.2, 0.8, 0.9], "float", "l2", 100)
    singleton.delete_by_condition("filename = 'test1.txt'")
    singleton.list_all_by_filename()
    singleton.delete_table(table_name)