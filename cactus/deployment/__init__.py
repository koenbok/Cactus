#coding:utf-8
import logging


logger = logging.getLogger(__name__)


PROVIDER_MAPPING = {
    "rackspace": "cactus.deployment.cloudfiles.engine.CloudFilesDeploymentEngine",
    "google": "cactus.deployment.gcs.engine.GCSDeploymentEngine",
    "aws": "cactus.deployment.s3.engine.S3DeploymentEngine",
    "neocities": "cactus.deployment.neocities.engine.NeocitiesDeploymentEngine",
}


def get_deployment_engine_class(provider):
    """
    Import an engine by name
    :provider: The provider you want to deploy to
    :type provider: str
    :returns: The deployment Engine
    :rtype: cactus.deployment.engine.BaseDeploymentEngine
    """
    engine_path = PROVIDER_MAPPING.get(provider, None)
    logger.debug("Loading Deployment Engine for %s: %s", provider, engine_path)

    if engine_path is None:
        return None

    module, engine = engine_path.rsplit(".", 1)

    try:
        _mod = __import__(module, fromlist=[engine])
    except ImportError as e:
        logger.error("Unable to import requested engine (%s) for provider %s", engine, provider)
        logger.error("A required library was missing: %s", e.message)
        logger.error("Please install the library and try again")
    else:
        return getattr(_mod, engine)
