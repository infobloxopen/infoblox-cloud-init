# infoblox-cloud-init
opensource cloud-init project 

Cloud-init is the industry standard multi-distribution method for cross-platform cloud instance initialization. It issupported across all major public cloud providers,  provisioning systems for private cloud infrastructure, and bare-metal installations. Cloud instances are initialized from a disk image and instance data:

•  Cloud metadata
•  User data (optional)
•  Vendor data (optional)

Cloud-init will identify the cloud it is running on during boot, read any provided metadata from the cloud and initializethe system accordingly.  This may involve setting up the network and storage devices to configuring SSH access keyand many other aspects of a system.  Later on the cloud-init will also parse and process any optional user or vendordata that was passed to the instance.
