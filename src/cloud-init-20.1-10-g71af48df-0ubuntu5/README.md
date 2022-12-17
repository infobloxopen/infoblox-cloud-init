# infoblox-cloud-init
opensource cloud-init project

Cloud-init is the industry standard multi-distribution method for cross-platform cloud instance initialization. It issupported across all major public cloud providers,  provisioning systems for private cloud infrastructure, and bare-metal installations. Cloud instances are initialized from a disk image and instance data:

•  Cloud metadata
•  User data (optional)
•  Vendor data (optional)

Cloud-init will identify the cloud it is running on during boot, read any provided metadata from the cloud and initializethe system accordingly.  This may involve setting up the network and storage devices to configuring SSH access keyand many other aspects of a system.  Later on the cloud-init will also parse and process any optional user or vendordata that was passed to the instance.

The files we are opensouring as part of the infoblox cloud-init project is given below

DataSourceIBAzure.py
DataSourceIBGCE.py
DataSourceIBOracle.py
DataSourceIBOVF.py

The above files are from the infoblox cloud-init source code where we are currently using a modified version of the OpenSource Azure and GCP platform files. Hence we are opensouring these files to satisfy the GNU GPL license recommendations. There is no separate installation or specific configuration is needed inorder to support these cloud platforms and by default as part of infoblox NIOS product installation these platforms will be auto configured during initial system bootup.
