#!/usr/bin/env python3

# copy of: https://gist.github.com/chrisguitarguy/e9cb271f6ac882627d0d61efe03dc8ae in order to avoid uncontrolled script changes.

import argparse
import requests
import os
import boto3 as aws

def _parse_args(args=None):
    p = argparse.ArgumentParser(description='Update a hostname record in route53 with the current IP address')
    p.add_argument('ipv4', help='IPV4 to set up')
    p.add_argument('zone_id', help='The DNS zone id to update')
    p.add_argument('hostname', help='The DNS name to update')
 

    return p.parse_args(args)


def _update_dns(ip, zone_id, hostname):
    dns = aws.client('route53')
    dns.change_resource_record_sets(
        HostedZoneId=zone_id,
        ChangeBatch={
            'Comment': 'Update {} record from ASG'.format(hostname),
            'Changes': [{
                'Action': 'UPSERT',
                'ResourceRecordSet': {
                    'Name': hostname,
                    'Type': 'A',
                    'TTL': 60,
                    'ResourceRecords': [{
                        'Value': ip
                    }],
                },
            }],
        },
    )


def main(args=None):
    args = _parse_args(args)

    _update_dns(args.ipv4, args.zone_id, args.hostname)


if __name__ == '__main__':
    main()
