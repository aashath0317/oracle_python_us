import oci
# Create a client for the Compute Cloud API
config = {
    "user": "ocid1.user.oc1..aaaaaaaaul4cbqzowr4x5bnmsdmlqpo3onbs2ekwqb55yhnbh3izmksgr5ha",
    "fingerprint": "4a:d4:ae:62:e3:29:bc:a6:0c:c9:b6:55:7a:f7:ba:a9",
    "key_file": "oci_private.pem",
    "tenancy": "ocid1.tenancy.oc1..aaaaaaaasnvm3ufpikguqeurze3z6ek5pgbsg2uiqtkfqha5qxplzbqqbm5a",
    "region": "ap-singapore-1",
    "compartment_id": "ocid1.tenancy.oc1..aaaaaaaasnvm3ufpikguqeurze3z6ek5pgbsg2uiqtkfqha5qxplzbqqbm5a"
}
compute_client = oci.core.ComputeClient(config)
# List the available images
images = compute_client.list_images(compartment_id).data

# Print the image IDs and names
for image in images:
  print("ID:", image.id)
  print("Name:", image.display_name)
