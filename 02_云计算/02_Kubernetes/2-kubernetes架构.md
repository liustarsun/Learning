## **K8S** 先放这里
> 2017年12月9日，23:28

[kubernetes在线教程](https://kubernetes.io/docs/tutorials/kubernetes-basics/)

### **1. 基本概念**
#### **1.1 Cluster**
**Cluster** 是计算、存储和网络资源的集合，Kubernetes 利用这些资源运行各种基于容器的应用

Master
Master 是 Cluster 的大脑，它的主要职责是调度，即决定将应用放在哪里运行。Master 运行 Linux 操作系统，可以是物理机或者虚拟机。为了实现高可用，可以运行多个 Master。


-------
### 2. 组成
#### 2.1 核心组件
etcd-配置文件，yaml或者是json格式，保存集群状态      
apiserver-提供资源操作唯一接口，提供认证，访问控制等     
controller manager-负责集群管理，容器调度，自动扩展， 更新迭代，维护资源状态等     
scheduler-负责维护资源的调度，按照预定策略将pod调度到相应机器上     
kubelet-维护容器的声明周期，同时也负责Volume(CVI)和网络(CNI)管理     
Container runtime-负责镜像管理，pod和容器的真正运行(CRI)      
服务节点Node-真正运行容器的主机，管理镜像，容器，cluster内的服务发现和负载均衡     

#### 2.2 推荐的Add-ons
 kube-dns-负责为集群提供DNS服务     
 Ingress controller-为服务提供外网入口     
 Heapster-资源监控    
 Dashboard-提供GUI   
 Federation-跨可用区的集群    
 Fluentd-elasticsearch-集群日志采集，存储和查询    



 ----------
 ### 3. 分层架构
 核心层-对外提供API构建高层应用，对内提供插件式应用执行环境    
 应用层-部署和路由          
 管理层-系统度量，自动化，策略管理          
 接口层-kubectl命令行工具，客户端SDK，集群联邦            
 生态系统-接口上的容器集群管理调度的生态系统
 > kubernets外部：日志，监控，配置管理，CI，CD，workflow, Faas, OTS应用，ChatOps等       
 kubernetes内部：CRI，CNI，CVI，镜像仓库，Cloud provider，集群自身配置和管理            