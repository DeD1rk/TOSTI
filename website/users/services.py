from urllib.parse import urlencode, urlparse, parse_qsl
import requests
from django.conf import settings
import re

from django.urls import reverse


def get_openid_verifier(request):
    """
    Get an OpenID verifier object with the openid settings set to the ones specified in the django settings file.

    :param request: the request
    :return: an OpenID verifier object
    """
    return OpenIDVerifier(
        settings.OPENID_SERVER_ENDPOINT,
        request,
        settings.OPENID_RETURN_URL,
        settings.OPENID_USERNAME_PREFIX,
        settings.OPENID_USERNAME_POSTFIX,
    )


class OpenIDVerifier:
    """Object used for OpenID verification."""

    def __init__(
        self, openid_server_endpoint, request, openid_return_url, prefix, postfix
    ):
        """
        Initialise an OpenIDVerifier object.

        :param openid_server_endpoint: the OpenID server endpoint as https://[server_name]/[endpoint_location]
        :param request: the request
        :param openid_return_url: the URL that OpenID has to redirect the authenticated user to
        :param prefix: the prefix before the OpenID username
        :param postfix: the postfix after the OpenID username
        """
        self.openid_server_endpoint = openid_server_endpoint
        self.openid_trust_root = request.META["HTTP_HOST"]
        self.openid_return_url = request.build_absolute_uri(reverse(openid_return_url))
        self.prefix = prefix
        self.postfix = postfix
        self.query_parameters = dict(parse_qsl(urlparse(request.get_full_path()).query))
        self.signed_field_values = dict()
        if "openid.signed" in self.query_parameters.keys():
            for field in self.query_parameters["openid.signed"].split(","):
                if field != "mode":
                    self.signed_field_values[
                        "openid.{}".format(field)
                    ] = self.query_parameters["openid.{}".format(field)]

    def get_request_url(self, username):
        """
        Get the OpenID request URL.

        :param username: the identity that the user wants to use for identifying against the OpenID identity server
        :return: the OpenID request URL with the formatted parameters
        """
        parameters = {
            "openid.mode": "checkid_setup",
            "openid.sreg.required": "fullname,email",
            "openid.identity": self.get_full_user_id(username),
            "openid.return_to": self.openid_return_url,
            "openid.trust_root": self.openid_trust_root,
        }
        return "{}?{}".format(self.openid_server_endpoint, urlencode(parameters))

    def get_full_user_id(self, username):
        """
        Get the full user id for the OpenID server.

        This is the reverse of extract_username
        :param username: the username of the user
        :return: the full username for the OpenID server, a formatted string with the prefix and postfix specified in
        settings
        """
        return "{}{}{}".format(self.prefix, username, self.postfix)

    def extract_username(self):
        """
        Get the username from the OpenID full username.

        This is the reverse of get_full_user_id
        :return: the username of the user in the full OpenID username
        """
        if "openid.identity" in self.query_parameters.keys():
            openid_identity = self.query_parameters["openid.identity"]
            return re.sub(
                "{}$".format(self.postfix),
                "",
                re.sub("^{}".format(self.prefix), "", openid_identity),
            )
        return False

    def extract_full_name(self):
        """
        Get the full name from the query parameters.

        :return: the full name of the user if it exists, False otherwise
        """
        if "openid.sreg.fullname" in self.query_parameters.keys():
            return self.query_parameters["openid.sreg.fullname"]
        return False

    def extract_email_address(self):
        """
        Get the email from the query parameters.

        :return: the email address of the user if it exists, False otherwise
        """
        if "openid.sreg.email" in self.query_parameters.keys():
            return self.query_parameters["openid.sreg.email"]
        return False

    def get_verification_url(self):
        """
        Create a verification url for verifying an OpenID.

        :return: a string with the verification URL
        """
        keys = self.query_parameters.keys()
        if not (
            "openid.mode" in keys
            and "openid.assoc_handle" in keys
            and "openid.sig" in keys
            and "openid.signed" in keys
        ):
            return False

        parameters = {
            "openid.mode": "check_authentication",
            "openid.assoc_handle": self.query_parameters["openid.assoc_handle"],
            "openid.sig": self.query_parameters["openid.sig"],
            "openid.signed": self.query_parameters["openid.signed"],
        }

        parameters = {**parameters, **self.signed_field_values}

        return "{}?{}".format(self.openid_server_endpoint, urlencode(parameters))

    def verify_request(self):
        """
        Verify a request send by an OpenID server.

        :return: the username if the verification succeeded, False otherwise
        """
        return (
            "openid.mode" in self.query_parameters.keys()
            and self.query_parameters["openid.mode"] == "id_res"
            and self.verify_signature()
        )

    def verify_signature(self):
        """
        Verify a signature send by an OpenID server.

        :return: the username if the verification succeeded, False otherwise
        """
        verification_url = self.get_verification_url()
        response = requests.get(verification_url)
        return (
            response.status_code == 200
            and re.sub("is_valid:", "", re.sub("\n", "", response.text)) == "true"
        )
