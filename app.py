"""
Hop-RAG 统一启动脚本
通过 uv run app.py 启动前后端服务
"""
import subprocess
import sys
import os
import signal
import atexit

# 项目根目录
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend")

# 存储进程引用
processes = []


def cleanup():
    """清理子进程"""
    print("\n正在关闭服务...")
    for proc in processes:
        if proc.poll() is None:
            proc.terminate()
    print("服务已关闭。")


def start_backend():
    """启动后端服务"""
    print("\n" + "=" * 60)
    print("启动后端服务 (FastAPI)...")
    print("访问地址：http://localhost:8002")
    print("API 文档：http://localhost:8002/docs")
    print("=" * 60)

    api_script = os.path.join(PROJECT_ROOT, "api.py")
    proc = subprocess.Popen([sys.executable, api_script], cwd=PROJECT_ROOT)
    processes.append(proc)

    # 等待后端启动
    import time
    time.sleep(2)


def start_frontend():
    """启动前端服务"""
    print("\n" + "=" * 60)
    print("启动前端服务 (Vite + Vue)...")
    print("访问地址：http://localhost:8080")
    print("=" * 60)

    # 检查 node_modules
    node_modules = os.path.join(FRONTEND_DIR, "node_modules")
    if not os.path.exists(node_modules):
        print("\n正在安装前端依赖...")
        subprocess.run(["npm", "install"], cwd=FRONTEND_DIR, check=True)

    proc = subprocess.Popen(["npm", "run", "dev"], cwd=FRONTEND_DIR)
    processes.append(proc)

    # 等待进程结束
    try:
        proc.wait()
    except KeyboardInterrupt:
        pass


def main():
    """主函数：同时启动前后端"""
    print("\n\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 12 + "Hop-RAG 中医知识问答系统" + " " * 18 + "║")
    print("╚" + "=" * 58 + "╝")

    # 注册清理函数
    atexit.register(cleanup)

    # 设置信号处理
    def signal_handler(sig, frame):
        cleanup()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    print()

    # 启动后端
    start_backend()

    # 启动前端（主线程）
    start_frontend()


if __name__ == "__main__":
    main()
