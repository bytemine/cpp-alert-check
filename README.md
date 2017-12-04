# cpp-alert-check

## About

Icinga check to read alerts from a crashplan pro server. it uses the
CrashPlan API to fetch alerts and uses the most recent one for status
(WARNING or CRITICAL) and message. Alerts can be acknowledged in the 
CrashPlan administrator panel. If only acknowledged alerts are present,
the check will succeed with status OK.
If the check can't read the data from the CrashPlan API, it will exit
with status UNKNOWN and print the message of the python exception.

## Installation

### Requirements

- python 2.7
- virtualenv has to be installed to generate the pex file or for manual setup.
  It usually is available for installation using packages of the distribution.

### Setup

#### pex

To create a pex file, just run `make pex/cpp_alert_check.pex`. It will

- create a virtualenv and install pex into it
- use the installed pex to create a pex, which is dropped to ./pex/cpp\_alert\_check.pex

#### Manual setup

Put the contents of this directory somewhere, then run:

    virtualenv venv
    . venv/bin/activate
    pip install -r requirements.txt

This will install the python dependencies into the virtual environment.


## Calling the check

To run the check, either use cpp\_alert\_check.pex which should work out of the box when
executed. if running with manual installation, this line should work:

	. venv/bin/activate && python -m cpp_alert_check.cpp_alert_check

#### Parameters

<table>
<tr><th>Parameter</th> <th>Description</th></tr>
<tr><td><code>-h, --help</code></td> <td>show this help message and exit</td></tr>
<tr><td><code>-V, --version</code></td> <td>display the version and exit</td></tr>
<tr><td><code>-l LOGIN, --login LOGIN</code></td> <td>username used for basic auth</td></tr>
<tr><td><code>-p PASSWORD, --password PASSWORD</code></td><td>password used for basic auth</td></tr>
<tr><td><code>-u URL, --url URL</code></td><td>base url of the CrashPlan instance</td></tr>
<tr><td><code>--no-verify</code></td><td>ignore invalid SSL certificate chains</td></tr>
</table>

#### Examples

If the CrashPlan instance is reachable at https://cpp.example.com:1234 a call
would look like this:

	./cpp_alert_check.pex -u https://cpp.example.com:1234 -l username -p password

To accept "invalid" SSL certificate chains (for example self-signed) use the `--no-verify` switch:

    ./cpp-alert-check.pex -u https://cpp.example.com:1234 -l username -p password --no-verify

