import argparse
import sys

from license import get_licence_status


def scrape():
    parser = argparse.ArgumentParser('Scraper of Driving License Status')
    parser.add_argument('--license_no', '-n', type=str, required=True,
                        help='driving license number')
    parser.add_argument('--dob', '-d', type=str, required=True,
                        help="date of birth of holder's driving license e.g. 31-01-1990")
    args = parser.parse_args()
    sys.stdout.write(str(get_licence_status(args)))


if __name__ == '__main__':
    scrape()
