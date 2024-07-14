#!/usr/bin/env python3
import os
from azure.mgmt.compute import ComputeManagementClient
from azure.identity import DefaultAzureCredential

import automationassets

subscription_id = automationassets.get_automation_variable("AZURE_SUBSCRIPTION_ID")
resource_group = automationassets.get_automation_variable('RESOURCE_GROUP_NAME')
vmss_name = automationassets.get_automation_variable('VMSS_NAME')

credential = DefaultAzureCredential()
compute_client = ComputeManagementClient(credential, subscription_id)

def scale_out_vmss(resource_group, vmss_name, instance_count):
    vmss = compute_client.virtual_machine_scale_sets.get(resource_group, vmss_name)
    vmss.sku.capacity = instance_count
    async_vmss_update = compute_client.virtual_machine_scale_sets.begin_create_or_update(
        resource_group_name=resource_group,
        vm_scale_set_name=vmss_name,
        parameters=vmss
    )
    async_vmss_update.wait()
    print(f'Scaled out VMSS to {instance_count} instances')

current_instance_count = compute_client.virtual_machine_scale_sets.get(resource_group, vmss_name).sku.capacity
new_instance_count = current_instance_count + 1

scale_out_vmss(resource_group, vmss_name, new_instance_count)
