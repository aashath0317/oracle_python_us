import oci
compartmentId= 'ocid1.tenancy.oc1..aaaaaaaasnvm3ufpikguqeurze3z6ek5pgbsg2uiqtkfqha5qxplzbqqbm5a'
# Create a client for the Compute Cloud API
compute_client = oci.core.ComputeClient(config)

# List the available images
images = compute_client.list_images(compartment_id).data

# Print the image IDs and names
for image in images:
  print("ID:", image.id)
  print("Name:", image.display_name)