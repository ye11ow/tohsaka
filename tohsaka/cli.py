import json
import click
from tohsaka import Tohsaka
from utils.file_util import load_json
import utils.log_util as log_util


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

    click.echo(f'{mystic_json.get("name")} - {mystic_json.get("description")}')
    click.echo(f'Parameters ({len(params.keys())}):')
    for key, value in params.items():
        required = value.get('required')
        if required:
            name = '(*)' + key
        else:
            name = key

        description = value.get('description')
        if value.get('default'):
            description += f'. Default: value.get("default")'

        click.echo(PARAM_FORMAT.format(name, description))


@cli.command()
@click.argument('profile', type=click.Path(exists=True))
@click.option('--log', default=False, help='the path of the log file')
def load(profile, log):
    if log:
        log_util.set_file_logger(log)
    else:
        log_util.set_std_logger()

    input_params = load_json(profile)

    if not 'mystic' in input_params:
        click.echo('Invalid profile')
    else:
        tohsaka = Tohsaka(input_params.pop('mystic'), input_params)
        tohsaka.go()


@cli.command()
@click.argument('mystic_code')
@click.option('--log', default=False, help='the path of the log file')
@click.option('--save', default=False, help='save the config')
def run(mystic_code, log, save):
    if log:
        log_util.set_file_logger(log)
    else:
        log_util.set_std_logger()

    """Run a Mystic Code"""
    mystic_json = Tohsaka.load_mystic_code(mystic_code)
    params = mystic_json.get('params', {})
    input_params = {}

    # if there are params, start wizard
    # otherwise, run directly
    if params:
        for key, value in params.items():
            required = value.get('required')
            if required:
                name = '(*)' + key
            else:
                name = key

            description = value.get('description')
            if value.get('default'):
                description += f'. (Default: {value.get("default")})'

            result = input(PARAM_INPUT_FORMAT.format(name, description))

            if result:
                if value.get('type') == 'boolean':
                    input_params[key] = str(result).lower() in ['1', 'true', 't']
                else:
                    input_params[key]  = str(result)
            elif value.get('default'):
                input_params[key] = value.get('default')
        click.echo('\n')

    tohsaka = Tohsaka(mystic_code, input_params)
    tohsaka.go()

    if isinstance(save, str):
        click.echo(f'Saving the config to {save}...')
        click.echo('All set.\n')

        with open(save, 'w') as json_file:
            json_file.write(json.dumps(input_params, indent=4))

if __name__ == '__main__': # pragma: no cover
    cli()
