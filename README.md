## 高顿资源采集器

### 创建虚拟环境

```
python3 -m venv venv
```

### 激活虚拟环境

```
source venv/bin/activate
```

### 安装环境依赖
pip freeze > requirements.txt

```
pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host  mirrors.aliyun.com
```

### 运行

```
python start_xxxx.py
```

### 退出虚拟环境

```
deactivate 
```