#!/usr/bin/env python
#
# Copyright 2020 VMware, Inc.
# SPDX-License-Identifier: BSD-2-Clause OR GPL-3.0-only
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING,
# BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: nsxt_policy_dhcp_server_config
short_description: Create or Delete a Policy DHCP Server Config
description:
    Creates or deletes a Policy DHCP Server Config.
    Required attributes include id and display_name.
version_added: "2.8"
author: Gautam Verma
options:
    hostname:
        description: Deployed NSX manager hostname.
        required: true
        type: str
    username:
        description: The username to authenticate with the NSX manager.
        type: str
    password:
        description:
            - The password to authenticate with the NSX manager.
            - Must be specified if username is specified
        type: str
    ca_path:
        description: Path to the CA bundle to be used to verify host's SSL
                     certificate
        type: str
    nsx_cert_path:
        description: Path to the certificate created for the Principal
                     Identity using which the CRUD operations should be
                     performed
        type: str
    nsx_key_path:
        description:
            - Path to the certificate key created for the Principal Identity
              using which the CRUD operations should be performed
            - Must be specified if nsx_cert_path is specified
        type: str
    request_headers:
        description: HTTP request headers to be sent to the host while making
                     any request
        type: dict
    display_name:
        description:
            - Display name.
            - If resource ID is not specified, display_name will be used as ID.
        required: false
        type: str
    state:
        choices:
        - present
        - absent
        description: "State can be either 'present' or 'absent'.
                     'present' is used to create or update resource.
                     'absent' is used to delete resource."
        required: true
    validate_certs:
        description: Enable server certificate verification.
        type: bool
        default: False
    tags:
        description: Opaque identifiers meaningful to the API user.
        type: dict
        suboptions:
            scope:
                description: Tag scope.
                required: true
                type: str
            tag:
                description: Tag value.
                required: true
                type: str
    do_wait_till_create:
        type: bool
        default: false
        description:
            - Can be used to wait for the realization of subresource before the
              request to create the next resource is sent to the Manager.
            - Can be specified for each subresource.
    id:
        description: The id of the DHCP Server Config.
        type: str
    description:
        description: DHCP Server Config description.
        type: str
    edge_cluster_info:
        description:
            - Auto assigned if only one edge cluster is configured on
              enforcement-point.
            - Modifying edge cluster will reallocate DHCP server to the new
              edge cluster. Please note that re-allocating edge-cluster will
              result in losing of all exisitng DHCP lease information.
            - Change edge cluster only when losing DHCP leases is not a real
              problem, e.g. cross-site migration or failover and all client
              hosts will be reboot and get new IP addresses.
        type: dict
        suboptions:
            site_id:
                description: site_id where edge cluster is located
                default: default
                type: str
            enforcementpoint_id:
                description: enforcementpoint_id where edge cluster is
                             located
                default: default
                type: str
            edge_cluster_id:
                description: ID of the edge cluster
                type: str
            edge_cluster_display_name:
                description:
                    - display name of the edge cluster.
                    - Either this or edge_cluster_id must be specified.
                      If both are specified, edge_cluster_id takes precedence
                type: str
    lease_time:
        description:
            - IP address lease time in seconds.
            - Min is 60
            - Max is 4294967295
        type: int
    preferred_edge_nodes_info:
        description: Policy paths to edge nodes on which the DHCP servers run.
                     The first edge node is assigned as active edge, and second
                     one as stanby edge. If only one edge node is specified,
                     the DHCP servers will run without HA support. When this
                     property is not specified, edge nodes are auto-assigned
                     during realization of the DHCP server.
        type: list
        elements: dict
        suboptions:
            site_id:
                description: site_id where edge node is located
                default: default
                type: str
            enforcementpoint_id:
                description: enforcementpoint_id where edge node is
                                located
                default: default
                type: str
            edge_cluster_id:
                description: edge_cluster_id where edge node is located
                type: str
            edge_cluster_display_name:
                description:
                    - display name of the edge cluster.
                    - either this or edge_cluster_id must be specified.
                      If both are specified, edge_cluster_id takes precedence
                type: str
            edge_node_id:
                description: ID of the edge node
                type: str
            edge_node_display_name:
                description:
                    - Display name of the edge node.
                    - either this or edge_node_id must be specified. If
                      both are specified, edge_node_id takes precedence
                type: str
    server_addresses:
        description:
            - DHCP server address in CIDR format. Both IPv4 and IPv6
              address families are supported.
            - Prefix length should be less than or equal to 30 for IPv4
              address family and less than or equal to 126 for IPv6.
            - When not specified, IPv4 value is auto-assigned to 100.96.0.1/30.
            - Ignored when this object is configured at a Segment.
            - Max 2 items
        type: list
        elements: str
'''

EXAMPLES = '''
- name: Update DHCP Server Config
  nsxt_policy_dhcp_server_config:
    hostname: "10.10.10.10"
    nsx_cert_path: /root/com.vmware.nsx.ncp/nsx.crt
    nsx_key_path: /root/com.vmware.nsx.ncp/nsx.key
    validate_certs: False
    display_name: test-dhcp-server-config
    state: present
    edge_cluster_info:
      edge_cluster_display_name: EDGECLUSTER1
    lease_time: 100
    preferred_edge_nodes_info:
      - edge_cluster_display_name: EDGECLUSTER1
        edge_node_display_name: NODE1
    server_addresses:
      - '100.100.0.1/8'
'''

RETURN = '''# '''

from ansible.module_utils.nsxt_base_resource import NSXTBaseRealizableResource
from ansible.module_utils.nsxt_resource_urls import DHCP_SERVER_CONFIG_URL
import ansible.module_utils.nsxt_utils as nsxt_utils


class NSXTDHCPServerConfig(NSXTBaseRealizableResource):
    @staticmethod
    def get_resource_spec():
        dhcp_server_config_arg_spec = {}
        dhcp_server_config_arg_spec.update(
            edge_cluster_info=dict(
                required=False,
                type='dict',
                options=dict(
                    # Note that only default site_id and
                    # enforcementpoint_id are used
                    site_id=dict(
                        type='str',
                        default="default"
                    ),
                    enforcementpoint_id=dict(
                        type='str',
                        default="default"
                    ),
                    edge_cluster_id=dict(
                        type='str'
                    ),
                    edge_cluster_display_name=dict(
                        type='str'
                    )
                )
            ),
            lease_time=dict(
                default=86400,
                type='int'
            ),
            preferred_edge_nodes_info=dict(
                required=False,
                type='list',
                options=dict(
                    # Note that only default site_id and
                    # enforcementpoint_id are used
                    site_id=dict(
                        type='str',
                        default="default"
                    ),
                    enforcementpoint_id=dict(
                        type='str',
                        default="default"
                    ),
                    edge_cluster_id=dict(
                        type='str'
                    ),
                    edge_cluster_display_name=dict(
                        type='str'
                    ),
                    edge_node_id=dict(
                        type='str'
                    ),
                    edge_node_display_name=dict(
                        type='str'
                    )
                )
            ),
            server_addresses=dict(
                type='list',
                elements='str'
            ),
        )
        return dhcp_server_config_arg_spec

    @staticmethod
    def get_resource_base_url(baseline_args=None):
        return DHCP_SERVER_CONFIG_URL

    def update_resource_params(self, nsx_resource_params):
        nsxt_utils.read_and_put_edge_cluster_info_to(
            nsx_resource_params, self.get_id_using_attr_name_else_fail)

        nsxt_utils.read_and_put_preferred_edge_nodes_info_to(
            nsx_resource_params, self.get_id_using_attr_name_else_fail)


if __name__ == '__main__':
    dhcp_server_config = NSXTDHCPServerConfig()
    dhcp_server_config.realize()
