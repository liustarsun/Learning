# 安装kubeadm

## 1. 启动代理 
```
1. sudo sslocal -c ~/shadowsocks.json -d start
2. sudo su -
```

## 2. 设置HTTP代理
```
apt-get install polipo
vi /etc/polipo/config

#********************************************#
socksParentProxy = "127.0.0.1:1080"
socksProxyType = socks5

chunkHighMark = 50331648
objectHighMark = 16384

serverMaxSlots = 64
serverSlots = 16
serverSlots1 = 32

proxyAddress = "0.0.0.0"
proxyPort = 8123

/etc/init.d/polipo restart
export http_proxy="http://127.0.0.1:8123/"
#********************************************#

```
## 3. 设置docker代理
```

```

## 4. 安装/更新docker
```
apt-get update && apt-get install docker.io
```

## 5. 关掉swap
```
swapoff -a
```

## 6. 安装kubeadm/kubectl/kubelet
```
1. apt-get update && apt-get install -y apt-transport-https curl

2. wget https://packages.cloud.google.com/apt/doc/apt-key.gpg  && apt-key add apt-key.gpg 

3. cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
deb https://apt.kubernetes.io/ kubernetes-xenial main
EOF

4. apt-get update
5. apt-get install -y kubelet kubeadm kubectl
6. apt-mark hold kubelet kubeadm kubectl
```
**以上是所有node都需要做的事情，其中1在每次启动都要去做，其他的只需要做一次**

-------------------------------
## 6. 初始化kubeadm节点

```
root@docker:~# kubeadm init --apiserver-advertise-address=192.168.0.111 --pod-network-cidr=10.244.0.0/16

#*********************************************************************************#
1114 22:35:16.612894    4836 version.go:93] could not fetch a Kubernetes version from the internet: unable to get URL "https://dl.k8s.io/release/stable-1.txt": Get https://storage.googleapis.com/kubernetes-release/release/stable-1.txt: net/http: request canceled while waiting for connection (Client.Timeout exceeded while awaiting headers)
I1114 22:35:16.613072    4836 version.go:94] falling back to the local client version: v1.12.2
[init] using Kubernetes version: v1.12.2
[preflight] running pre-flight checks
[preflight/images] Pulling images required for setting up a Kubernetes cluster
[preflight/images] This might take a minute or two, depending on the speed of your internet connection
[preflight/images] You can also perform this action in beforehand using 'kubeadm config images pull'
[kubelet] Writing kubelet environment file with flags to file "/var/lib/kubelet/kubeadm-flags.env"
[kubelet] Writing kubelet configuration to file "/var/lib/kubelet/config.yaml"
[preflight] Activating the kubelet service
[certificates] Generated ca certificate and key.
[certificates] Generated apiserver-kubelet-client certificate and key.
[certificates] Generated apiserver certificate and key.
[certificates] apiserver serving cert is signed for DNS names [docker kubernetes kubernetes.default kubernetes.default.svc kubernetes.default.svc.cluster.local] and IPs [10.96.0.1 192.168.0.111]
[certificates] Generated front-proxy-ca certificate and key.
[certificates] Generated front-proxy-client certificate and key.
[certificates] Generated etcd/ca certificate and key.
[certificates] Generated etcd/peer certificate and key.
[certificates] etcd/peer serving cert is signed for DNS names [docker localhost] and IPs [192.168.0.111 127.0.0.1 ::1]
[certificates] Generated etcd/server certificate and key.
[certificates] etcd/server serving cert is signed for DNS names [docker localhost] and IPs [127.0.0.1 ::1]
[certificates] Generated etcd/healthcheck-client certificate and key.
[certificates] Generated apiserver-etcd-client certificate and key.
[certificates] valid certificates and keys now exist in "/etc/kubernetes/pki"
[certificates] Generated sa key and public key.
[kubeconfig] Wrote KubeConfig file to disk: "/etc/kubernetes/admin.conf"
[kubeconfig] Wrote KubeConfig file to disk: "/etc/kubernetes/kubelet.conf"
[kubeconfig] Wrote KubeConfig file to disk: "/etc/kubernetes/controller-manager.conf"
[kubeconfig] Wrote KubeConfig file to disk: "/etc/kubernetes/scheduler.conf"
[controlplane] wrote Static Pod manifest for component kube-apiserver to "/etc/kubernetes/manifests/kube-apiserver.yaml"
[controlplane] wrote Static Pod manifest for component kube-controller-manager to "/etc/kubernetes/manifests/kube-controller-manager.yaml"
[controlplane] wrote Static Pod manifest for component kube-scheduler to "/etc/kubernetes/manifests/kube-scheduler.yaml"
[etcd] Wrote Static Pod manifest for a local etcd instance to "/etc/kubernetes/manifests/etcd.yaml"
[init] waiting for the kubelet to boot up the control plane as Static Pods from directory "/etc/kubernetes/manifests" 
[init] this might take a minute or longer if the control plane images have to be pulled
[apiclient] All control plane components are healthy after 27.589070 seconds
[uploadconfig] storing the configuration used in ConfigMap "kubeadm-config" in the "kube-system" Namespace
[kubelet] Creating a ConfigMap "kubelet-config-1.12" in namespace kube-system with the configuration for the kubelets in the cluster
[markmaster] Marking the node docker as master by adding the label "node-role.kubernetes.io/master=''"
[markmaster] Marking the node docker as master by adding the taints [node-role.kubernetes.io/master:NoSchedule]
[patchnode] Uploading the CRI Socket information "/var/run/dockershim.sock" to the Node API object "docker" as an annotation
[bootstraptoken] using token: gx074d.vneuxz0er102lc37
[bootstraptoken] configured RBAC rules to allow Node Bootstrap tokens to post CSRs in order for nodes to get long term certificate credentials
[bootstraptoken] configured RBAC rules to allow the csrapprover controller automatically approve CSRs from a Node Bootstrap Token
[bootstraptoken] configured RBAC rules to allow certificate rotation for all node client certificates in the cluster
[bootstraptoken] creating the "cluster-info" ConfigMap in the "kube-public" namespace
[addons] Applied essential addon: CoreDNS
[addons] Applied essential addon: kube-proxy

Your Kubernetes master has initialized successfully!

To start using your cluster, you need to run the following as a regular user:

  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config

You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  https://kubernetes.io/docs/concepts/cluster-administration/addons/

You can now join any number of machines by running the following on each node
as root: ===> 使用root

  kubeadm join 192.168.0.111:6443 --token gx074d.vneuxz0er102lc37 --discovery-token-ca-cert-hash sha256:f0208625f7c808cd09ec24dc40c49d4e72caaec8c01ce53dce054342aa78784c

#*****************************************************************************#

```

## 7. 设置kubectl
```
root@docker:~# exit
logout
asb@docker:~$ mkdir -p $HOME/.kube
asb@docker:~$ sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
[sudo] password for asb: 
asb@docker:~$ sudo chown $(id -u):$(id -g) $HOME/.kube/config
asb@docker:~$ echo "source < (kubectl completio bash)" >> ~/.bashrc

```



## 8. 安装Pod网络
```
asb@docker:~$ kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/bc79dd1505b0c8681ece4de4c0d86c5cd2643275/Documentation/kube-flannel.yml
asb@docker:~$ kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.
yml
clusterrole.rbac.authorization.k8s.io/flannel created
clusterrolebinding.rbac.authorization.k8s.io/flannel created
serviceaccount/flannel created
configmap/kube-flannel-cfg created
daemonset.extensions/kube-flannel-ds-amd64 created
daemonset.extensions/kube-flannel-ds-arm64 created
daemonset.extensions/kube-flannel-ds-arm created
daemonset.extensions/kube-flannel-ds-ppc64le created
daemonset.extensions/kube-flannel-ds-s390x created
asb@docker:~$ 

// 仔细检查下应该选用哪个配置文件
https://github.com/coreos/flannel/blob/master/Documentation/kubernetes.md
```
## 并且是否要加入
```
Set /proc/sys/net/bridge/bridge-nf-call-iptables to 1 by running sysctl net.bridge.bridge-nf-call-iptables=1 to pass bridged IPv4 traffic to iptables’ chains. This is a requirement for some CNI plugins to work, for more information please see here.
```



=====
# 安装Node节点
## 1. 首先执行modprobe操作
```
asb@k8s-node:~$ sudo modprobe ip_vs_rr
asb@k8s-node:~$ sudo modprobe ip_vs_wrr
asb@k8s-node:~$ sudo modprobe ip_vs_sh
asb@k8s-node:~$ sudo modprobe ip_vs
```

## 2. 把Node加入集群
```
// 创建成功后在最后会显示相关的内容
asb@docker:~$ sudo kubeadm join --token gx074d.vneuxz0er102lc37 192.168.0.111:6443 --discovery-token-ca-cert-hash sha256:f0208625f7c808cd09ec24dc40c49d4e72caaec8c01ce53dce054342aa78784c
```

====
# 如何停止master节点
```

```

# 如何删除Node节点
```
PS C:\Users\xingyanl> kubectl drain minikube --delete-local-data --force --ignore-daemonsets
node "minikube" cordoned
pod "kubernetes-bootcamp-79fb999b88-8xlms" evicted
pod "kubernetes-bootcamp-79fb999b88-9tj7n" evicted
pod "kubernetes-bootcamp-79fb999b88-wjsrp" evicted
node "minikube" drained
PS C:\Users\xingyanl> kubectl delete node minikube
node "minikube" deleted
```



# 如何查看log==>除了pod都处于running状态，其他的状态都表示没有就绪
1. **kubectl describe pod/deployment等等**
```
// 通过描述可以看到pod的相关信息
PS C:\Users\xingyanl> kubectl describe pod  kubernetes-bootcamp-79fb999b88-8xlms


Events:
  Type     Reason                  Age                  From               Message
  ----     ------                  ----                 ----               -------
  Warning  FailedCreatePodSandBox  34m (x4296 over 1d)  kubelet, minikube  Failed create pod sandbox.  ====> 相关问题的原因
  Normal   SuccessfulMountVolume   30m                  kubelet, minikube  MountVolume.SetUp succeeded for volume "default-token-bq4ql"
  Warning  FailedCreatePodSandBox  54s (x64 over 30m)   kubelet, minikube  Failed create pod sandbox.

```

2. **kubectl.exe get deployment/pods** ==> 查看pod的东西
```
PS C:\Users\xingyanl> kubectl.exe get pods
NAME                                   READY     STATUS              RESTARTS   AGE
kubernetes-bootcamp-79fb999b88-8xlms   0/1       ContainerCreating   0          3d
kubernetes-bootcamp-79fb999b88-9tj7n   0/1       ContainerCreating   0          3d
kubernetes-bootcamp-79fb999b88-wjsrp   0/1       ContainerCreating   0          3d
PS C:\Users\xingyanl>

// deployment是用来管理pods的===>管理资源的各种方式
PS C:\Users\xingyanl> kubectl.exe get deployment
NAME                  DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
kubernetes-bootcamp   3         3         3            0           3d
PS C:\Users\xingyanl> kubectl.exe get deployment kubernetes-bootcamp
NAME                  DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
kubernetes-bootcamp   3         3         3            0           3d
PS C:\Users\xingyanl> kubectl.exe describe deployment kubernetes-bootcamp

PS C:\Users\xingyanl> kubectl.exe get replicaSet
NAME                             DESIRED   CURRENT   READY     AGE
kubernetes-bootcamp-79fb999b88   3         3         0         3d
PS C:\Users\xingyanl> kubectl.exe get daemonSet
No resources found.
PS C:\Users\xingyanl> kubectl.exe get StatefulSet
No resources found.
PS C:\Users\xingyanl> kubectl.exe get job
No resources found.
PS C:\Users\xingyanl>
```
