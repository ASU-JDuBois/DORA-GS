# DORA-GS
Code for DORA groundstation
Dora_data_upload.py will make a URL to upload demodulated DORA data.
when you run the file, it will ask for:
obsservation number
the time you started the demod, this is used to calculate a more accurate time for the data
when it asks for the data, this should be input in 3 lines, the formated time line (including brackets and DORA), the data and a blank line. Multiple data sets from the same observation can be input. type end to complete your input.
This script will query the observation to determine the time and the lat and lon of the observation.

This script requires the Python Library: requests
use pip to install requests
if you don't have pip, you must install it first

to install pip:
This depends on your operating system. A Python environment is highly recommended.
https://pip.pypa.io/en/stable/installation/

to install requests:
pip install requests

https://www.activestate.com/resources/quick-reads/how-to-pip-install-requests-python-package/
