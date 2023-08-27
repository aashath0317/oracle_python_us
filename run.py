import oci
import os
import time
import telethon
from telethon.sessions import StringSession
from telethon.sync import events
from telethon.sync import TelegramClient
import asyncio

api_id = 3030128
api_hash = 'cfc3885f5d2cbdbc5f10e6a643de2711'
bot_token = '5007713837:AAFAFF-zyIN7XTf_AgM3A-tdKUk6qvfdg60'

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)


async def run_code():
    config = {
        "user": "ocid1.user.oc1..aaaaaaaatgxf6qpzrvuex77bggqcqwcluqjpmie63x7rclh3ltrzql6z35oq",
        "fingerprint": "04:f6:f5:5f:90:e4:a4:d1:3e:80:f0:4b:4c:cf:4a:60",
        "key_file": "private.pem",
        "tenancy": "ocid1.tenancy.oc1..aaaaaaaazg6cbfgzyredqou3g4tjshdi2cdo5jke262qhidqzoi3qomjwtpa",
        "region": "us-phoenix-1"
    }

    instance_name = 'VPNS'
    shape = 'VM.Standard.A1.Flex'
    # availability_domain = 'vOeV:AP-SINGAPORE-1-AD-1'
    compartment_id = 'ocid1.tenancy.oc1..aaaaaaaazg6cbfgzyredqou3g4tjshdi2cdo5jke262qhidqzoi3qomjwtpa'
    image_id = 'ocid1.image.oc1.phx.aaaaaaaaa54mhccuc5s352bnkyorgplcdcy5yirlcuw3hzu4r52oi7i54otq'
    subnet_id = 'ocid1.subnet.oc1.phx.aaaaaaaakk2bava4vnzpkk2huhr2mpr7dw2sev6gsrbmetjlmhe566qq2htq'
    ssh_authorized_keys = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCA7V/Iw4XrTFpjgfv+w64XG1x+4DaIGHPqOkAKO9OrJK2rwNwu6neMoUsurs040Warq+Rd34t6q3snlmLc+tG7MlfiYPaXJ/Flj04qlcBmLcF6JTAwBO4KnVcPTjV3EnNU2Qop0Hpt7/4Q+7xTRVptqprqMRo0H3BOvv+Egz2Uo4MhZ8zFzfPPx1YcZ4E3hIZVuaMl+VAKBhnhWcHfnc7QW9Cxk8tFHKOViry6NoJFbHMpo7uObztYIJWmrOwYSQUFmtaDt2e6Lt1awcRdIML/GFaUT198SseYDW2YrxZsyhyP6OyB/3eXFdAXFEJZa0OaiqrOtEFrrDSWIFWEuIpn rsa-key-20230801'
    bootVolumeSizeInGBs = 100
    bootVolumeVpusPerGB = 10
    isPvEncryptionInTransitEnabled = True
    domains = ["LiiQ:PHX-AD-1", "LiiQ:PHX-AD-2", "LiiQ:PHX-AD-3"]
    d_change = 0
    compute_client = oci.core.ComputeClient(config)
    igroup = 1273430546
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
                availability_domain= domains[d_change],
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
          print(str(er.message))
          time.sleep(10)
          d_change = d_change+1
          if d_change == 3:
            d_change = 0
          continue

      vm = vm_response.data
      print("Created VM:", vm.id)
      message = f'Created VM:{vm.id}'
      await client.send_message(igroup, message)
      # Wait for the VM to reach the "Running" state
      compute_client.get_instance(vm.id).wait_until(
          oci.core.models.Instance.LIFECYCLE_STATE_RUNNING,
          max_wait_seconds=10
      )
      print("VM is running")
      message=("VM is running")
      await client.send_message(igroup, message)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_code())
