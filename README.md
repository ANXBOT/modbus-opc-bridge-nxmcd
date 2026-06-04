# Modbus TCP to OPC UA Bridge for NXMCD Virtual Debugging

Modbus TCP 转 OPC UA 通信桥接，实现 NXMCD 虚拟调试。

## 功能

- 从 Modbus TCP 服务器（NXMCD）读取寄存器数据
- 将数据映射到 OPC UA 服务器节点
- 支持线圈(Coils)、离散输入(Discrete Inputs)、保持寄存器(Holding Registers)、输入寄存器(Input Registers)
- 可配置的地址映射表
- 实时数据同步

## 架构

```
NXMCD (Modbus TCP Server)
    │
    ▼ 127.0.0.1:502
┌─────────────────┐
│  Modbus Client  │
│  (pymodbus)     │
└────────┬────────┘
         │ 数据映射
┌────────▼────────┐
│  OPC UA Server  │
│  (opcua)        │
└────────┬────────┘
         │
    ▼ opc.tcp://0.0.0.0:4840
OPC UA Client (NXMCD / 调试工具)
```

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置

编辑 `config/mapping.yaml` 配置 Modbus 地址映射。

### 运行

```bash
python src/main.py
```

## 配置说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| MODBUS_HOST | 127.0.0.1 | Modbus TCP 服务器地址 |
| MODBUS_PORT | 502 | Modbus TCP 端口 |
| OPC_HOST | 0.0.0.0 | OPC UA 服务器绑定地址 |
| OPC_PORT | 4840 | OPC UA 服务器端口 |
| POLL_INTERVAL | 0.5 | 数据轮询间隔（秒） |

## 许可证

MIT License
