# aws_tags_ext
An osquery extension that allows for the retrieval of AWS tags attached to that node.

*NOTE:* use the offical tables included into osquery [2.7.0](https://github.com/facebook/osquery/releases/tag/2.7.0)

## overview:
This extension enables one table that extends osquery. The data from this table is retrieved using the boto library. This was built of the need to be able to create queries based on tags given to instances. Our environment was heavily automated through the use of tags so extending this to our monitoring tool was essential.

## prerequisites:
- osquery must be installed on the target node
- python 2.7 must be installed on the target node
- ec2 instance running Linux
- role attached to the ec2 instance for querying of tags
- role must have permissions to use `ec2:DescribeTags`
- `sudo apt install python-pip` will install the required python environment
- `sudo pip install -r requirements.txt` which will install the following dependencies:
  * osquery-2.2.0
  * boto-2.46.1
  * six-1.10.0
  * thrift-0.10.0

## select * from aws_tags;
### osqueryi
add the extension to osquery:
```
burdz@hackbook:~/osquery/awstags_ext$ osqueryi --extension aws_tags_table.ext
Using a virtual database. Need help, type '.help'
osquery>
```
check if the extension is running:
```
osquery> select * from osquery_extensions;
+-------+---------+-------------------+-------------+---------------------------------------+-----------+
| uuid  | name    | version           | sdk_version | path                                  | type      |
+-------+---------+-------------------+-------------+---------------------------------------+-----------+
| 0     | core    | 2.1.2-23-ga23a2fa | 2.1.2       | /home/burdz/.osquery/shell.em         | core      |
| 51793 | aws_tags| 1.0.0             | 1.8.0       | /home/burdz/.osquery/shell.em.51793   | extension |
+-------+---------+-------------------+-------------+---------------------------------------+-----------+
```
query the table:
```
osquery> select * from aws_tags;
+---------------------------+----------------------+
| key                       | value                |
+---------------------------+----------------------+
| Name                      | awstagging_test      |
| environment               | development          |
| product                   | infosec              |
| service                   | osquery              |
+---------------------------+----------------------+
```

## AWS role
As this information cannot be extracted from ec2 metadata this table does require a role to be attached to the instance with the following policy:
```
{
  "Version": "2012-10-17",
  "Statement": [
    {    
      "Effect": "Allow",
      "Action": [ "ec2:DescribeTags"],
      "Resource": ["*"]
    }
  ]
}
```
AWS has now made it easy to add / modify a role attached to an instance - https://aws.amazon.com/about-aws/whats-new/2017/02/new-attach-an-iam-role-to-your-existing-amazon-ec2-instance/

## TODO
- auto load the module
- osqueryd examples
- performance testing
- update readme
- possibly more error handling
