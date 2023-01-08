import oci
import os
import time
config = {
    "user": "ocid1.user.oc1..aaaaaaaaakgvq2decbpx4rwzommac4x3g5kxuhmhsgzutgsz7ixlviazxpdq",
    "fingerprint": "00:2e:a6:27:16:43:99:3e:e6:8b:77:52:1c:61:02:10",
    "key_file": "oci_private.pem",
    "tenancy": "ocid1.tenancy.oc1..aaaaaaaazg6cbfgzyredqou3g4tjshdi2cdo5jke262qhidqzoi3qomjwtpa",
    "region": "us-phoenix-1"
}

instance_name = 'instance-20230108-1105'
shape = 'VM.Standard.A1.Flex'
#availability_domain = 'vOeV:AP-SINGAPORE-1-AD-1'
compartment_id= 'ocid1.tenancy.oc1..aaaaaaaazg6cbfgzyredqou3g4tjshdi2cdo5jke262qhidqzoi3qomjwtpa'
image_id= 'ocid1.image.oc1.phx.aaaaaaaanyjs4d76ax5anv254rnscizcnrkfdqmvwxw7bnwpdxh2z5b2n2ia'
subnet_id = 'ocid1.subnet.oc1.phx.aaaaaaaakk2bava4vnzpkk2huhr2mpr7dw2sev6gsrbmetjlmhe566qq2htq'
ssh_authorized_keys = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCIp9Tq+a9hUL796nCKtPpoE9LBxbRAxknuExUImZv0Nn+4Mq2knSCtStqoOlrt8ta2eBsVsm0lRR3dkbNrWeDsk25tHonBkhvD9ltDKz7JfqkhaWmnGiVsMX0xqcj+L4EzbjcmwPQ0PV4Vb9SvpWgY7VkCtvnTykPAm4wloe9FfZrhN/ZvpTjOc1O+kyaMHi+e8kbk1B+BeqbVZrNwCyEfdIPz5Ykb+G9oEoagnrrCzMF1usxLAQ3hIq4A6ex9w6e9hUASK7yi4aGUFXzX4M9By8WlE5SihqVs+kepPTau2DPpmcqTdmOerFgkFAXNvU0IvJdlvTMDPp8AyaqNy9P5 rsa-key-20230108'
bootVolumeSizeInGBs = 100
bootVolumeVpusPerGB = 10
isPvEncryptionInTransitEnabled = True

compute_client = oci.core.ComputeClient(config)
while True:
  # Create a VM
  try:  
    vm_response = compute_client.launch_instance(
        oci.core.models.LaunchInstanceDetails(
            compartment_id=compartment_id,
            display_name = instance_name,
            image_id=image_id,
            shape=shape,
            subnet_id=subnet_id,
            availability_domain='LiiQ:PHX-AD-3',
            is_pv_encryption_in_transit_enabled=True,
            bootVolumeSizeInGBs = 100,
            ocpus=4,
            memoryInGBs=24,
            metadata={
                "ssh_authorized_keys": ssh_authorized_keys
            }
        )
    )
  except oci.exceptions.ServiceError as er:
      print(er.message)
      print("waiting for 10s")
      time.sleep(10)
      continue
  
  vm = vm_response.data
  print("Created VM:", vm.id)
  # Wait for the VM to reach the "Running" state
  compute_client.get_instance(vm.id).wait_until(
      oci.core.models.Instance.LIFECYCLE_STATE_RUNNING,
      max_wait_seconds=10
  )
  print("VM is running")
