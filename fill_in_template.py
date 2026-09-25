#!/usr/bin/env python3

### IMPORTS ###
import argparse
import logging
import pathlib
import os
import sys

from jinja2 import Environment, FileSystemLoader, select_autoescape

### GLOBALS ###

### FUNCTIONS ###

### CLASSES ###

### MAIN ###
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action = "store_true")
    parser.add_argument("--host", default = os.getenv("JFROG_URL", ""),
                        help = "Artifactory host URL (e.g. https://artifactory.example.com/) to use for requests.  Will use JFROG_URL if not specified.")

    parser.add_argument("--template-from-repo", default = os.getenv("TEMPLATE_FROM_REPO", ""),
                        help = "Repository in Artifactory to put into the FROM value in templates.")
    parser.add_argument("--template-from-image", default=os.getenv("TEMPLATE_FROM_IMAGE", ""),
                        help="Image Name to put into the FROM value in templates.")
    parser.add_argument("--template-from-tag", default=os.getenv("TEMPLATE_FROM_TAG", ""),
                        help="Image Tag to put into the FROM value in templates.")

    parser.add_argument("template", help = "The filename of the template that should be processed.")

    args = parser.parse_args()

    # Set up logging
    logging.basicConfig(
        format = "%(asctime)s:%(levelname)s:%(name)s:%(funcName)s: %(message)s",
        level = logging.DEBUG if args.verbose else logging.INFO
    )
    logging.debug("Args: %s", args)

    template_filename = pathlib.Path(args.template)

    if args.host is None:
        logging.error("No host set")
        sys.exit(1)
    template_host = str(args.host)
    template_host = template_host.replace('http://', '')
    template_host = template_host.replace('https://', '')

    if args.template_from_repo is None:
        logging.error("No repo set")
        sys.exit(1)
    template_from_repo = str(args.template_from_repo)

    if args.template_from_image is None:
        logging.error("No image name set")
        sys.exit(1)
    template_from_image = str(args.template_from_image)

    if args.template_from_tag is None:
        logging.error("No image tag set")
        sys.exit(1)
    template_from_tag = str(args.template_from_tag)

    jinja_env = Environment(
        loader = FileSystemLoader(template_filename.parent),
        autoescape = select_autoescape()
    )

    jinja_temp = jinja_env.get_template(template_filename.name)

    jinja_out = jinja_temp.render(
        host = template_host,
        repo = template_from_repo,
        image_name = template_from_image,
        image_tag = template_from_tag
    )

    with open(template_filename.stem, 'w') as tf:
        tf.write(jinja_out)

if __name__ == '__main__':
    main()
