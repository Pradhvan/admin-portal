import dramatiq

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
console = logging.StreamHandler()
logger.addHandler(console)


@dramatiq.actor
def process_log(domain):
    from .workers import SiteCheckLogger

    check_logger = SiteCheckLogger()

    logger.debug(f"logging a check for {domain}")
    if domain is not None:
        check_logger.log_sitecheck_for_domain(domain)