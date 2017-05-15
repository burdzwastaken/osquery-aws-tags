#!/usr/bin/python

# retrieves AWS tags from the instance it is running on.
# awstags includes two columns - key and value.
# dependencies: boto-2.46.1, osquery-2.2.0.

from boto import ec2
from boto.utils import get_instance_identity

def main():

    # get instance information
    instance_identity = get_instance_identity()
    instance_id = instance_identity['document']['instanceId']
    region = instance_identity['document']['region']

    # connect to region
    conn = ec2.connect_to_region(region)

    # search for ec2 instance tags of running host
    tags = conn.get_all_tags(filters={"resource-id": instance_id})

    # inject tags into rows
    aws_tags = []
    for tag in tags:
        row = {}
        row['key'] = tag.name
        row['value'] = tag.value
        aws_tags.append(row)
    return aws_tags

if __name__ == '__main__':
    main()
