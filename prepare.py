#!/usr/bin/env python

import argparse
import ruamel.yaml
import os

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

from ruamel.yaml.util import load_yaml_guess_indent

# Define path
basepath = os.path.abspath(os.path.dirname(__file__))
K8S_CLUSTER_CONFIG_PATH = os.path.abspath(
    basepath + '/../inventory/group_vars/k8s-cluster.yml')
INVENTORY_CONFIG_PATH = os.path.abspath(
    basepath + '/../inventory/inventory.cfg')

# Define args
config_parser = argparse.ArgumentParser(add_help=False)
config_parser.add_argument(
    '--network', help='Cluster network plugin. Default: flannel', default='flannel',
    choices=["calico", "contiv", "weave", "flannel", "cloud"],  required=False)
config_parser.add_argument(
    '--enable-helm', help='Enable helm. Default: False', action="store_true", required=False)
config_parser.add_argument(
    '--helm-deployment-type', help='Helm deployment type. Default: host', choices=["host", "docker"], default='host', required=False)
config_parser.add_argument(
    '--enable-local-volumes', help='Enable local volumes. Default: False', action="store_true", required=False)
config_parser.add_argument(
    '--disable-swap-fail', help='Disable swap fail. Default: False', action="store_false", required=False)


parser = argparse.ArgumentParser(add_help=True)
subparsers = parser.add_subparsers(help='Available Types', dest='type')
singlenode_parser = subparsers.add_parser(
    'singlenode', help='Single node cluster', parents=[config_parser])
multinode_parser = subparsers.add_parser(
    'multinode', help='Multi node cluster', parents=[config_parser])

multinode_parser.add_argument(
    '--masters', help='Cluster masters number. Default: 1', type=int, default=1, required=False)
multinode_parser.add_argument(
    '--nodes', help='Cluster nodes number exclude master. Default: 2', type=int, default=2, required=False)
multinode_parser.add_argument(
    '--master-as-node', help='Use master as node. Default: No', action="store_true", required=False)


# Configure inventory/group_vars/k8s-cluster.yml
def prepare_k8s_cluster_config(args):

    config, ind, bsi = load_yaml_guess_indent(
        open(K8S_CLUSTER_CONFIG_PATH), preserve_quotes=True)

    config["kube_network_plugin"] = args.network
    config["helm_enabled"] = args.enable_helm
    config["helm_deployment_type"] = args.helm_deployment_type
    config["kubelet_fail_swap_on"] = args.disable_swap_fail
    config["local_volumes_enabled"] = args.enable_local_volumes

    ruamel.yaml.round_trip_dump(config, open(K8S_CLUSTER_CONFIG_PATH, 'w'),
                                width=8000, indent=2, block_seq_indent=bsi)


# Configure inventory/inventory.cfg
def prepare_inventory(args):

    cfgfile = open(INVENTORY_CONFIG_PATH, 'w')

    config = configparser.ConfigParser(allow_no_value=True)
    config.add_section('all')
    config.add_section('kube-master')
    config.add_section('etcd')
    config.add_section('kube-node')
    config.add_section('k8s-cluster:children')

    if args.type == 'singlenode':
        config.set(
            'all', 'master ansible_ssh_host=  ansible_python_interpreter=/usr/bin/python3  # ip=10.3.0.1')
        config.set('kube-master', 'master')
        config.set('etcd', 'master')
        config.set('kube-node', 'master')

    if args.type == 'multinode':
        for m in range(args.masters):
            master_name = 'master-' + str(m + 1)
            config.set('all', master_name +
                       ' ansible_ssh_host=  ansible_python_interpreter=/usr/bin/python3  # ip=10.3.0.' + str(m + 1))
            config.set('kube-master', master_name)
            config.set('etcd', master_name)
            if args.master_as_node:
                config.set('kube-node', master_name)

        for n in range(args.nodes):
            node_name = 'node-' + str(n + 1)
            config.set(
                'all', node_name + ' ansible_ssh_host=  ansible_python_interpreter=/usr/bin/python3  # ip=10.3.0.' + str(n + 10))
            config.set('kube-node', node_name)

    config.set('k8s-cluster:children', 'kube-node')
    config.set('k8s-cluster:children', 'kube-master')

    config.write(cfgfile)
    cfgfile.close()

if __name__ == "__main__":
    args = parser.parse_args()
    prepare_k8s_cluster_config(args)
    prepare_inventory(args)
