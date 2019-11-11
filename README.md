# BiKi Open API

简体中文 | [English](./README.us-en.md)

- [**入门指引**](#入门指引)

  - [**创建API Key**](#创建api-key)
  - [**接口调用方式说明**](#接口调用方式说明)
  - [**服务器**](#服务器)
  - [**联系我们**](#联系我们)

- [**REST API**](#rest-api)

  - [**接入 URL**](#接入-url)
  - [**请求交互**](#请求交互)
  - [**签名认证**](#签名认证)
  - [**REST API列表**](#rest-api列表)
  - [**查询系统支持的所有交易对及精度**](#查询系统支持的所有交易对及精度)
  - [**获取所有交易对行情**](#获取所有交易对行情)
  - [**获取各个币对最新成交价**](#获取各个币对最新成交价)
  - [**获取指定币对当前行情**](#获取指定币对当前行情)
  - [**获取K线数据**](#获取k线数据)
  - [**获取买卖盘深度**](#获取买卖盘深度)
  - [**获取资产余额**](#获取资产余额)
  - [**获取当前委托**](#获取当前委托)
  - [**获取全部委托**](#获取全部委托)
  - [**获取全部成交记录**](#获取全部成交记录)
  - [**获取订单详情**](#获取订单详情)
  - [**创建订单**](#创建订单)
  - [**取消委托单**](#取消委托单)
  - [**取消指定币对全部委托单**](#取消指定币对全部委托单)
  - [**批量下单撤单**](#批量下单撤单)

- [**Websocket API**](#websocket-api)

  - [**接入 URL**](#host-url)
  - [**请求交互**](#请求交互)
  - [**订阅实时成交信息**](#订阅实时成交信息)
  - [**订阅深度盘口**](#订阅深度盘口)
  - [**订阅K线数据**](#订阅k线数据)

## 入门指引

**欢迎使用开发者文档，BiKi提供了简单易用的API接口，通过API可以获取市场行情数据、进行交易、管理订单**

### 创建API Key

用户在 **[BiKi](https://www.biki.com)** 注册账号后，需要在 **[[用户中心](https://www.biki.com/personal/userManagement)] - [[API管理](https://www.biki.com/personal/apiManagement)]** 中创建API Key秘钥，创建完成后得到一组随机生成的API Key与Secret Key,利用这一组数据可以进行程序化交易，单个账号最多创建5个密钥

> **请不要泄露API Key 与 Secret Key信息，以免造成资产损失,建议用户为API绑定IP地址，每个密钥最多绑定5个IP，使用英文逗号进行分隔**

### 接口调用方式说明

**BiKi提供两种调用接口方式，用户可根据使用场景和偏好选择适合自己的方式来调用。 [可参考SDK(点击跳转SDK页面)](/sdk/)**

- REST API

  提供行情查询、余额查询、币币交易、订单管理功能，建议用户使用REST API进行账户余额查询、币币交易及订单管理等操作

- Websocket API

  提供市场行情、买卖深度、实时成交信息，建议用户使用Websocket API获取市场行情类信息

### 服务器

BiKi服务器运行在东京，为了最大限度地减少API访问延迟，建议使用与东京通讯通畅的服务器

<br>

## REST API

### 接入 URL

- **[https://openapi.biki.com](https://www.biki.com) [推荐]**

- **[https://openapi.bikicoin.pro](https://www.bikicoin.pro)**

### 请求交互

#### 介绍

REST API 提供行情查询、余额查询、币币交易、订单管理功能

所有请求基于Https协议，请求头信息中content-type需要统一设置为表单格式:

- **content-type:application/x-www-form-urlencoded**

#### 状态码

状态码    | 说明               | 备注
------ | ---------------- | ---------------------
0      | 成功               | code=0 成功， code >0 失败
5      | 下单失败             | 请检查订单价格与数量精度是否符合
6      | 数量小于最小值          |
7      | 数量大于最大值          |
8      | 订单取消失败           |
9      | 交易被冻结            |
13     | 系统错误             |
19     | 可用余额不足           |
22     | 订单不存在            |
23     | 缺少交易数量参数         |
24     | 缺少交易价格参数         |
10034  | 可用余额不足           |
10062  | 价格或数量精度超过最大限制    |
10063  | 数量小于最小值          |
10064  | 价格或金额小于最小值       |
10067  | 价格超出当日涨跌停范围，无法下单 |
10068  | 订单委托量超出最大限制      |
10069  | 超出下单频率           |
10071  | 涨跌停限制币对,不允许下市价单  |
100001 | 系统异常             |
100002 | 系统升级             |
100004 | 请求参数不合法          |
100005 | 参数签名错误           |
100007 | 非法IP             | 服务器IP不在API绑定IP列表中
110004 | 提现被冻结            |
110025 | 账户被后台管理员锁定       |
110041 | 接口访问频率过高         |

### 签名认证

#### 签名说明

API 请求在通过网络传输的过程中极有可能被篡改，为了确保请求未被更改，除公共接口（基础信息，行情数据）外的私有接口均必须使用您的 API Key 做签名认证，以校验参数或参数值在传输途中是否发生了更改。

#### 签名步骤

**以获取资产余额为例**

- 接口

  - GET /open/api/user/account

- 示例API秘钥

  - api_key = 0816016bb06417f50327e2b557d39aaa

  - secret_key = ab5bba291b8e1cabd8009c2ce6aabdb3

**1\. 按照ASCII码的顺序对参数名进行排序**

- 原始参数顺序为:

  - time = 156200607

  - api_key = 0816016bb06417f50327e2b557d39aaa

- 按照ASCII码顺序对参数名进行排序：

  - api_key = 0816016bb06417f50327e2b557d39aaa

  - time = 156200607

**2\. 所有参数按"参数名参数值"格式拼接在一起组成要签名计算的字符串**

- api_key0816016bb06417f50327e2b557d39aaatime156200607

**3\. 签名计算的字符串与秘钥(Secret Key)拼接形成最终计算的字符串，使用32位MD5算法进行计算生成数字签名**

- MD5(api_key0816016bb06417f50327e2b557d39aaatime156200607ab5bba291b8e1cabd8009c2ce6aabdb3)

- 签名结果中字母全部小写:

  - sign = 5fcf02e226a4bb2fb180be2aaa6fe541

**4\. 将生成的数字签名加入到请求的路径参数里**

- 最终发送到服务器的请求地址为:

  - <https://openapi.biki.com/open/api/user/account?api_key=0816016bb06417f50327e2b557d39aaa&time=156200607&sign=5fcf02e226a4bb2fb180be2aaa6fe541>

### REST API列表

API                                              | 接口类型 | 签名 | 频率限制      | 说明
------------------------------------------------ | ---- | -- | --------- | ---------------
[GET /open/api/common/symbols](#查询系统支持的所有交易对及精度) | 公共接口 | X  | 10 次/秒    | 查询系统支持的所有交易对及精度
[GET /open/api/get_allticker](#获取所有交易对行情)        | 公共接口 | X  | 10 次/秒    | 获取所有交易对行情
[GET /open/api/market](#获取各个币对的最新成交价)            | 公共接口 | X  | 10 次/秒    | 获取各个币对的最新成交价
[GET /open/api/get_ticker](#获取指定币对当前行情)          | 公共接口 | X  | 10 次/秒    | 获取指定币对当前行情
[GET /open/api/get_trades](#获取行情成交记录)            | 公共接口 | X  | 10 次/秒    | 获取行情成交记录
[GET /open/api/get_records](#获取K线数据)             | 公共接口 | X  | 10 次/秒    | 获取K线数据
[GET /open/api/market_dept](#获取买卖盘深度)            | 公共接口 | X  | 10 次/秒    | 获取买卖盘深度
[GET /open/api/user/account](#获取资产余额)            | 私有接口 | V  | 10 次/秒    | 获取资产余额
[GET /open/api/v2/new_order](#获取当前委托)            | 私有接口 | V  | 10 次/秒    | 获取当前委托
[GET /open/api/v2/all_order](#获取全部委托)            | 私有接口 | V  | 10 次/秒    | 获取全部委托
[GET /open/api/all_trade](#获取全部成交记录)             | 私有接口 | V  | 10 次/秒    | 获取全部成交记录
[GET /open/api/order_info](#获取订单详情)              | 私有接口 | V  | 10 次/秒    | 获取订单详情
[POST /open/api/create_order](#创建订单)             | 私有接口 | V  | 100 次/10秒 | 创建订单
[POST /open/api/cancel_order](#取消委托单)            | 私有接口 | V  | 100 次/10秒 | 取消委托单
[POST /open/api/cancel_order_all](#取消指定币对全部委托单)  | 私有接口 | V  | 100 次/10秒 | 取消指定币对全部委托单
[POST /open/api/mass_replaceV2](#批量下单撤单)         | 私有接口 | V  | 100 次/10秒 | 批量下单撤单

### 查询系统支持的所有交易对及精度

#### GET [/open/api/common/symbols](https://openapi.biki.com/open/api/common/symbols)

#### 输入参数: 无

#### 返回参数:

参数名称             | 数据类型   | 描述
---------------- | ------ | ---------------------
code             | string | code=0 成功， code >0 失败
symbol           | string | 交易对
count_coin       | string | 计价币种
base_coin        | string | 基础币种
amount_precision | number | 数量精度位数(0为个位)
price_precision  | number | 价格精度位数(0为个位)

#### 返回示例:

```python
{
    "code": "0",
    "msg": "suc",
    "data": [
        {
            "symbol": "bikiusdt",
            "count_coin": "USDT",
            "amount_precision": 4,
            "base_coin": "BIKI",
            "price_precision": 6
        },
        {
            "symbol": "vdsusdt",
            "count_coin": "USDT",
            "amount_precision": 2,
            "base_coin": "BTC",
            "price_precision": 4
        },
        ...
    ]
}
```

### 获取所有交易对行情

#### GET [/open/api/get_allticker](https://openapi.biki.com/open/api/get_allticker)

#### 输入参数: 无

#### 返回参数:

参数名称   | 数据类型   | 描述
------ | ------ | ---------------------
code   | string | code=0 成功， code >0 失败
symbol | string | 交易对
vol    | string | 最近24H 交易量
high   | string | 最近24H 最高价
last   | number | 最新价
low    | string | 最近24H 最低价
buy    | number | 当前买一价
sell   | number | 当前卖一价
change | string | 最近24H 价格变化
rose   | string | 最近24H 涨跌幅度

#### 返回示例:

```python
{
    "code": "0",
    "msg": "suc",
    "data": {
        "ticker": [
            {
                "symbol": "bikiusdt",
                "high": "0.1235",
                "vol": "31753853.80270792",
                "last": 0.114906,
                "low": "0.1111",
                "buy": 0.114887,
                "sell": 0.114967,
                "change": "0.0085224",
                "rose": "0.0085224"
            },
            {
                "symbol": "vdsusdt",
                "high": "3.39",
                "vol": "532061.01067007",
                "last": 3.1459,
                "low": "3.1",
                "buy": 3.14,
                "sell": 3.1541,
                "change": "-0.00427296",
                "rose": "-0.00427296"
            },
            {
                "symbol": "btcusdt",
                "high": "10716.3335",
                "vol": "20433.12745191",
                "last": 10521.9785,
                "low": "9864.9351",
                "buy": 10515.7454,
                "sell": 10527.1895,
                "change": "-0.00423288",
                "rose": "-0.00423288"
            },
            ...
        ],
        "date": 1563207200947
    }
}
```

### 获取各个币对最新成交价

#### GET [/open/api/market](https://openapi.biki.com/open/api/market)

#### 输入参数: 无

#### 返回参数:

参数名称 | 数据类型   | 描述
---- | ------ | ---------------------
code | string | code=0 成功， code >0 失败
data | object | 各币对最新成交价格

#### 返回示例:

```python
{
    "code": "0",
    "msg": "suc",
    "data": {
        "eosbtc": 0.00038891,
        "attusdt": 0.000041,
        "heyusdt": 0.021607,
        "ontbtc": 0.00008929,
    ...
    }
}
```

### 获取指定币对当前行情

#### GET [/open/api/get_ticker](https://openapi.biki.com/open/api/get_ticker?symbol=btcusdt)

#### 输入参数:

参数名称   | 是否必须 | 数据类型   | 描述  | 取值范围
------ | ---- | ------ | --- | -----------------------------
symbol | true | string | 交易对 | btcusdt, ltcusdt, ethusdt ...

#### 返回参数:

参数名称   | 数据类型   | 描述
------ | ------ | ---------------------
code   | string | code=0 成功， code >0 失败
symbol | string | 交易对
vol    | string | 当日 交易量
high   | string | 当日 最高价
last   | number | 最新价
low    | string | 当日 最低价
buy    | number | 当前买一价
sell   | number | 当前卖一价
change | string | 当日 价格变化
rose   | string | 当日 涨跌幅度

#### 返回示例:

```python
{
    "code": "0",
    "msg": "suc",
    "data": {
        "high": "10753.6563",
        "vol": "20193.35399854",
        "last": 10335.8936,
        "low": "9287.7207",
        "buy": 10328.6517,
        "sell": 10340.1291,
        "rose": "-0.00963801",
        "time": 1563530414000
    }
}
```

### 获取行情成交记录

#### GET [/open/api/get_trades](https://openapi.biki.com/open/api/get_trades?symbol=btcusdt)

#### 输入参数:

参数名称   | 是否必须 | 数据类型   | 描述  | 取值范围
------ | ---- | ------ | --- | -----------------------------
symbol | true | string | 交易对 | btcusdt, ltcusdt, ethusdt ...

#### 返回参数:

参数名称 | 数据类型   | 描述
---- | ------ | ---------------------
code | string | code=0 成功， code >0 失败
data | object | 交易记录

#### 返回示例:

```python
{
    "code": "0",
    "msg": "suc",
    "data": [
        {
            "amount": 0.55,               // 成交量
            "price": 0.18519949,          // 成交价
            "id": 447121,
            "type": "buy"                 // 买卖type，买为buy，买sell
            "ts":1553690617000            // 成交时间戳
            "ds":2019-3-27 20:43:37       // 成交时间格式化显示
        },
        ...
    ]
}
```

### 获取K线数据

#### GET [/open/api/get_records](https://openapi.biki.com/open/api/get_records?symbol=btcusdt&period=1)

#### 输入参数:

参数名称   | 是否必须 | 数据类型   | 描述                        | 取值范围
------ | ---- | ------ | ------------------------- | -----------------------------
symbol | true | string | 交易对                       | btcusdt, ltcusdt, ethusdt ...
period | true | number | K线周期 单位为分钟,1代表1分钟 1天为1440 | 1/5/15/30/60/1440/10080/43200

#### 返回参数:

参数名称 | 数据类型   | 描述
---- | ------ | ---------------------
code | string | code=0 成功， code >0 失败
data | object | K线数据

##### data说明:

```python
"data": [
  [
    1558586460,   // K线开盘时间戳
    7654.7866,    // 开盘价
    7654.7866,    // 最高
    7654.0322,    // 最低
    7654.0322,    // 收盘价
    26.9234       // 成交量
  ],
  ...
]
```

#### 返回示例:

```python
{
    "code": "0",
    "msg": "suc",
    "data": [
        [
            1558586460,
            7654.7866,
            7654.7866,
            7654.0322,
            7654.0322,
            26.9234
        ],
        [
            1558586520,
            7654.0322,
            7654.0322,
            7654.0322,
            7654.0322,
            0.0
        ],
        ...
    ]
}
```

### 获取买卖盘深度

#### GET [/open/api/market_dept](https://openapi.biki.com/open/api/market_dept?symbol=btcusdt&type=step0)

#### 输入参数:

参数名称   | 是否必须 | 数据类型   | 描述                      | 取值范围
------ | ---- | ------ | ----------------------- | -----------------------------
symbol | true | string | 交易对                     | btcusdt, ltcusdt, ethusdt ...
type   | true | string | 深度类型（合并深度0-2）step0时精度最高 | step0/step1/step2

#### 返回参数:

参数名称 | 数据类型   | 描述
---- | ------ | ---------------------
code | string | code=0 成功， code >0 失败
tick | object | 订单簿数据

##### tick说明:

```python
"tick": {
    "asks": [             // 卖单
        [
            10352.1109,
            0.1959
        ],
        [
            10352.1315,
            0.2393
        ],
        ...
    ],
    "bids": [             // 买单
        [
            10336.1313,
            0.8707
        ],
        [
            10334.3287,
            0.1721
        ],
        ...
    ],
    "time": null
}
```

#### 返回示例:

```python
{
    "code": "0",
    "msg": "suc",
    "data": {
        "tick": {
            "asks": [
                [
                    10352.1109,
                    0.1959
                ],
                [
                    10352.1315,
                    0.2393
                ],
                ...
            ],
            "bids": [
                [
                    10336.1313,
                    0.8707
                ],
                [
                    10334.3287,
                    0.1721
                ],
                ...
            ],
            "time": null
        }
    }
}
```

### 获取资产余额

#### GET [/open/api/user/account](https://openapi.biki.com/open/api/user/account?api_key=0816016bb06417f50327e2b557d39aaa&time=156200607&sign=3cdbe8034f7abf2820fc1bbe721e5692)

#### 签名请求示例

api_key0816016bb06417f50327e2b557d39aaatime156200607

#### 输入参数:

参数名称    | 是否必须 | 数据类型   | 描述         | 取值范围
------- | ---- | ------ | ---------- | ----
api_key | true | string | 用户 api_key |
time    | true | string | 时间戳        |
sign    | true | string | 签名         |

#### 返回参数:

参数名称        | 数据类型   | 描述
----------- | ------ | ---------------------
code        | string | code=0 成功， code >0 失败
total_asset | string | 总资产折合BTC价值
btcValuatin | string | 币种折合BTC价值
normal      | number | 币种可用余额
locked      | string | 币种冻结中余额
coin        | string | 持有币种

#### 返回示例:

```python
{
    "code": "0",
    "msg": "suc",
    "data": {
        "total_asset": "10.79548765",
        "coin_list": [
            {
                "normal": "27599.42",
                "btcValuatin": "2.73373997",
                "locked": "702.40",
                "coin": "usdt"
            },
            {
                "normal": "0.00000000",
                "btcValuatin": "0.00000000",
                "locked": "0.00000000",
                "coin": "eusdt"
            },
            ...
        ]
    }
}
```

### 获取当前委托

#### GET [/open/api/v2/new_order](https://openapi.biki.com/open/api/v2/new_order)

#### 签名请求示例

api_keyd7e4d03168ac95fca79ffd60a9dc3632symbolbtcusdttime1564132794

#### 输入参数:

参数名称     | 是否必须  | 数据类型   | 描述         | 取值范围
-------- | ----- | ------ | ---------- | ----
api_key  | true  | string | 用户 api_key |
pageSize | false | string | 每页数据数      |
page     | false | string | 页码         |
sign     | true  | string | 签名         |
symbol   | true  | string | 币对         |
time     | true  | string | 时间戳        |

#### 返回参数:

参数名称          | 数据类型   | 描述
------------- | ------ | ------------------------------------------------
code          | string | code=0 成功， code >0 失败
count         | number | 最大条数
side          | string | BUY/SELL
side_msg      | string | 买卖方向中文解释
status        | number | 订单状态 1 新订单, 2 完全成交, 3 部分成交, 4 已撤单, 5 待撤单, 6 异常订单
status_msg    | string | 订单状态中文解释
type          | number | 1 限价单, 2 市价单
baseCoin      | string | 基础币种
countCoin     | string | 计价币种
price         | string | 订单挂单价
volume        | string | 订单挂单量
avg_price     | string | 订单已成交均价
deal_volume   | string | 订单已成交量
remain_volume | string | 订单未成交量
deal_price    | string | 订单已成交金额
created_at    | string | 下单时间
tradeList     | object | 成交记录

#### 返回示例:

```python
{
    "code": "0",
    "msg": "suc",
    "data": {
        "count": 1000,
        "resultList": [
            {
                "side": "SELL",
                "total_price": "4.18993396",
                "fee": 0.0,
                "created_at": 1563541098939,
                "deal_price": 0.0,
                "avg_price": "0.00000000",
                "countCoin": "USDT",
                "source": 3,
                "type": 1,
                "side_msg": "卖出",
                "volume": "0.00040000",
                "price": "10474.83490000",
                "source_msg": "WEB",
                "status_msg": "未成交",
                "deal_volume": "0.00000000",
                "fee_coin": "USDT",
                "id": 90419538,
                "remain_volume": "0.00040000",
                "baseCoin": "BTC",
                "tradeList": [],
                "status": 1
            },
            ...
        ]
    }
}
```

### 获取全部委托

#### GET [/open/api/v2/all_order](https://openapi.biki.com/open/api/v2/all_order)

#### 签名请求示例

api_keyd7e4d03168ac95fca79ffd60a9dc3632symbolbtcusdttime1564132947

#### 输入参数:

参数名称      | 是否必须  | 数据类型   | 描述                             | 取值范围
--------- | ----- | ------ | ------------------------------ | ----------------------------
api_key   | true  | string | 用户 api_key                     |
startDate | false | string | 开始时间,精确到秒"yyyy-MM-dd mm:hh:ss" |
endDate   | false | string | 结束时间,精确到秒"yyyy-MM-dd mm:hh:ss" | 需与startDate相距10分钟以内，否则返回错误码1
pageSize  | false | string | 每页数据数                          |
page      | false | string | 页码                             |
sign      | true  | string | 签名                             |
symbol    | true  | string | 币对                             |
time      | true  | string | 时间戳                            |

> 没有开始时间，结束时间时，默认返回最近10分钟的全部委托单数据

#### 返回参数:

参数名称          | 数据类型   | 描述
------------- | ------ | ------------------------------------------------
code          | string | code=0 成功， code >0 失败
count         | number | 最大条数
side          | string | BUY/SELL
side_msg      | string | 买卖方向中文解释
status        | number | 订单状态 1 新订单, 2 完全成交, 3 部分成交, 4 已撤单, 5 待撤单, 6 异常订单
status_msg    | string | 订单状态中文解释
type          | number | 1 限价单, 2 市价单
baseCoin      | string | 基础币种
countCoin     | string | 计价币种
price         | string | 订单挂单价
volume        | string | 订单挂单量
avg_price     | string | 订单已成交均价
deal_volume   | string | 订单已成交量
remain_volume | string | 订单未成交量
deal_price    | string | 订单成交金额
created_at    | string | 下单时间
tradeList     | object | 成交记录

#### 返回示例:

```python
{
    "code": "0",
    "msg": "suc",
    "data": {
        "count": 1000,
        "resultList": [
            {
                "side": "SELL",
                "total_price": "4.18993396",
                "fee": 0.0,
                "created_at": 1563541098939,
                "deal_price": 0.0,
                "avg_price": "0.00000000",
                "countCoin": "USDT",
                "source": 3,
                "type": 1,
                "side_msg": "卖出",
                "volume": "0.00040000",
                "price": "10474.83490000",
                "source_msg": "WEB",
                "status_msg": "未成交",
                "deal_volume": "0.00000000",
                "fee_coin": "USDT",
                "id": 90419538,
                "remain_volume": "0.00040000",
                "baseCoin": "BTC",
                "tradeList": [],
                "status": 1
            },
            ...
        ]
    }
}
```

### 获取全部成交记录

#### GET [/open/api/all_trade](https://openapi.biki.com/open/api/all_trade)

#### 签名请求示例

api_keyd7e4d03168ac95fca79ffd60a9dc3632symbolbtcusdttime1564133020

#### 输入参数:

参数名称      | 是否必须  | 数据类型   | 描述                             | 取值范围
--------- | ----- | ------ | ------------------------------ | ----
api_key   | true  | string | 用户 api_key                     |
startDate | false | string | 开始时间,精确到秒"yyyy-MM-dd mm:hh:ss" |
endDate   | false | string | 结束时间,精确到秒"yyyy-MM-dd mm:hh:ss" |
pageSize  | false | string | 每页数据数                          |
page      | false | string | 页码                             |
sort      | false | string | 1表示倒序                          |
symbol    | true  | string | 币对                             |
sign      | true  | string | 签名                             |
time      | true  | string | 时间戳                            |

#### 返回参数:

参数名称       | 数据类型   | 描述
---------- | ------ | ---------------------
code       | string | code=0 成功， code >0 失败
count      | number | 最大条数
side       | string | BUY/SELL
type       | number | 买入 卖出
price      | string | 订单价
volume     | string | 成交数量
deal_price | string | 成交金额
ctime      | string | 成交时间

#### 返回示例:

```python
{
    "code": "0",
    "msg": "suc",
    "data": {
        "count":22,
        "resultList":[
            {
                "volume":"1.000",
                "side":"BUY",
                "feeCoin":"YLB",
                "price":"0.10000000",
                "fee":"0.16431104",
                "ctime":1510996571195,
                "deal_price":"0.10000000",
                "id":306,
                "type":"买入"
            },
            {
                "volume":"0.850",
                "side":"BUY",
                "feeCoin":"YLB",
                "price":"0.10000000",
                "fee":"0.13966438",
                "ctime":1510996571190,
                "deal_price":"0.08500000",
                "id":305,
                "type":"买入"
            },
            ...
        ]
    }
}
```

### 获取订单详情

#### GET [/open/api/order_info](https://openapi.biki.com/open/api/order_info)

#### 签名请求示例

api_keyd7e4d03168ac95fca79ffd60a9dc3632order_id30symbolbtcusdttime1564133078

#### 输入参数:

参数名称     | 是否必须 | 数据类型   | 描述         | 取值范围
-------- | ---- | ------ | ---------- | ----
api_key  | true | string | 用户 api_key |
symbol   | true | string | 币对         |
order_id | true | string | 订单号        |
sign     | true | string | 签名         |
time     | true | string | 时间戳        |

#### 返回示例:

```python
{
  code:0,
  msg:"suc",
  data:{
      "order_info":{
            "side": "SELL",
              "total_price": "3.57000000",   // 总成交价格
              "fee": 0,
              "created_at": 1546759419493,
              "deal_price": 0,
              "avg_price": "0.00000000",
              "countCoin": "USDT",
              "source": 1,
              "type": 1,
              "side_msg": "卖出",
              "volume": "1.00000000",        // 委托数量
              "price": "3.57000000",         // 委托价格
              "source_msg": "WEB",
              "status_msg": "未成交",
              "deal_volume": "0.00000000",   // 成交数量
              "fee_coin": "USDT",
              "id": 16,
              "remain_volume": "1.00000000",
              "baseCoin": "ETC",
              "tradeList": [],
              "status": 0                    // 订单状态：
                                             // 0 初始订单，1 新订单，2 完全成交，3 部分成交，4 撤销订单, 6 异常订单',
      }
      "trade_list":[                         // 订单对应的成交明细列表
          {
              "id":343,
              "created_at":"09-22 12:22",
              "price":222.33,               // 成交单价
              "volume":222.33,              // 成交数量
              "deal_price":222.33,          // 成交总金额
              "fee":222.33                  // 交易手续费支出, 交易双方收到什么币,便扣除多少数量的对应币种
          },
          {
              "id":345,
              "created_at":"09-22 12:22",
              "price":222.33,
              "volume":222.33,
              "deal_price":222.33,
              "fee":222.33
          }
      ]
  }
}
```

### 创建订单

#### POST [/open/api/create_order](https://openapi.biki.com/open/api/create_order)

#### 签名请求示例

api_keyd7e4d03168ac95fca79ffd60a9dc3632fee_is_user_exchange_coin0price9000sideBUYsymbolbtcusdttime1564133147type1volume1

#### 输入参数:

参数名称    | 是否必须  | 数据类型   | 描述             | 取值范围
------- | ----- | ------ | -------------- | ------------------------------------
api_key | true  | string | 用户 api_key     |
side    | true  | string | 买卖方向           | BUY/SELL
type    | true  | string | 挂单类型           | 1 限价委托, 2 市价委托
volume  | true  | string | 购买数量(多义, 复用字段) | type=1:表示买卖数量, type=2:买则表示总价格，卖表示总个数
price   | false | string | 委托单价           | type=2,忽略此参数
symbol  | true  | string | 币对             |
time    | true  | string | 时间戳            |
sign    | true  | string | 签名             |

#### 返回参数:

参数名称     | 数据类型   | 描述
-------- | ------ | ---------------------
code     | string | code=0 成功， code >0 失败
order_id | number | 订单号

#### 返回示例:

```python
{
    "code": "0",
    "msg": "suc",
    "data": {
        "order_id":34343
    }
}
```

### 取消委托单

#### POST [/open/api/cancel_order](https://openapi.biki.com/open/api/cancel_order)

#### 签名请求示例

api_keyd7e4d03168ac95fca79ffd60a9dc3632order_id39symbolbtcusdttime1564133229

#### 输入参数:

参数名称     | 是否必须 | 数据类型   | 描述         | 取值范围
-------- | ---- | ------ | ---------- | ----
api_key  | true | string | 用户 api_key |
order_id | true | number | 订单号        |
symbol   | true | string | 币对         |
time     | true | string | 时间戳        |
sign     | true | string | 签名         |

#### 返回示例:

```python
{
    "code": "0",
    "msg": "suc",
    "data": ""
}
```

### 取消指定币对全部委托单

#### POST [/open/api/cancel_order_all](https://openapi.biki.com/open/api/cancel_order_all)

#### 签名请求示例

api_keyd7e4d03168ac95fca79ffd60a9dc3632symbolbtcusdttime1564133267

#### 输入参数:

参数名称    | 是否必须 | 数据类型   | 描述         | 取值范围
------- | ---- | ------ | ---------- | ----
api_key | true | string | 用户 api_key |
symbol  | true | string | 币对         |
time    | true | string | 时间戳        |
sign    | true | string | 签名         |

#### 返回示例:

```python
{
    "code": "0",
    "msg": "suc",
    "data": ""
}
```

### 批量下单撤单

#### POST [/open/api/mass_replaceV2](https://openapi.biki.com/open/api/mass_replaceV2)

#### 签名请求示例

api_keyd7e4d03168ac95fca79ffd60a9dc3632mass_cancel[24, 25]mass_place[{"side": "BUY", "type": "2", "volume": 1000}, {"side": "BUY", "type": "1", "volume": 1.5, "price": 10000}]symbolbtcusdttime1564133356

#### 输入参数:

参数名称        | 是否必须  | 数据类型   | 描述
----------- | ----- | ------ | --------------------------------------------------------------------------------------------
api_key     | true  | string | 用户 api_key
symbol      | true  | string | 币对
mass_cancel | false | string | [1234,1235,...]
mass_place  | false | string | [{side:"BUY",type:"1",volume:"0.01",price:"6400",fee_is_user_exchange_coin:"0"}, {...}, ...]
time        | true  | string | 时间戳
sign        | true  | string | 签名

> mass_place 下单参数<br>
> side：方向（买卖方向BUY、SELL）<br>
> type：类型（1:限价委托、2:市价委托）<br>
> volume：购买数量（多义，复用字段） type=1:表示买卖数量type=2:买则表示总价格，卖表示总个数<br>
> price：委托单价：type=2：不需要此参数

#### 返回示例:

```python
{
    "code": "0",
    "msg": "suc",
    "data": {
      "mass_place": [{"msg": "Success","code": "0","order_id": [504,505]}],
      "mass_cancel": [
        {"msg": "Success","code": "0","order_id": [572,573,574,626,629]},
        {"msg": "Order cancellation failed","code": "8","order_id": [504,505]}
      ]
    }
}
```

> 批量下单中 如某一单下单失败则所有下单均失败

<br>

## Websocket API

### 接入 URL

#### [wss://ws.biki.com/kline-api/ws]((https://www.biki.com)) [推荐]

#### [wss://ws.bikicoin.pro/kline-api/ws](https://www.biki.com)

### 请求交互

#### 数据压缩

- WebSocket API 返回的所有数据都进行了 GZIP 压缩，需要客户端在收到数据之后解压

#### 心跳消息

- 当用户的Websocket客户端连接到Websocket服务器后，服务器会定期向其发送ping消息并包含一整数值如下： {"ping": 156200607000}

- 当用户的Websocket客户端接收到此心跳消息后，应返回pong消息并包含同一整数值： {"pong": 156200607000}

> 当Websocket服务器连续多次发送了`ping`消息却没有收到任何一次`pong`消息返回后，服务器将主动断开与此客户端的连接

### 订阅实时成交信息

#### 连接成功后发送请求:

```python
{
    "event": "sub",
    "params": {
        "channel": "market_$base$quote_trade_ticker",
        "cb_id": "自定义"
    }
}
```

> 其中$base$quote 为交易对信息<br>
> channel 示例 "channel": "market_btcusdt_trade_ticker"

#### 返回订阅成功消息

```python
{
    "event_rep": "subed",
    "channel": "market_$base$quote_trade_ticker",
    "cb_id": "原路返回",
    "ts": 1506584998239,
    "status": "ok"
}
```

#### 每当有新的成交信息后，服务器端自动推送消息如下:

```python
{
    "channel":"market_$base$quote_trade_ticker", // 订阅的交易对行情channel
    "ts":1506584998239,                         // 请求时间
    "tick":{
        "id":12121,                             // data中最大交易ID
        "ts":1506584998239,                     // data中最大时间
        "data":[
            {
                "id":12121,                     // 交易ID
                "side":"buy",                   // 买卖方向buy,sell
                "price":32.233,                 // 单价
                "vol":232,                      // 数量
                "amount":323,                   // 总额
                "ts":1506584998239,             // 数据产生时间
                "ds":'2017-09-10 23:12:21'
            },
            {
                "id":12120,                     // 交易ID
                "side":"buy",                   // 买卖方向buy,sell
                "price":32.233,                 // 单价
                "vol":232,                      // 数量
                "amount":323,                   // 总额
                "ts":1506584998239,             // 数据产生时间
                "ds":'2017-09-10 23:12:21'
            }
        ]
    }
}
```

### 订阅深度盘口

#### 连接成功后发送请求:

```python
{
    "event": "sub",
    "params": {
        "channel": "market_$base$quote_depth_step[0-2]",
        "cb_id": "自定义",
        "asks": 150,
        "bids": 150
    }
}
```

> $base$quote表示btcusdt等币对,step[0-2]表示深度有3个维度，0、1、2<br>
> channel 示例 "channel": "market_btcusdt_depth_step0"

#### 返回订阅成功消息

```python
{
    "event_rep": "subed",
    "channel": "market_$base$quote_depth_step[0-2]",
    "cb_id": "原路返回",
    "asks": 150,
    "bids": 150,
    "ts": 1506584998239,
    "status": "ok"
}
```

#### 每当深度数据有更新时，服务器端自动推送消息如下:

```python
{
    "channel": "market_$base$quote_depth_step[0-2]",
    "ts": 1506584998239,
    "tick": {
        "asks": [
            [22112.22,0.9332],      // 价格，数量
            [22112.21,0.2]
        ],
        "buys": [
            [22111.22,0.9332],
            [22111.21,0.2]
        ]
    }
}
```

### 订阅K线数据

#### 连接成功后发送请求:

```python
{
    "event": "sub",
    "params": {
        "channel": "market_$base$quote_kline_[1min/5min/15min/30min/60min/1day/1week/1month]",
        "cb_id": "自定义"
    }
}
```

> channel 示例 "channel": "market_btcusdt_kline_1min"

#### 返回订阅成功消息

```python
{
    "event_rep": "subed",
    "channel": "market_$base$quote_kline_[1min/5min/15min/30min/60min/1day/1week/1month]",
    "cb_id": "原路返回",
    "ts": 1506584998239,
    "status": "ok"
}
```

#### 每当K线数据更新时，服务器端自动推送消息如下:

```python
{
    "channel": "market_$base$quote_kline_[1min/5min/15min/30min/60min/1day/1week/1month]",
    "ts": 1506584998239,
    "tick": {
        "id": 1506602880,
        "amount": 123.1221,
        "vol": 1212.12211,
        "open": 2233.22,
        "close": 1221.11,
        "high": 22322.22,
        "low": 2321.22
    }
}
```

[^_^]: aadf4
