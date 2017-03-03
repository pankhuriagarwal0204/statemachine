#!/usr/bin/python

import base
from fetch_data import models
import logging


def main():
    # models.Event.objects.all().delete()
    # logging.info("Deleted data from truth")
    models.Intrusion.objects.all().delete()
    # logging.info("Deleted extracted data from truth")

if __name__ == '__main__':
    logging.basicConfig(filemode='w', level=logging.INFO,
                        format="%(asctime)s %(process)d %(levelname)s "
                               "[%(name)s:%(funcName)s:%(lineno)d] %(message)s")
    main()