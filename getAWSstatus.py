import feedparser
import click

EC2 = aws_eu_frankfurt_EC2 = "http://status.aws.amazon.com/rss/ecr-eu-central-1.rss"
R53 = aws_eu_frankfurt_R53 = "http://status.aws.amazon.com/rss/route53.rss"
S3 = aws_eu_frankfurt_S3 = "http://status.aws.amazon.com/rss/s3-eu-central-1.rss"
RDS = aws_eu_frankfurt_RDS = "http://status.aws.amazon.com/rss/rds-eu-central-1.rss"

dict = {'EC2': EC2, 'R53': R53, 'S3': S3, 'RDS': RDS}

@click.command()
@click.option('-l', '--list', is_flag=True, help='Lists all served AWS services')
@click.option('-s', '--service',
              help='Prints status for chosen service. To list all availible services use -l',multiple=True)
@click.option('-a','--all', is_flag=True, help='Prints status for all defined services')
def get_status_of_aws(list, all, service='ec2'):
    """ Fetches, parses and prints status of AWS for endpoints defined at the beggining of the script. """
    if list:
        click.echo("Services:\n EC2 \n R53 \n S3 \n RDS")

    if service:
        try:
            for each in service:

                service = each

                service = dict[str(service.upper())]
                aws_status = feedparser.parse(service)
                click.echo(aws_status.feed.title)
                click.echo("Updated: " + aws_status.feed.updated)
                if len(aws_status.entries) == 0:
                    click.echo("There is no news")
                    click.echo("-" * 80)
                else:
                    click.echo(aws_status.entries[0].published + " - " + aws_status.entries[0].title)
                    click.echo("-" * 80)
        except KeyError as err:
            click.echo(click.style('Error: Invalid Key provided', fg='red') + "\nTry: \n  -l, --list \t for listing all availible services\n  --help \t for more infromation")

    if all:
        for source in EC2, R53, S3, RDS:
            aws_status = feedparser.parse(source)
            click.echo(aws_status.feed.title)
            click.echo("Updated: " + aws_status.feed.updated)
            if len(aws_status.entries) == 0:
                click.echo("There is no news")
                click.echo("-"*80)
            else:
                click.echo(aws_status.entries[0].published +" - " + aws_status.entries[0].title)
                click.echo("-" * 80)
    # else:
    #     click.echo(click.style(">>Program Terminating",fg="red"))


if __name__ == '__main__':
    get_status_of_aws()
