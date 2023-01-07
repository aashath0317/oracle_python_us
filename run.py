import oci
config = {
    "user": "ocid1.user.oc1..aaaaaaaaul4cbqzowr4x5bnmsdmlqpo3onbs2ekwqb55yhnbh3izmksgr5ha",
    "fingerprint": "4a:d4:ae:62:e3:29:bc:a6:0c:c9:b6:55:7a:f7:ba:a9",
    "key_file": "oci_private.pem",
    "tenancy": "ocid1.tenancy.oc1..aaaaaaaasnvm3ufpikguqeurze3z6ek5pgbsg2uiqtkfqha5qxplzbqqbm5a",
    "region": "ap-singapore-1"
}
instance_name = ''
shape = ''
availability_domain = 'vOeV:AP-SINGAPORE-1-AD-1'
compartment_id= 'ocid1.tenancy.oc1..aaaaaaaasnvm3ufpikguqeurze3z6ek5pgbsg2uiqtkfqha5qxplzbqqbm5a'
image_id= 'ocid1.image.oc1.ap-singapore-1.aaaaaaaav2nfrctnfspilj3ueob37g2yljyr7lhv663mpargajcunyqzjnla'
compute_client = oci.core.ComputeClient(config)
subnet_id = 'ocid1.vcn.oc1.ap-singapore-1.amaaaaaat3xrswia6uzcrxayg4hlmxiwmabdn7rjiliqfcbwkerg32eptoua'
ssh_authorized_keys = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCxs3qA5wRuR2UdQdcU4hgI2OmOko4rtT2vWS5SXWZCHemUJLHya5YAq2nnn9wOA3V9mgBDUYkyui+tB/56lR7wipkUUeJeIcbgSMk7/ZRAd+4XCZP93QWhj0Jh+tBaOOjrV04s4O8oQs0Vfvjs11FkAhITcc8EhkPIiAsDhirdY3EbThP3iGOrQUGoOsTSHAOi09MOROd/ecNXdfYVCot9tEdRpydsRHhchs7pkvY0px+n85V964bYuElwVOec+h2N68eqG8+sdmrJYEccxiaC6ezA9EnGETFdH89mfgVjZ3U+SxppisnxtmFxPaqncZQ2QqK6qeLN1jdUeR1PR/qn rsa-key-20230107'


while True:
  # Create a VM
  vm_response = compute_client.launch_instance(
      oci.core.models.LaunchInstanceDetails(
          compartment_id=compartment_id,
          display_name = instance_name,
          image_id=image_id,
          shape=shape,
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
