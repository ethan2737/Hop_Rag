"""
Hop-RAG API Server
为 Vue 前端提供 REST API
"""
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import uvicorn
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag import (
    get_knowledge_bases,
    create_knowledge_base,
    delete_knowledge_base,
    get_kb_files,
    process_and_index_files,
    simple_generate_answer,
    multi_hop_generate_answer,
    ask_question_parallel,
    Config
)

app = FastAPI(title="Hop-RAG API", version="1.0.0")

# CORS 配置 - 允许所有 localhost 端口用于开发
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8080",
        "http://localhost:8081",
        "http://localhost:8082",
        "http://localhost:8083",
        "http://127.0.0.1:8080",
        "http://127.0.0.1:8081",
        "http://127.0.0.1:8082",
        "http://127.0.0.1:8083",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== 知识库管理 API ====================

@app.get("/api/knowledge-bases")
def api_get_knowledge_bases():
    """获取知识库列表"""
    return get_knowledge_bases()

@app.post("/api/knowledge-base")
def api_create_knowledge_base(name: str = Form(...)):
    """创建知识库"""
    return create_knowledge_base(name)

@app.delete("/api/knowledge-base/{name}")
def api_delete_knowledge_base(name: str):
    """删除知识库"""
    return delete_knowledge_base(name)

@app.get("/api/knowledge-base/{name}/files")
def api_get_kb_files(name: str):
    """获取知识库文件列表"""
    return get_kb_files(name)

# ==================== 文件上传 API ====================

@app.post("/api/upload")
async def api_upload(files: List[UploadFile] = File(...), kb_name: str = Form(...)):
    """上传文件到知识库"""
    temp_files = []
    try:
        # 保存上传的文件到临时目录
        temp_dir = os.path.join(os.path.dirname(__file__), "temp_uploads")
        os.makedirs(temp_dir, exist_ok=True)

        for file in files:
            file_path = os.path.join(temp_dir, file.filename)
            content = await file.read()
            with open(file_path, "wb") as f:
                f.write(content)
            temp_files.append(file_path)

        # 处理文件
        result = process_and_index_files(temp_files, kb_name)

        # 清理临时文件
        for f in temp_files:
            os.remove(f)
        os.rmdir(temp_dir)

        return result
    except Exception as e:
        # 清理
        for f in temp_files:
            if os.path.exists(f):
                os.remove(f)
        raise HTTPException(status_code=500, detail=str(e))

# ==================== 问答 API ====================

from fastapi import Request

@app.post("/api/chat")
async def api_chat(request: Request):
    """问答接口"""
    try:
        data = await request.json()
        answer = ask_question_parallel(
            question=data.get("question", ""),
            kb_name=data.get("kb_name", "default"),
            use_search=data.get("use_search", True),
            use_table_format=data.get("use_table_format", False),
            multi_hop=data.get("multi_hop", False)
        )
        return answer
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
