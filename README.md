BookVerse Golden Images
=======================

An example of a "golden images" workflow for docker images for the BookVerse demo project.


TODOs
-----

* ~~Create a project for the "global" remote repos.  Not necessary, but will help with managing the example.~~

* Create "global" remote repos for PyPi and NPM.

* Create and apply curation policies to the "global" repos.

* ~~Create a project for the "golden-images".~~

* ~~Create the "golden-images" life cycle stages (Dev and Testing?).~~
  Decided on just DEV for now.

* Create the "golden-images" life cycle gates.

  * How to do a custom rego to check for a custom evidence?  This may be a later add.

* Create separate evidence signing keys for the golden images.
  Name them so they look like they're controlled by a security team.

* ~~Create local repos for the "golden-images" life cycle stages.~~

* Enable Xray on the local repos.

* Xray Policies.

* Create the remote for "alpine" packages.  Do some curation on them.

* Create Applications for the base, pypi, and npm images.

* Create the dockerfile for the base image.  Add a fake company-root-ca cert to the image.
  Maybe add something like envoy proxy as an example security base package.

  * This will likely need to be a jinja template or similar for the example as we'll need to inject the
    Artifactory / JFrog Platform host name into the dockerfile.

  * Is there some sort of templating engine that's in the python standard lib?

* Create the dockerfile for the pypi image.  Install Python and pip.

* Create the dockerfile for the npm image.  Install NodeJS and npm.

* Create a Github Action workflow that does the following:

 * Builds the base image.

 * Pushes the base image to Artifactory.

 * Pushes the build-info to Artifactory.

 * Gets the Xray scan data.
   Fail the build if there's a policy violation.
   Add scan data as evidence (if not already done) if no violation.

 * Applies an Application version to the base image.

 * Promotes image to testing phase?

 * Promotes image to prod release.
   Should this be a separate repo that is internal to the project?  Or should the base be an available golden?

* Create a Github Action workflow, triggered from the base, that does the following:

 * Builds the pypi image.

 * Pushes the pypi image to Artifactory.

 * Pushes the build-info to Artifactory.

 * Gets the Xray scan data.
   Fail the build if there's a policy violation.
   Add scan data as evidence (if not already done) if no violation.

 * Applies an Application version to the base image.

 * Promotes image to testing phase?

 * Adds the "Golden Image" evidence to the image.

 * Promotes image to prod release.  This should be the repo that is shared outside the project.

* Create a Github Action workflow, triggered from the base, that does the following:

 * Builds the npm image.

 * Pushes the npm image to Artifactory.

 * Pushes the build-info to Artifactory.

 * Gets the Xray scan data.
   Fail the build if there's a policy violation.
   Add scan data as evidence (if not already done) if no violation.

 * Applies an Application version to the base image.

 * Promotes image to testing phase?

 * Adds the "Golden Image" evidence to the image.

 * Promotes image to prod release.  This should be the repo that is shared outside the project.
 
 * Create policy to check for the golden image chain via the AI policy generator.
