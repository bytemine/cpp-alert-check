_DISTNAME := bytemine-cpp-alert-check

# this needs to be called with a VERSION, e.g. 
# VERSION=$(pex/cpp-alert-check.pex -V) make distfile
distfile: pex/cpp-alert-check.pex
	mkdir -p /tmp/$(_DISTNAME)-$(VERSION)
	cp README.md pex/cpp-alert-check.pex /tmp/$(_DISTNAME)-$(VERSION)
	cd /tmp && tar cvzf $(_DISTNAME)-$(VERSION).tgz $(_DISTNAME)-$(VERSION)
	sha256sum /tmp/$(_DISTNAME)-$(VERSION).tgz

pex/cpp-alert-check.pex: requirements.txt cpp_alert_check/cpp_alert_check.py setup.py venv-pex
	mkdir -p pex
	. venv-pex/bin/activate && pex . --disable-cache -r requirements.txt -m cpp_alert_check.cpp_alert_check -o pex/cpp-alert-check.pex && deactivate

venv-pex:
	virtualenv venv-pex
	. venv-pex/bin/activate && pip install pex

clean:
	rm -rf pex
	rm -rf venv-pex
