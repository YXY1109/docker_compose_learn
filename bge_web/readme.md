# DockerCompose学习记录

```
安装torch
pip install torch==2.6.0 torchvision==0.21.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cu126
```

## 一，生成requirements.txt

requirements_manual.txt
是我手动添加的

**方式一**

#### 有个问题就是会把所有包都生成，有些包是依赖的，不同系统版本可能不同

> pip freeze > requirements_pip.txt
>
> 生成：requirements_pip.txt

**方式二**
使用[pipreqs](https://github.com/bndr/pipreqs)
> pip install pipreqs
>
> pipreqs .\web\
>
> 生成：requirements.txt

## 二，postman调用

### 1，向量

```
curl --location 'http://127.0.0.1:8010/bge_m3' \
--header 'Content-Type: application/json' \
--data '{
    "sentences": [
        "你好1",
        "你好2"
    ],
    "dense":true,
    "sparse":true,
    "colbert_vecs":true
}'
```

### 2，重排

```
curl --location 'http://127.0.0.1:8010/bge_ranker_v2_m3' \
--header 'Content-Type: application/json' \
--data '{
    "problem_list": [
        [
            "我是中国人",
            "你好"
        ],
        [
            "我是中国人",
            "在一起"
        ],
        [
            "我是中国人",
            "中国人很强大"
        ],
        [
            "我是中国人",
            "生为中国人很自豪"
        ],
        [
            "我是中国人",
            "我是中国人，我出生在中国"
        ]
    ]
}'
```

