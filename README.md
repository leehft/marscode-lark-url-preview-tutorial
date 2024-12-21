# MarsCode Lark URL Preview Tutorial

这里是 [用豆包 MarsCode 让飞书个性签名“动”起来](https://www.feishu.cn/community/article/event?id=%25E7%2594%25A8%25E8%25B1%2586%25E5%258C%2585%2520Marscode%2520%25EF%25BC%258C%25E8%25AE%25A9%25E9%25A3%259E%25E4%25B9%25A6%25E4%25B8%25AA%25E6%2580%25A7%25E7%25AD%25BE%25E5%2590%258D%25E2%2580%259C%25E5%258A%25A8%25E2%2580%259D%25E8%25B5%25B7%25E6%259D%25A5) 配套教学代码


## 步骤代码

代码仓库已经按照步骤打上了标签，可以通过以下命令查看所有标签

```
git tag
```

如果想切换到某个标签，执行以下命令

```
git checkout <tag_name>
```

例如切换到教学第一节的代码

```
git checkout 1a
```

## 安装依赖

```shell
pip install -r requirements.txt
```

## 运行服务

```shell   
python -m flask --app api.index run --debug
```

回调服务会运行在 `/api/handler`，将飞书的回调地址指向此路由即可