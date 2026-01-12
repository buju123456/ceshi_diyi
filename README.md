# 简单图书管理系统 (Flask + SQLite)

这是一个非常基础的图书管理示例，提供 RESTful API 与简单前端页面。

## 依赖
建议使用虚拟环境：

```bash
python -m venv venv
source venv/bin/activate   # macOS / Linux
venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

## 运行
```bash
export FLASK_APP=app.py
export FLASK_ENV=development   # 可选，用于自动重载
flask run
```
或者直接：
```bash
python app.py
```

打开浏览器访问 http://127.0.0.1:5000

## API 示例
- 列表: GET /api/books
- 搜索: GET /api/books?search=关键字
- 获取单本: GET /api/books/<id>
- 添加: POST /api/books
  - JSON body: {"title": "...", "author":"...", "year":2020, "isbn":"...", "available": true}
- 更新: PUT /api/books/<id> (同上字段，字段缺省保持不变)
- 删除: DELETE /api/books/<id>

示例 curl:
```bash
# 添加
curl -X POST -H "Content-Type: application/json" -d '{"title":"Python 入门","author":"张三","year":2021}' http://127.0.0.1:5000/api/books

# 列表
curl http://127.0.0.1:5000/api/books

# 更新
curl -X PUT -H "Content-Type: application/json" -d '{"available":false}' http://127.0.0.1:5000/api/books/1

# 删除
curl -X DELETE http://127.0.0.1:5000/api/books/1
```
