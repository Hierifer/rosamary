#!/bin/bash
# 检查虚拟环境是否存在
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装或更新依赖
if [ -f "requirements.txt" ]; then
    echo "安装依赖..."
    pip install -r requirements.txt
elif [ -f "pyproject.toml" ]; then
    echo "安装项目..."
    pip install -e .
fi

# 提示信息
echo "环境已激活，可以运行项目:"
echo "python index.py"