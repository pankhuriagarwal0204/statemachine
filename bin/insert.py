#!/usr/bin/python

import base
from fetch_data import models
import logging


def main():
    geospace_1 = models.Geospace(latitude=32.45777715387119, longitude=75.12176513671876)
    geospace_1.save()
    geospace_2 = models.Geospace(latitude=32.476315491147616, longitude=75.11077880859376)
    geospace_2.save()
    geospace_3 = models.Geospace(latitude=32.48239755141864, longitude=75.09223937988283)
    geospace_3.save()
    geospace_4 = models.Geospace(latitude=32.48963756347198, longitude=75.07593154907228)
    geospace_4.save()
    geospace_5 = models.Geospace(latitude=32.49398129108325, longitude=75.05395889282228)
    geospace_5.save()
    geospace_6 = models.Geospace(latitude=32.49164656356051, longitude=75.12032043188812)
    geospace_6.save()

    battalion_1 = models.Battalion(name='battalion1', geospace=geospace_1)
    battalion_1.save()

    post_1 = models.Post(name='post1', geospace=geospace_6, battalion=battalion_1)
    post_1.save()

    morcha_1 = models.Morcha(name='Morcha-111', geospace=geospace_1, post=post_1, repr='qrt1')
    morcha_1.save()
    morcha_2 = models.Morcha(name='Morcha-242', geospace=geospace_2, post=post_1, repr='qrt2')
    morcha_2.save()
    morcha_3 = models.Morcha(name='Morcha-345', geospace=geospace_3, post=post_1, repr='qrt3')
    morcha_3.save()
    morcha_4 = models.Morcha(name='Morcha-563', geospace=geospace_4, post=post_1, repr='qrt4')
    morcha_4.save()
    morcha_5 = models.Morcha(name='Morcha-123', geospace=geospace_5, post=post_1, repr='qrt5')
    morcha_5.save()


if __name__ == '__main__':
    logging.basicConfig(filemode='w', level=logging.INFO,
                        format="%(asctime)s %(process)d %(levelname)s "
                               "[%(name)s:%(funcName)s:%(lineno)d] %(message)s")
    main()
