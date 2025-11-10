## 答案示例

```python
import turtle
# 圆形
turtle.color('red')
turtle.fillcolor('red')
turtle.begin_fill()
turtle.circle(100)
turtle.end_fill()

# 抬笔定位
turtle.penup()
turtle.goto(-70,120)
turtle.pendown()

# 矩形
turtle.color('white')
turtle.fillcolor('white')
turtle.begin_fill()
turtle.goto(70,120)
turtle.goto(70,150)
turtle.goto(-70,150)
turtle.goto(-70,120)
turtle.end_fill()
```