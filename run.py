import oci
import os
import time
config = {
    "user": "ocid1.user.oc1..aaaaaaaaakgvq2decbpx4rwzommac4x3g5kxuhmhsgzutgsz7ixlviazxpdq",
    "fingerprint": "00:2e:a6:27:16:43:99:3e:e6:8b:77:52:1c:61:02:10",
    "key_file": "private.pem",
    "tenancy": "ocid1.tenancy.oc1..aaaaaaaazg6cbfgzyredqou3g4tjshdi2cdo5jke262qhidqzoi3qomjwtpa",
    "region": "us-phoenix-1"
}

instance_name = 'instance-20230108-1105'
shape = 'VM.Standard.A1.Flex'
#availability_domain = 'vOeV:AP-SINGAPORE-1-AD-1'
compartment_id= 'ocid1.tenancy.oc1..aaaaaaaazg6cbfgzyredqou3g4tjshdi2cdo5jke262qhidqzoi3qomjwtpa'
image_id= 'ocid1.image.oc1.phx.aaaaaaaanyjs4d76ax5anv254rnscizcnrkfdqmvwxw7bnwpdxh2z5b2n2ia'
subnet_id = 'ocid1.subnet.oc1.phx.aaaaaaaakk2bava4vnzpkk2huhr2mpr7dw2sev6gsrbmetjlmhe566qq2htq'
ssh_authorized_keys = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDoZ/Q0o0xBgRXZDpb9eclKbg53t2cnW+yRrlftQVlZDHyZa2jg3Sl8p18tai7T2ie5r2381iHT/fBGMG+Bgm9oHEHUsYwmMqSvS8SCj8CT3Risu8KMNLDBWRqSiDzHUL7219a/qMvjCTJJ7vQBy1Mm1Y+5kdCTJ97y4eNQQcfYyWD3QTXQXBt+4jJtEtOcmRjkxCPiPsKnkxCB0IavWAJfp0p9jQIUOVTFkYZGqsvqs0R1wdWQHA9CASlRWI2etksc1cdlKfU+3v3UfwqrqS0RxTRGStbuKdYEBqjYy6bDBxKUzMDzhrakpcqAYndiBJx4n2I1Dx+mDlf8UsvVN/0V rsa-key-20230402'
bootVolumeSizeInGBs = 150
bootVolumeVpusPerGB = 10
isPvEncryptionInTransitEnabled = True
domains = ["LiiQ:PHX-AD-1","LiiQ:PHX-AD-2","LiiQ:PHX-AD-3"]
d_change = 0
compute_client = oci.core.ComputeClient(config)
while d_change <= 2 :          
  print("trying "+domains[d_change])
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
            shape_config={
            "ocpus":4,
            "memory_in_gbs":24,
            "boot_volume_size_in_gbs":100
            },
            metadata={
                "ssh_authorized_keys": ssh_authorized_keys
            },

        )
    )
  except oci.exceptions.ServiceError as er:
      print(er.message)
      time.sleep(10)
      d_change = d_change+1
      if d_change == 3:
        d_change = 0     
      continue

  vm = vm_response.data
  print("Created VM:", vm.id)
  # Wait for the VM to reach the "Running" state
  compute_client.get_instance(vm.id).wait_until(
      oci.core.models.Instance.LIFECYCLE_STATE_RUNNING,
      max_wait_seconds=10
  )
  print("VM is running")
