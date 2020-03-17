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

from ansible.module_utils.nsxt_resource_urls import (
    EDGE_CLUSTER_URL, EDGE_NODE_URL)


def read_and_put_edge_cluster_info_to(
        nsx_resource_params, infer_id_method):
    if "edge_cluster_info" in nsx_resource_params:
        edge_cluster_info = nsx_resource_params.pop(
            "edge_cluster_info")
        site_id = edge_cluster_info["site_id"]
        enforcementpoint_id = edge_cluster_info["enforcementpoint_id"]
        edge_cluster_base_url = (
            EDGE_CLUSTER_URL.format(site_id, enforcementpoint_id))
        edge_cluster_id = infer_id_method(
            "edge_cluster", edge_cluster_info, edge_cluster_base_url,
            "Edge Cluster")
        nsx_resource_params["edge_cluster_path"] = (
            edge_cluster_base_url + "/" + edge_cluster_id)


def read_and_put_preferred_edge_nodes_info_to(
        nsx_resource_params, infer_id_method):
    if "preferred_edge_nodes_info" in nsx_resource_params:
        preferred_edge_nodes_info = nsx_resource_params.pop(
            "preferred_edge_nodes_info")
        nsx_resource_params["preferred_edge_paths"] = []
        for preferred_edge_node_info in preferred_edge_nodes_info:
            site_id = preferred_edge_node_info.get(
                "site_id", "default")
            enforcementpoint_id = preferred_edge_node_info.get(
                "enforcementpoint_id", "default")
            edge_cluster_base_url = (
                EDGE_CLUSTER_URL.format(site_id, enforcementpoint_id))
            edge_cluster_id = infer_id_method(
                "edge_cluster", preferred_edge_node_info,
                edge_cluster_base_url, 'Edge Cluster')
            edge_node_base_url = EDGE_NODE_URL.format(
                site_id, enforcementpoint_id, edge_cluster_id)
            edge_node_id = infer_id_method(
                "edge_node", preferred_edge_node_info,
                edge_node_base_url, "Edge Node")
            nsx_resource_params["preferred_edge_paths"].append(
                edge_node_base_url + "/" + edge_node_id)
