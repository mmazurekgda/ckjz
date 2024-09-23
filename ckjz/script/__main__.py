import requests
import random
import time
import click
import gpio as GPIO
import logging
from ckjz.constants import TOILET_TYPE


def update(name: TOILET_TYPE, status: bool, ip: str, port: int):
    url = f'http://{ip}:{port}/toilets/{name.value}'
    response = requests.post(
        url,
        params={'status': status},
        headers={"accept": "application/json"},
    )
    return response.json()


def add_toilet_type_options(function):
    for toilet_type in TOILET_TYPE:
        function = click.option(
            f"--{toilet_type.value}",
            default=None,
            type=int,
            required=False,
            help=f"GPIO pin number for {toilet_type.value}"
        )(function)
    return function


@click.group()
def cli():
    pass


@click.command()
@click.option('--ip', default='localhost', help='IP address of the server')
@click.option('--port', default=3000, help='Port of the server')
@click.option('--interval', default=1, help='Interval between updates')
def test(ip, port, interval, **kwargs):
    logger = logging.getLogger(__name__)
    logger.info(f"Starting test with interval {interval}")
    while True:
        for name in TOILET_TYPE:
            time.sleep(interval)
            logger.info(f"Updating `{name}`")
            status = random.choice([True, False])
            update(name, status, ip, port)
            logger.info(f"Updated `{name}` with status `{status}`")


@click.command()
@click.option('--ip', default='localhost', help='IP address of the server')
@click.option('--port', default=3000, help='Port of the server')
@click.option('--interval', default=1, help='Interval between updates')
@add_toilet_type_options
def run(ip, port, interval, **kwargs):
    logger = logging.getLogger(__name__)
    logger.info(f"Starting run with interval {interval}")
    if not any(kwargs.values()):
        logger.error("No pins provided!")
        exit(1)
    for name, pin in kwargs.items():
        logger.info(f"Setting up pin `{pin}` for `{name}`")
        GPIO.setup(pin, GPIO.IN)
    while True:
        for name, pin in kwargs.items():
            logger.info(f"Reading pin `{pin}` for `{name}`")
            status = GPIO.input(pin)
            logger.info(f"Updating `{name}` with status `{status}`")
            update(name, status, ip, port)
            logger.info(f"Updated `{name}` with status `{status}`")
        logger.info(f"Sleeping for {interval} seconds")
        time.sleep(interval)


cli.add_command(test)
cli.add_command(run)

if __name__ == '__main__':
    cli()
