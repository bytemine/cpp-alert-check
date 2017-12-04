import argparse
import sys
import urllib3
import requests
import requests.compat
import requests.auth

VERSION = "0.0.2"

ICINGA_OK = 0
ICINGA_WARNING = 1
ICINGA_CRITICAL = 2
ICINGA_UNKNOWN = 3

SRT_KEY_SERVER = "server"
SRT_KEY_TYPE = "type"
SRT_KEY_STATUS = "status"
SRT_KEY_SEVERITY = "severity"
SRT_KEY_TIMESTAMP = "timestamp"

SRT_DIR_ASC = "asc"
SRT_DIR_DESC = "desc"

STATUS_NEW = "NEW"
STATUS_ARCHIVED = "ARCHIVED"

TYPE_ADMIN_PASSWORD_UNCHANGED = "ADMIN_PASSWORD_UNCHANGED"
TYPE_DATABASE_EXPORT = "DATABASE_EXPORT"
TYPE_DATABASE_IMPORT_BACKUP = "DATABASE_IMPORT_BACKUP"
TYPE_DEMO_EXPIRED = "DEMO_EXPIRED"
TYPE_DESTINATION_OFFLINE = "DESTINATION_OFFLINE"
TYPE_DIRECTORY_SYNC_DEACTIVATE = "DIRECTORY_SYNC_DEACTIVATE"
TYPE_EMAIL_CONNECTION = "EMAIL_CONNECTION"
TYPE_EMAIL_EXPIRED = "EMAIL_EXPIRED"
TYPE_JOB_FAILED = "JOB_FAILED"
TYPE_LDAP_CONNECTION = "LDAP_CONNECTION"
TYPE_RADIUS_CONNECTION = "RADIUS_CONNECTION"
TYPE_SERVER_OFFLINE = "SERVER_OFFLINE"
TYPE_SERVER_OUTOFDATE = "SERVER_OUTOFDATE"
TYPE_CORRUPT_ARCHIVE = "CORRUPT_ARCHIVE"
TYPE_STORE_POINT_OFFLINE = "STORE_POINT_OFFLINE"
TYPE_STORE_POINT_SPACE_WARNING = "STORE_POINT_SPACE_WARNING"
TYPE_STORE_POINT_SPACE_CRITICAL = "STORE_POINT_SPACE_CRITICAL"
TYPE_SUPPORT_EXPIRED = "SUPPORT_EXPIRED"
TYPE_ALERT_RECIPIENTS_MISSING = "ALERT_RECIPIENTS_MISSING"
TYPE_DEVICE_BACKUP_WARNING = "DEVICE_BACKUP_WARNING"
TYPE_DEVICE_BACKUP_CRITICAL = "DEVICE_BACKUP_CRITICAL"
TYPE_LOCATOR_SERVICE_OVERLOADED = "LOCATOR_SERVICE_OVERLOADED"
TYPE_SSO_IDENTITY_PROVIDER_REMOVED_WHEN_IN_USE = "SSO_IDENTITY_PROVIDER_REMOVED_WHEN_IN_USE"
TYPE_SSO_IDENTITY_PROVIDER_FAILED_USER_ATTRIBUTE_MAPPING = "SSO_IDENTITY_PROVIDER_FAILED_USER_ATTRIBUTE_MAPPING"
TYPE_SSO_IDENTITY_PROVIDER_DOES_NOT_SUPPORT_HTTP_POST = "SSO_IDENTITY_PROVIDER_DOES_NOT_SUPPORT_HTTP_POST"
TYPE_SSO_METADATA_URL_UNAVAILABLE = "SSO_METADATA_URL_UNAVAILABLE"
TYPE_SSO_METADATA_NOT_PARSABLE = "SSO_METADATA_NOT_PARSABLE"
TYPE_APPLICATION_REVOKED_FROM_DESTINATION = "APPLICATION_REVOKED_FROM_DESTINATION"
TYPE_LICENSE_UPDATE_FAILURE = "LICENSE_UPDATE_FAILURE"

EXPORT_CSV = "csv"

class C42(object):
    def __init__(self, baseurl, user, password, verify=True):
        """Creates a new C42 API client.

        :param baseurl: URL of the CPP instance like https://cpp.example.org/ .
        :param user: username to use with basic auth.
        :param password: password to use with basic auth.
        :param verify: (optional) Boolean to control SSL verification. Defaults to ``True``
        """
        self.baseurl = baseurl
        self.user = user
        self.password = password
        self.verify = verify

    def _url(self, path):
        return requests.compat.urljoin(self.baseurl, path)

    def get_alerts(self, srt_key=None, srt_dir=None, status=None, typ=None, export=None, pg_size=None, pg_num=None):
        """Get alert log entries.

        :param srt_key: (Optional) Key to sort the returned results by, can be one of the SRT_KEY_* values.
        :param srt_dir: (Optional) Sorting direction, can be one of the SRT_DIR_* values.
        :param status: (Optional) Only return alerts with this status, can be one of the STATUS_* values.
        :param typ: (Optional) Only return alerts of this type, can be one of the TYPE_* values.
        :param export: (Optional) Specifies an export, can be EXPORT_CSV .
        :param pg_size: (Optional) Number of alerts on one page, integer.
        :param pg_num: (Optional) Page number to query, interger.
        :return: list of dict describing alerts.
        """

        params = {"srtKey": srt_key, "srtDir": srt_dir, "status": status, "type": typ, "export":export, "pgSize": pg_size, "pgNum": pg_num}
        res = requests.get(self._url("/api/alertLog"), params=params, auth=requests.auth.HTTPBasicAuth(self.user, self.password), verify=self.verify)

        return res.json()["data"]["log"]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-V", "--version", action="store_true", help="display the version and exit")
    parser.add_argument("-l", "--login", help="username used for basic auth")
    parser.add_argument("-p", "--password", help="password used for basic auth")
    parser.add_argument("-u", "--url", help="base url of the CrashPlan instance")
    parser.add_argument("--no-verify", dest="verify", action="store_false", help="ignore invalid SSL certificate chains")
    parser.set_defaults(verify=True)
    args = parser.parse_args()

    if args.version:
        print VERSION
        sys.exit(0)

    if args.verify == False:
        # suppress warnings about unsecure connection when using --no-verify
        urllib3.disable_warnings()

    c = C42(args.url, args.login, args.password, args.verify)
    try:
        alerts = c.get_alerts(srt_key=SRT_KEY_SEVERITY, srt_dir=SRT_DIR_DESC, status=STATUS_NEW)
    except Exception, exc:
        print "Failed to get alerts from API: " + str(exc)
        sys.exit(ICINGA_UNKNOWN)

    if len(alerts) < 1:
        print "No alerts."
        sys.exit(ICINGA_OK)

    severity = alerts[0]["severity"]
    msg = "{type} {info}".format(type=alerts[0]["type"], info=", ".join([ "{}: {}".format(x, alerts[0]["infoMap"][x]) for x in alerts[0]["infoMap"].keys()]))
    print msg
    if severity == "CRITICAL":
        sys.exit(ICINGA_CRITICAL)
    elif severity == "WARNING":
        sys.exit(ICINGA_WARNING)
    elif severity == "NORMAL":
        sys.exit(ICINGA_OK)
    
    sys.exit(ICINGA_UNKNOWN)

if __name__ == "__main__":
    main()
