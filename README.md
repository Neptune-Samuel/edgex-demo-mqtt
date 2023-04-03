## EDGEX演示项目

### 环境准备

1. Ubuntu操作系统

2. 安装docker-ce 

3. 安装python3及 paho-mqtt-client python包

```shell

    sudo apt install python3-pip 
    pip3 install paho.mqtt

```

### 运行 

```sh
docker compose up -d 
cd virtual-device 
python3 device.py 

```

### 使用Edgex UI 

http://IP:4000 


### 使用 API， 请参考官方API文档 

[EdgeX API](https://docs.edgexfoundry.org/2.1/api/Ch-APIIntroduction/)

