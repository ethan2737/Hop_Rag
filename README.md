# 医疗知识问答系统 (Hop-RAG)

一个基于检索增强生成 (RAG) 技术的智能医疗知识问答系统，支持多知识库管理、多轮对话、普通语义检索和高级多跳推理功能。

## 功能特性

- **多知识库管理**：支持创建、删除和管理多个独立的知识库
- **文件处理**：支持上传 TXT 和 PDF 格式文件，自动进行语义分块和向量化
- **两种检索模式**：
  - 简单向量检索：基于 FAISS 的语义相似度搜索
  - 多跳推理检索：迭代式检索和推理，自动发现信息缺口并进行后续查询
- **联网搜索**：可选的 Bing 搜索引擎集成，补充网络背景信息
- **对话历史**：支持多轮对话，理解上下文语境
- **表格输出**：可选的 Markdown 表格格式输出，结构化呈现医疗信息

## 系统架构

```
┌─────────────────────────────────────────────────────────────────┐
│                        Gradio Web UI                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │ 知识库管理  │  │  对话界面   │  │  配置选项               │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐    ┌────────────────┐    ┌───────────────┐
│  知识库模块   │    │   RAG 引擎     │    │  联网搜索模块 │
│  - 文件上传   │    │  - 简单检索    │    │  - Bing 搜索  │
│  - 语义分块   │    │  - 多跳推理    │    │  - 结果融合   │
│  - 向量化     │    │  - 答案生成    │    │               │
│  - FAISS 索引 │    │                │    │               │
└───────────────┘    └────────────────┘    └───────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │   LLM API       │
                    │  (Qwen-Plus)    │
                    └─────────────────┘
```

## 项目结构

```
Hop-Rag/
├── config.py           # 配置文件（API 密钥、模型参数、路径等）
├── rag.py              # 核心 RAG 系统实现
│   ├── TextVector      # 文本向量化类
│   ├── ReasoningRAG    # 多跳推理 RAG 类
│   ├── 知识库管理函数
│   ├── 文件处理函数
│   └── Gradio UI 定义
├── retrievor.py        # 信息检索与排序模块
│   ├── TextRecallRank  # 文本召回排序类
│   └── search_bing()   # Bing 搜索接口
├── text2vec.py         # 文本向量化工具
└── requirements.txt    # Python 依赖
```

## 依赖安装

### 环境要求

- Python 3.10+
- CUDA 兼容的 GPU（可选，用于本地模型）

### 安装步骤

```bash
# 克隆或进入项目目录
cd Hop-Rag

# 安装依赖
pip install -r requirements.txt
```

### 主要依赖

| 包名 | 用途 |
|------|------|
| torch | 深度学习框架 |
| faiss-cpu | 向量相似度搜索 |
| openai | API 客户端（兼容 OpenAI 格式） |
| llama-index | 文档分块处理 |
| PyMuPDF | PDF 文件解析 |
| gradio | Web 界面 |
| jieba | 中文分词 |
| chardet | 编码检测 |

## 配置说明

编辑 `config.py` 文件进行配置：

```python
class Config():
    # 检索器参数
    topd = 3              # 召回文章数量
    topt = 6              # 召回文本片段数量
    maxlen = 128          # 召回文本片段长度
    topk = 5              # 关键词召回数量
    recall_way = 'embed'  # 召回方式：'keyword' 或 'embed'

    # Embedding API 参数
    use_api = True
    api_key = "your-api-key"
    base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    model_name = "text-embedding-v3"
    dimensions = 1024

    # LLM API 参数
    llm_api_key = "your-api-key"
    llm_model = "qwen-plus"

    # 知识库配置
    kb_base_dir = "knowledge_bases"
    default_kb = "default"
    output_dir = "output_files"
```

## 使用指南

### 启动应用

```bash
python rag.py
```

启动后，访问终端显示的 URL（通常是 `http://localhost:7860`）打开 Web 界面。

### 知识库管理

1. **创建知识库**：
   - 切换到"知识库管理"标签页
   - 输入知识库名称
   - 点击"创建知识库"

2. **上传文件**：
   - 选择目标知识库
   - 上传 TXT 或 PDF 文件
   - 系统自动进行：
     - 文本提取
     - 语义分块（800 字符块大小，20 字符重叠）
     - 向量化处理
     - FAISS 索引构建

3. **管理知识库**：
   - 刷新列表查看已有知识库
   - 删除不需要的知识库（默认知识库不可删除）

### 问答对话

1. **选择知识库**：从下拉菜单选择要查询的知识库

2. **输入问题**：在问题输入框中输入您的医疗问题

3. **配置选项**：
   - 🔍 **联网搜索**：启用后会同时搜索网络信息
   - 🔄 **多跳推理**：启用多跳推理模式，进行深度检索

4. **表格输出**：勾选后以 Markdown 表格格式呈现结构化信息

5. **查看结果**：
   - 实时显示检索/推理过程
   - 查看推理步骤和检索到的内容块
   - 获取最终答案

## 核心算法

### 语义分块

使用改进的 `SentenceSplitter`，支持中文标点分隔：

```python
def semantic_chunk(text, chunk_size=800, chunk_overlap=20):
    # 自定义分隔符：。；!?
    # 段落合并策略
    # 生成带 ID 的分块数据
```

### 多跳推理流程

```
1. 初始检索 → 获取 top-k 相关块
2. 推理分析 → 识别信息缺口
3. 生成后续查询 → 填补缺口
4. 重复检索 → 最多 3 跳
5. 答案合成 → 整合所有信息
```

### 向量化处理

- 使用阿里云通义千问 Embedding API
- 批处理优化（batch_size=10）
- 自动重试机制
- 文本长度控制（≤8000 字符）

## API 说明

### 主要函数

| 函数名 | 描述 |
|--------|------|
| `process_and_index_files(file_objs, kb_name)` | 处理并索引文件到知识库 |
| `simple_generate_answer(question, kb_name)` | 简单向量检索生成答案 |
| `multi_hop_generate_answer(question, kb_name)` | 多跳推理生成答案 |
| `ask_question_parallel(question, kb_name, use_search, use_table_format, multi_hop)` | 并行搜索 + 本地检索 |
| `process_question_with_reasoning(question, kb_name, ...)` | 流式响应版本 |

### ReasoningRAG 类

```python
rag = ReasoningRAG(
    index_path="path/to/index",
    metadata_path="path/to/metadata",
    max_hops=3,              # 最大推理跳数
    initial_candidates=5,    # 初始候选数
    refined_candidates=3,    # 精炼候选数
    verbose=True
)

# 流式调用
for result in rag.stream_retrieve_and_answer(query):
    print(result["status"], result["answer"])

# 普通调用
answer, debug_info = rag.retrieve_and_answer(query)
```

## 知识库文件结构

```
knowledge_bases/
├── default/
│   ├── *.pdf                 # 原始 PDF 文件
│   ├── *.txt                 # 原始 TXT 文件
│   ├── semantic_chunk.index  # FAISS 索引
│   └── semantic_chunk_metadata.json  # 分块元数据
├── 知识库 1/
│   └── ...
└── 知识库 2/
    └── ...
```

## 输出目录

```
output_files/
├── semantic_chunk_output.json  # 语义分块结果（临时）
├── semantic_chunk_vector.json  # 向量化结果（临时）
└── knowledge_base.txt          # 知识库文本
```

## 注意事项

1. **API 密钥**：需要配置有效的阿里云 API 密钥
2. **网络要求**：需要访问阿里云 API 和 Bing 搜索
3. **内存使用**：大文件处理可能需要较多内存
4. **索引重建**：上传新文件会重建整个知识库索引

## 示例问题

- "多囊卵巢综合征的诊断标准是什么？"
- "原发性肝癌的治疗方法有哪些？"
- "新冠感染的用药指南"
- "幽门螺杆菌感染的预防措施"

## 技术亮点

1. **创新的多跳推理机制**：自动分析信息缺口，生成后续查询
2. **流式响应**：实时显示检索和推理过程
3. **多知识库隔离**：支持不同领域的知识管理
4. **混合检索**：本地知识库 + 网络搜索
5. **智能分块**：中文优化的语义分块策略

## License

MIT License
