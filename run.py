import oci
availability_domain = 'vOeV:AP-SINGAPORE-1-AD-1'
region= 'ap-singapore-1'
tenancy= 'ocid1.tenancy.oc1..aaaaaaaasnvm3ufpikguqeurze3z6ek5pgbsg2uiqtkfqha5qxplzbqqbm5a'
compartmentId= 'ocid1.tenancy.oc1..aaaaaaaasnvm3ufpikguqeurze3z6ek5pgbsg2uiqtkfqha5qxplzbqqbm5a'
image_id= '
# Create a client for the Compute Cloud API
compute_client = oci.core.ComputeClient(config)

while True:
  # Create a VM
  vm_response = compute_client.launch_instance(
      oci.core.models.LaunchInstanceDetails(
          compartment_id=compartment_id,
          display_name="My VM",
          image_id=image_id,
          shape="VM.Standard.E2.1.Micro",
          subnet_id=subnet_id,
          availability_domain=availability_domain,
          is_pv_encryption_in_transit_enabled=True,
          metadata={
              "ssh_authorized_keys": ssh_authorized_keys
          }
      )
  )
  vm = vm_response.data
  print("Created VM:", vm.id)
 
  # Wait for the VM to reach the "Running" state
  compute_client.get_instance(vm.id).wait_until(
      oci.core.models.Instance.LIFECYCLE_STATE_RUNNING,
      max_wait_seconds=10
  )
  print("VM is running")
 ''' 
  # Do some work here...
  
  # Terminate the VM
  compute_client.terminate_instance(vm.id)
  print("Terminated VM:", vm.id)
'''
