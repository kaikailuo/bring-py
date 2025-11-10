## 答案示例

```python
s = 0
m = 0
n = int(input("请输入今年销售的文创产品的种类数量："))
for i in range(1, n+1):
    a = int(input("第" + str(i) + "号产品的销售件数是："))
    if a > m:
        m = a
    if a > 125:
        s += 1
print("今年销量最大的文创产品销量是：", m, "件")
print("可以保留生产的文创产品种类有：", s, "种")
```