# kube-tasks

Easy Kubespray configurator.

## Requirements
- Python 2.7.x or 3.x
- ruamel.yaml python package
- netaddr python package (for Kubespray)
- Ansible >= 2.4

## Getting Started
Clone or download kubespray repo first. See detailed instructions by link - https://github.com/kubernetes-incubator/kubespray
### Installing
```bash
$ pip install ruamel.yaml
$ pip install netaddr
$ cd kubespray
$ git clone https://github.com/cyberfantom/kube-tasks.git
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
$ python kube-tasks/prepare.py multinode --master-ips 1.2.3.4 --node-ips 1.2.3.5 1.2.3.4.6
```
##### Example for multi node cluster with Helm and Heapster monitoring:
```bash
$ python kube-tasks/prepare.py multinode \
--master-ips 1.2.3.4 \
--node-ips 1.2.3.5 1.2.3.4.6 \
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
| --master-ips  | Ip list. Values: 1.2.3.4 1.2.3.4...1.2.3.n  | Yes. For singlenode and multionode modes  |
| --node-ips  | Ip list. Values: 1.2.3.4 1.2.3.4...1.2.3.n  | Yes. For multinode mode only  |
|--master-as-node | Use master host as node. No value, boolean flag.| No. Default: false (for multinode)|
|--network | Cluster network plugin. Values: calico, contiv, weave, flannel, cloud | No. Default: flannel|
|--enable-helm | Enable helm. No value, boolean flag. | No. Default: false|
|--helm-deployment-type | Helm deployment type. Values: host, docker | No. Default: host|
|--enable-local-volumes | Enable local volumes. No value, boolean flag.|  No. Default: false|
|--disable-swap-fail | Disable swap fail. No value, boolean flag. |No. Default: false|
|--enable-kube-shell | Install kube-shell. No value, boolean flag. | No. Default: false |
|--enable-monitoring | Install Heapster. No value, boolean flag. | No. Default: false |
|--enable-ingress | Install simple nginx ingress. No value, boolean flag. | No. Default: false |


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
