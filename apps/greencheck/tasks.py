import logging

import dateutil.parser as date_parser
import dramatiq
import MySQLdb

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# console = logging.StreamHandler()
# logger.addHandler(console)


@dramatiq.actor
def process_log(domain):
    from .workers import SiteCheckLogger

    check_logger = SiteCheckLogger()

    logger.debug(f"logging a check for {domain}")
    if domain is not None:
        try:
            check_logger.log_sitecheck_for_domain(domain)
        except MySQLdb.OperationalError as err:
            logger.warning(
                (
                    f"Problem reported by the database when trying to "
                    f"log domain: {domain}"
                )
            )
            logger.warning(err)
            return False
        except Exception as err:
            logger.exception(err)
            return False


@dramatiq.actor(queue_name="stats")
def create_stat_async(date_string: str = None, query_name: str = "total_count", *args):
    """
    Accept a date_string, and a query name then execute the query. Used to carry out
    expensive aggregation queries outside the request cycle.
    """

    from .models.stats import DailyStat

    allowed_queries = [
        "total_count",
        "total_count_for_providers",
        "top_domains_for_day",
        "top_hosting_providers_for_day",
    ]

    if query_name not in allowed_queries:
        raise Exception("Unsupported query. Ignoring")

    parsed_date = date_parser.parse(date_string)

    query_function = getattr(DailyStat, query_name)
    query_function(date_to_check=parsed_date)

