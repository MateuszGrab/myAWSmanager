
import click
import boto3


def color(status):
    if status == "running":
        return click.style(status, fg='green')
    elif status == "pending" or status == "stopping" or status == "shutting-down":
        return click.style(status, fg='yellow')
    else:
        return click.style(status, fg='red')


@click.command()
@click.option('-l', '--list', is_flag=True, help='List all instances with status')
def get_ec2_status(list):

    """"This scripts should list all instances """
    ec2 = boto3.Session(profile_name='default')
    ec2 = ec2.client('ec2')
    aws_response = ec2.describe_instances()

    for reservation in aws_response['Reservations']:
        for instance in reservation['Instances']:
            tags_list = instance['Tags']
            intance_name = ""
            for dictionary_value in tags_list:
                if 'Name' in dictionary_value.values():
                    instance_name = dictionary_value['Value']

            click.echo(
                str(instance['InstanceId'])
                + " "
                + color(str(instance['State']['Name']))
                + " "
                + str(instance_name)
            )

if __name__ == "__main__":
    get_ec2_status()