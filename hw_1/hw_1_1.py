import click
import sys

def nl(source):
    for i, line in enumerate(source):
        print(f"{i+1:5}\t{line}", end='')


@click.command()
@click.argument('file', required=False)
def click_main(file =None):
    if file is None or file == '-':
        nl(sys.stdin)
    else:
        with open(file) as f:
            nl(f)


if __name__ == '__main__':
    click_main()
