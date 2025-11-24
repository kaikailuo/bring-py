### 答案示例

```python
a = int(input())
b = int(input())
r = (a - b) / 10
r = round(r, 1)
if r >= 3:
    status = "良好"
else:
    status = "不佳"
print(r, status)
```
