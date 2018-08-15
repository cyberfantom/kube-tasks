# kube-tasks
[![Maintainability](https://api.codeclimate.com/v1/badges/757a5b3f07442971d4df/maintainability)](https://codeclimate.com/github/cyberfantom/kube-tasks/maintainability)

Easy Kubespray configurator.

## Requirements
- Python 2.7.x or 3.x
- ruamel.yaml python package
- Ansible >= 2.4

## Getting Started
Clone kubespray repo first and switch branch to the latest version. You can find the latest version by link - https://github.com/kubernetes-incubator/kubespray/releases. For this example we'll use version v2.6.0.
```bash
$ git clone https://github.com/kubernetes-incubator/kubespray.git
$ cd kubespray
$ git checkout -b tags/v2.6.0
```
### Installing Kube Tasks
```bash
$ git clone https://github.com/cyberfantom/kube-tasks.git
$ pip install -r kube-tasks/requirements.txt
```

### Quick Start
#### Get Help
```bash
$ python kube-tasks/prepare.py -h

positional arguments:
  {singlenode,multinode}
                        Available Types
    singlenode          Single node cluster
    multinode           Multi node cluster

$ python kube-tasks/prepare.py singlenode -h
...

$ python kube-tasks/prepare.py multinode -h
...
```

#### Simple Usage
##### Main usage (see more in options table):
```bash
$ python kube-tasks/prepare.py {singlenode|multinode} --master-ips 1.2.3.4 [options]
```
*where 1.2.x.x - your external host ips*

##### Example for simple single node cluster:
```bash
$ python kube-tasks/prepare.py singlenode --master-ips 1.2.3.4
```
##### Example for simple multi node cluster:
```bash
$ python kube-tasks/prepare.py multinode --master-ips 1.2.3.4 --node-ips 1.2.3.5 1.2.3.4.6 [--etcd-ips 1.2.3.7 1.2.3.8 1.2.3.9]
```
Here --etcd-ips is the optional param. If this param is omitted, etcd service will be installed on the master node(s) by default.
Remeber that etcd nodes must be an odd number - 1,3,5...
##### Example for multi node cluster with 1 master, 3 worker nodes, Helm and Elasticsearch/Fluentd/Kibana monitoring:
```bash
$ python kube-tasks/prepare.py multinode \
--master-ips 1.2.3.4 \
--node-ips 1.2.3.5 1.2.3.6 1.2.3.7\
--enable-helm --enable-monitoring
```
##### Run ansible playbook after:
```bash
$ ansible-playbook -u <your ssh user> -b -i inventory/inventory.cfg \
kube-tasks/deploy.yml --private-key=/path/to/your/ssh/private_key
```
#### Options
| Option  | Value |Required |
| ------------- | ------------- |------------- |
| --master-ips  | Master IP list. Values: 1.2.3.4 1.2.3.4...1.2.3.n  | Yes. For singlenode and multionode modes  |
| --node-ips  | Nodes IP list. Values: 1.2.3.4 1.2.3.4...1.2.3.n  | Yes. For multinode mode only  |
| --etcd-ips  | Etcd nodes IP list. Values: 1.2.3.7 1.2.3.8...1.2.3.n  | No. If defined must be an odd number  |
| --python-interpreter  | Ansible remote python interpreter path.  | No. Default: /usr/bin/python3  |
|--master-as-node | Use master host as node. No value, boolean flag.| No. Default: false (for multinode)|
|--network | Cluster network plugin. Values: calico, contiv, weave, flannel, cloud | No. Default: flannel|
|--enable-helm | Enable helm. No value, boolean flag. | No. Default: false|
|--helm-deployment-type | Helm deployment type. Values: host, docker | No. Default: docker|
|--enable-local-volumes | Enable local volumes. No value, boolean flag.|  No. Default: false|
|--disable-swap-fail | Disable swap fail. No value, boolean flag. |No. Default: false|
|--enable-kube-shell | Install kube-shell. No value, boolean flag. | No. Default: false |
|--enable-monitoring | Install Elasticsearch/Fluentd/Kibana. No value, boolean flag. | No. Default: false |
|--loadbalancer | External loadbalancer FQDN. It can be AWS ELB domain name, Haproxy, Nginx or any other. See more https://github.com/kubernetes-incubator/kubespray/blob/master/docs/ha-mode.md | No. Default: None |
|--enable-ingress | Install simple nginx ingress. No value, boolean flag. | No. Default: false |


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
