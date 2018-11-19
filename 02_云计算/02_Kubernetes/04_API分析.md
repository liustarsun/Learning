


## API对象

### 三大类属性
元数据metadata-标识API对象       
> 至少有三个元数据：namespace，name和uid；另外可以用各种各样的标签labels用来标识和匹配不同对象，如可以用标签env来标识区分不同的服务部署环境，env=dev，env=testing， env=production来标识开发、测试、生成的不同服务


规范spec-描述用户期望k8s集群中分布式系统达到的理想状态(Desired state)     
> 如用户通过复制控制器Replication Controller设置期望的pod副本数为2，那么RC当前的程序逻辑就是自动启动新的pod，争取达到副本数为3    
**所有配置都是通过API对象的spec去设置，即所有操作都是声明式，而不是命令式**， 设置副本数为3的操作就是声明式，而给副本数加1的操作是命令式，声明式在分布式系统中的好处是稳定  

状态status


### Pod概念