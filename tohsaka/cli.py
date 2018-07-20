import json
import click
from tohsaka import Tohsaka
from utils.file_util import load_json


@click.group()
def cli(): # pragma: no cover
    """Tohsaka CLI"""
    pass


PRINT_FORMAT = '{0: <16} - {1}'
PARAM_FORMAT = '{0: <16} - {1: <64}'
PARAM_INPUT_FORMAT = '{0}: {1}? '


@cli.command('list-mystic-codes')
def list_mystic_codes():
    """List all the available Mystic Codes"""
    mystic_codes = Tohsaka.get_mystic_codes()

    click.echo(PRINT_FORMAT.format('Name', 'Description'))
    click.echo('-' * 80)
    for code in mystic_codes:
        click.echo(PRINT_FORMAT.format(code['name'], code['description']))

@cli.command('show-mystic-code')
@click.argument('mystic_code')
def show_mystic_code(mystic_code):
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
@click.option('--config', default=False, help='config file')
@click.option('--save', default=False, help='save the config')
def run(mystic_code, config, save):
    """Run a Mystic Code"""
    mystic_json = Tohsaka.load_mystic_code(mystic_code)
    params = mystic_json.get('params', {})
    input_params = {}

    # config file is specified, use the config file as param
    if config:
        input_params = load_json(config)
    # if config is not there but there are params, start wizard
    # otherwise, run directly
    elif params:
        for key, value in params.items():
            required = value.get('required')
            if required:
                name = '(*)' + key
            else:
                name = key

            description = value.get('description')
            if value.get('default'):
                description += '. (Default: %s)' % value.get('default')

            result = input(PARAM_INPUT_FORMAT.format(name, description))

            if result:
                input_params[key] = str(result)
            elif value.get('default'):
                input_params[key] = value.get('default')
        print('\n')

    tohsaka = Tohsaka(mystic_code, input_params)
    tohsaka.go()

    if isinstance(save, str):
        print('Saving the config to %s...' % (save))
        print('All set.\n')

        with open(save, 'w') as json_file:
            json_file.write(json.dumps(input_params, indent=4))

if __name__ == '__main__': # pragma: no cover
    cli()
