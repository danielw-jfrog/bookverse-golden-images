#!/usr/bin/env python3

### IMPORTS ###
import argparse
import json
import logging
import os
import sys

import urllib.request
import urllib.error
import urllib.parse

### GLOBALS ###

### FUNCTIONS ###
def make_api_request(login_data, method, path, data = None, is_data_json = True):
    # Send the request to the JFrog Artifactory API.
    req_url = "{}{}".format(login_data["host"], urllib.parse.quote(path, safe="/?=,&"))
    req_headers = {}
    req_data = None
    if is_data_json:
        req_headers["Content-Type"] = "application/json"
        req_data = json.dumps(data).encode("utf-8") if data is not None else None
    else:
        req_headers["Content-Type"] = "text/plain"
        req_data = data.encode("utf-8") if data is not None else None

    logging.debug("req_url: %s", req_url)
    logging.debug("req_headers: %s", req_headers)
    logging.debug("req_data: %s", req_data)

    req_headers["Authorization"] = "Bearer {}".format(login_data["token"])

    request = urllib.request.Request(req_url, data = req_data, headers = req_headers, method = method)
    resp = None
    try:
        with urllib.request.urlopen(request) as response:
            # Check the status and log
            # NOTE: response.status for Python >=3.9, change to response.code if Python <=3.8
            # FIXME: JSON decode the response if the content is type "application/json"
            resp = response.read().decode("utf-8")
            logging.debug("  Response Status: %d, Response Body: %s", response.status, resp)
            logging.debug("Repository operation successful")
    except urllib.error.HTTPError as ex:
        logging.warning("Error (%d) for operation", ex.code)
        logging.warning("  response body: %s", ex.read().decode("utf-8"))
        if(ex.code == 404):
            raise NotFoundException()
        else:
            raise Exception("Fail Build")
    except urllib.error.URLError as ex:
        logging.error("Request Failed (URLError): %s", ex.reason)
        raise Exception("Fail Build")
    # FIXME: Should make the status code available to the calling method.
    return resp

def create_application_version(login_data, application_key, version, version_tag, build_name, build_number, build_info_repository):
    # FIXME: Add the other options
    req_url = "/apptrust/api/v1/applications/{}/versions".format(application_key)
    req_data = {
        "version": version,
        "tag": version_tag,
        "sources": {
            "builds": [{
                "name": build_name,
                "number": build_number,
                "repository_key": build_info_repository,
                "include_dependencies": False
            }]
        }
    }
    make_api_request(login_data, 'POST', req_url, req_data)

### CLASSES ###
class NotFoundException(Exception):
    pass

### MAIN ###
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action = "store_true")
    parser.add_argument("--token", default = os.getenv("JFROG_ACCESS_TOKEN", ""),
                        help = "Artifactory access token to use for requests.  Will use JFROG_ACCESS_TOKEN if not specified.")
    parser.add_argument("--host", default = os.getenv("JFROG_URL", ""),
                        help = "Artifactory host URL (e.g. https://artifactory.example.com/) to use for requests.  Will use JFROG_URL if not specified.")

    parser.add_argument("--project_key", default = os.getenv("PROJECT_KEY", None),
                        help = "Short version of the project name used for identifying the project.")

    parser.add_argument("--build_name", default = os.getenv("BUILD_NAME", None),
                        help = "The name of the build used to create the application version.")
    parser.add_argument("--build_number", default = os.getenv("BUILD_NUMBER", None),
                        help = "The number of the build used to create the application version.")

    parser.add_argument("application_key")
    parser.add_argument("application_version")

    args = parser.parse_args()

    # Set up logging
    logging.basicConfig(
        format = "%(asctime)s:%(levelname)s:%(name)s:%(funcName)s: %(message)s",
        level = logging.DEBUG if args.verbose else logging.INFO
    )
    logging.debug("Args: %s", args)

    tmp_login_data = {}
    tmp_login_data["token"] = args.token
    tmp_login_data["host"] = args.host

    project_key = str(args.project_key)
    app_key = str(args.application_key)
    app_version = str(args.application_version)

    try:
        logging.info("Creating Application Version: %s - %s", app_key, app_version)
        create_application_version(
            tmp_login_data,
            app_key,
            app_version,
            "release",
            args.build_name,
            args.build_number,
            "{}-build-info".format(project_key)
        )
    except Exception as ex:
        logging.error(ex)
        sys.exit(1)

if __name__ == "__main__":
    main()

