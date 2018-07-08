import click
from tohsaka import Tohsaka


@click.group()
def cli():
    """Tohsaka CLI"""
    pass


PRINT_FORMAT = '{0: <16} - {1}'
PARAM_FORMAT = '{0: <16} - {1: <64}'

@cli.command('list-spells')
def list_spells(): # pragma: no cover
    """List all the available spells"""
    spells = Tohsaka.get_spells()

    click.echo(PRINT_FORMAT.format('Name', 'Intro'))
    click.echo('-' * 80)
    for spell in spells:
        click.echo(PRINT_FORMAT.format(spell['name'], spell['intro']))


@cli.command('list-mystic-codes')
def list_mystic_codes(): # pragma: no cover
    """List all the available Mystic Codes"""
    mystic_codes = Tohsaka.get_mystic_codes()

    click.echo(PRINT_FORMAT.format('Name', 'Description'))
    click.echo('-' * 80)
    for code in mystic_codes:
        click.echo(PRINT_FORMAT.format(code['name'], code['description']))

@cli.command('show-mystic-code')
@click.argument('mystic_code')
def show_mystic_code(mystic_code): # pragma: no cover
    """Show the details of the Mystic Code"""
    mystic_json = Tohsaka.load_mystic_code(mystic_code)
    params = mystic_json.get('params', {})

    click.echo('%s - %s' % (mystic_json.get('name'), mystic_json.get('description')))
    click.echo('Parameters (%d):' % len(params.keys()))
    for key, value in params.items():
        required = value.get('required')
        if required:
            name = '(*)' + key
        else:
            name = key

        description = value.get('description')
        if value.get('default'):
            description += '. Default: %s' % value.get('default')

        click.echo(PARAM_FORMAT.format(name, description))


@cli.command()
@click.argument('mystic_code')
@click.argument('config', default={})
def run(mystic_code, config):
    """Run a Mystic Code"""
    tohsaka = Tohsaka(mystic_code, config)
    tohsaka.go()


if __name__ == '__main__':
    cli()
