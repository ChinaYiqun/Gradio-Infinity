import gradio as gr
from main import InfinityDatabaseSingleton
import pandas as pd
# 数据库配置
db_name = "my_db"
table_name = "my_table"
table_columns = {
    "chunk_text": {"type": "varchar", "default": ""},
    "file_uuid": {"type": "varchar", "default": ""},
    "filename": {"type": "varchar", "default": ""},
    "vector": {"type": "vector, 4, float"},
}
# address = infinity.common.LOCAL_HOST
address = "/mnt/d/pycharmProject/infinity/TMP"
db_singleton = InfinityDatabaseSingleton(db_name, table_name, table_columns, address)
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
db_singleton.insert_data(data)
db_singleton.create_indexes()

def insert_data(file_uuid, filename, chunk_text, vector):
    data = {
        "file_uuid": file_uuid,
        "filename": filename,
        "chunk_text": chunk_text,
        "vector": vector
    }
    db_singleton.insert_emb(data)
    return "数据插入成功"

def delete_data(condition):
    db_singleton.delete_emb(condition)
    return "数据删除成功"

def search_data(embeddings, filename, top_k):
    result = db_singleton.search_emb_by(embeddings, filename, top_k)
    return result

def delete_table():
    db_singleton.delete_table(TABLE_NAME)
    return "表已删除"

def delete_work_place():
    db_singleton.delete_work_place()
    return "工作目录已删除"

def list_all():
    table = db_singleton.get_table()
    if table:
        try:
            res, _ = table.output(["*"]).to_df()
            result_df = pd.DataFrame(res)
            return result_df
        except Exception as e:
            print(f"列出数据失败: {e}")
    else:
        print("表对象不存在，无法列出数据")

with gr.Blocks() as demo:
    gr.Markdown("### Infinity 数据库操作界面")
    with gr.Tab("插入数据"):
        file_uuid = gr.Textbox(label="File UUID")
        filename = gr.Textbox(label="文件名")
        chunk_text = gr.Textbox(label="文本块")
        vector = gr.Textbox(label="向量", placeholder="输入 768 维向量，用逗号分隔")
        insert_button = gr.Button("插入数据")
        insert_output = gr.Textbox(label="插入结果")
        insert_button.click(insert_data, inputs=[file_uuid, filename, chunk_text, vector], outputs=insert_output)

    with gr.Tab("删除数据"):
        condition = gr.Textbox(label="删除条件")
        delete_button = gr.Button("删除数据")
        delete_output = gr.Textbox(label="删除结果")
        delete_button.click(delete_data, inputs=condition, outputs=delete_output)

    with gr.Tab("搜索数据"):
        embeddings = gr.Textbox(label="搜索向量", placeholder="输入 768 维向量，用逗号分隔")
        filename = gr.Textbox(label="文件名")
        top_k = gr.Number(label="返回结果数量", value=3)
        search_button = gr.Button("搜索数据")
        search_output = gr.Dataframe(label="搜索结果")
        search_button.click(search_data, inputs=[embeddings, filename, top_k], outputs=search_output)

    with gr.Tab("删除表"):
        delete_table_button = gr.Button("删除表")
        delete_table_output = gr.Textbox(label="删除表结果")
        delete_table_button.click(delete_table, outputs=delete_table_output)

    with gr.Tab("删除工作目录"):
        delete_work_place_button = gr.Button("删除工作目录")
        delete_work_place_output = gr.Textbox(label="删除工作目录结果")
        delete_work_place_button.click(delete_work_place, outputs=delete_work_place_output)

    with gr.Tab("列出所有数据"):
        list_button = gr.Button("列出数据")
        list_output = gr.Dataframe(label="列出结果")
        list_button.click(list_all, outputs=list_output)

demo.launch()
