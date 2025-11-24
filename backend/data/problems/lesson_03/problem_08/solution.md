## 答案示例

```python
n = int(input())
s = 0
for i in range(n):
    a = int(input())
    if a == 3:
        s += 1
print(round(s/n*100, 1))
```
