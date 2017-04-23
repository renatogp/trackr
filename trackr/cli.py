# coding: utf-8
import click


@click.command()
@click.option('--carrier', prompt='Carrier ID', help='Example: "ect" for Correios')
@click.option('--object-id', prompt='Object ID',
              help='Example: PN871429404BR')
def main(carrier, object_id):
    from trackr import Trackr
    from trackr.exceptions import PackageNotFound

    try:
        p = Trackr.track(carrier, object_id)
    except PackageNotFound as e:
        click.echo(click.style(
            u'Package with object ID {} ({}) not found'.format(
                object_id, carrier),
            fg='red')
        )

        if e.carrier_message:
            click.echo(click.style(
                u'Carrier message: {}'.format(e.carrier_message),
                fg='red',)
            )
        return

    click.echo(click.style(u'Package found!', fg='green'))

    for t in p.tracking_info:
        click.echo(t.__unicode__())


if __name__ == "__main__":
    main()
