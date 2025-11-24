## 答案示例

```python
s = 0
n = int(input())
for i in range(1, n+1):
    a = int(input())
    s += a

if s % 40 == 0:
    b = s // 40
else:
    b = s // 40 + 1

print(s)
print(b)
````
