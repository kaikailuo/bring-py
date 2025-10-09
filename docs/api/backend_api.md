````markdown
# 后端 API 文档

## 基础信息

- **基础URL**: `http://localhost:8000/api`
- **认证方式**: JWT Bearer Token
- **响应格式**: JSON
- **字符编码**: UTF-8

## 通用响应格式

```json
{
    "code": 200,
    "message": "success",
    "data": {}
}
````

### 响应状态码

| 状态码 | 说明       |
| --- | -------- |
| 200 | 请求成功     |
| 400 | 请求参数错误   |
| 401 | 未授权/认证失败 |
| 403 | 权限不足     |
| 404 | 资源不存在    |
| 422 | 数据验证失败   |
| 500 | 服务器内部错误  |

---

## 认证接口

### 1. 用户注册

**接口**: `POST /auth/register`
**描述**: 注册新用户账户

**请求参数**:

| 参数名      | 类型     | 必填 | 说明                   |
| -------- | ------ | -- | -------------------- |
| username | string | 是  | 用户名，3-20字符           |
| password | string | 是  | 密码，6-20字符            |
| role     | string | 是  | 用户角色：student/teacher |
| name     | string | 是  | 真实姓名，2-10字符          |
| email    | string | 是  | 邮箱地址                 |

**请求示例**:

```json
{
    "username": "student001",
    "password": "password123",
    "role": "student",
    "name": "张三",
    "email": "zhangsan@example.com"
}
```

**响应示例**:

```json
{
    "code": 200,
    "message": "注册成功",
    "data": {
        "user": {
            "id": 1,
            "username": "student001",
            "role": "student",
            "name": "张三",
            "email": "zhangsan@example.com",
            "is_active": true,
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": null
        }
    }
}
```

---

### 2. 用户登录

**接口**: `POST /auth/login`
**描述**: 用户登录获取访问令牌

**请求参数**:

| 参数名      | 类型     | 必填 | 说明  |
| -------- | ------ | -- | --- |
| username | string | 是  | 用户名 |
| password | string | 是  | 密码  |

**请求示例**:

```json
{
    "username": "student001",
    "password": "password123"
}
```

**响应示例**:

```json
{
    "code": 200,
    "message": "登录成功",
    "data": {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "user": {
            "id": 1,
            "username": "student001",
            "role": "student",
            "name": "张三",
            "email": "zhangsan@example.com",
            "is_active": true,
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": null
        }
    }
}
```

---

### 3. 用户登出

**接口**: `POST /auth/logout`
**描述**: 用户登出（客户端需删除本地令牌）

**请求头**:

| 参数名           | 类型     | 必填 | 说明             |
| ------------- | ------ | -- | -------------- |
| Authorization | string | 是  | Bearer <token> |

**响应示例**:

```json
{
    "code": 200,
    "message": "登出成功",
    "data": {
        "user_id": 1,
        "username": "student001"
    }
}
```

---

### 4. 获取当前用户信息

**接口**: `GET /auth/me`
**描述**: 获取当前登录用户的详细信息

**请求头**:

| 参数名           | 类型     | 必填 | 说明             |
| ------------- | ------ | -- | -------------- |
| Authorization | string | 是  | Bearer <token> |

**响应示例**:

```json
{
    "code": 200,
    "message": "获取用户信息成功",
    "data": {
        "user": {
            "id": 1,
            "username": "student001",
            "role": "student",
            "name": "张三",
            "email": "zhangsan@example.com",
            "is_active": true,
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": null
        }
    }
}
```

---

### 5. 更新用户信息

**接口**: `PUT /auth/me`
**描述**: 更新当前用户的基本信息

**请求头**:

| 参数名           | 类型     | 必填 | 说明             |
| ------------- | ------ | -- | -------------- |
| Authorization | string | 是  | Bearer <token> |

**请求参数**:

| 参数名   | 类型     | 必填 | 说明   |
| ----- | ------ | -- | ---- |
| name  | string | 否  | 真实姓名 |
| email | string | 否  | 邮箱地址 |

**请求示例**:

```json
{
    "name": "张三丰",
    "email": "zhangsanfeng@example.com"
}
```

**响应示例**:

```json
{
    "code": 200,
    "message": "更新用户信息成功",
    "data": {
        "user": {
            "id": 1,
            "username": "student001",
            "role": "student",
            "name": "张三丰",
            "email": "zhangsanfeng@example.com",
            "is_active": true,
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T01:00:00Z"
        }
    }
}
```

---

### 6. 修改密码

**接口**: `POST /auth/change-password`
**描述**: 修改当前用户的密码

**请求头**:

| 参数名           | 类型     | 必填 | 说明             |
| ------------- | ------ | -- | -------------- |
| Authorization | string | 是  | Bearer <token> |

**请求参数**:

| 参数名          | 类型     | 必填 | 说明         |
| ------------ | ------ | -- | ---------- |
| old_password | string | 是  | 原密码        |
| new_password | string | 是  | 新密码，6-20字符 |

**请求示例**:

```json
{
    "old_password": "password123",
    "new_password": "newpassword456"
}
```

**响应示例**:

```json
{
    "code": 200,
    "message": "密码修改成功",
    "data": null
}
```

---

## 管理员接口

### 1. 获取用户列表

**接口**: `GET /auth/users`
**描述**: 获取系统中的用户列表（仅管理员可用）

**请求头**:

| 参数名           | 类型     | 必填 | 说明                   |
| ------------- | ------ | -- | -------------------- |
| Authorization | string | 是  | Bearer <admin_token> |

**查询参数**:

| 参数名   | 类型      | 必填 | 说明                          |
| ----- | ------- | -- | --------------------------- |
| skip  | integer | 否  | 跳过的记录数，默认0                  |
| limit | integer | 否  | 限制返回的记录数，默认100              |
| role  | string  | 否  | 按角色筛选：student/teacher/admin |

**请求示例**:

```
GET /auth/users?skip=0&limit=10&role=student
```

**响应示例**:

```json
{
    "code": 200,
    "message": "获取用户列表成功",
    "data": {
        "users": [
            {
                "id": 1,
                "username": "student001",
                "role": "student",
                "name": "张三",
                "email": "zhangsan@example.com",
                "is_active": true,
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": null
            }
        ],
        "total": 1
    }
}
```

---

### 2. 激活用户

**接口**: `PUT /auth/users/{user_id}/activate`
**描述**: 激活指定用户账户（仅管理员可用）

**请求头**:

| 参数名           | 类型     | 必填 | 说明                   |
| ------------- | ------ | -- | -------------------- |
| Authorization | string | 是  | Bearer <admin_token> |

**路径参数**:

| 参数名     | 类型      | 必填 | 说明   |
| ------- | ------- | -- | ---- |
| user_id | integer | 是  | 用户ID |

**响应示例**:

```json
{
    "code": 200,
    "message": "用户激活成功",
    "data": null
}
```

---

### 3. 停用用户

**接口**: `PUT /auth/users/{user_id}/deactivate`
**描述**: 停用指定用户账户（仅管理员可用）

**请求头**:

| 参数名           | 类型     | 必填 | 说明                   |
| ------------- | ------ | -- | -------------------- |
| Authorization | string | 是  | Bearer <admin_token> |

**路径参数**:

| 参数名     | 类型      | 必填 | 说明   |
| ------- | ------- | -- | ---- |
| user_id | integer | 是  | 用户ID |

**响应示例**:

```json
{
    "code": 200,
    "message": "用户停用成功",
    "data": null
}
```

---

## 错误响应示例

### 认证失败

```json
{
    "code": 401,
    "message": "用户名或密码错误",
    "data": null
}
```

### 权限不足

```json
{
    "code": 403,
    "message": "权限不足",
    "data": null
}
```

### 数据验证失败

```json
{
    "code": 422,
    "message": "数据验证失败",
    "data": {
        "detail": [
            {
                "loc": ["body", "username"],
                "msg": "用户名长度应为3-20个字符",
                "type": "value_error"
            }
        ]
    }
}
```

### 资源不存在

```json
{
    "code": 404,
    "message": "用户不存在",
    "data": null
}
```

---

## 使用示例

### JavaScript (fetch)

```javascript
// 用户登录
const login = async (username, password) => {
    const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });
    
    const data = await response.json();
    if (data.code === 200) {
        localStorage.setItem('token', data.data.token);
        return data.data.user;
    }
    throw new Error(data.message);
};

// 获取用户信息
const getUserInfo = async () => {
    const token = localStorage.getItem('token');
    const response = await fetch('/api/auth/me', {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    
    const data = await response.json();
    return data.data.user;
};
```

### Python (requests)

```python
import requests

# 用户登录
def login(username, password):
    response = requests.post('/api/auth/login', json={'username': username, 'password': password})
    data = response.json()
    if data['code'] == 200:
        return data['data']['token']
    raise Exception(data['message'])

# 获取用户信息
def get_user_info(token):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get('/api/auth/me', headers=headers)
    data = response.json()
    return data['data']['user']
```

---

## 注意事项

1. JWT令牌有效期为30分钟，过期后需要重新登录。
2. 所有需要认证的接口都需要在请求头中携带有效的JWT令牌。
3. 管理员接口需要管理员权限，普通用户无法访问。
4. 密码在传输和存储时都会进行加密处理。
5. 建议在生产环境中使用HTTPS协议。
6. 请妥善保管JWT令牌，避免泄露。

```

---
