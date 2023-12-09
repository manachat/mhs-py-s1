import sys
import click


def cyclic_read(source, n) :
    lst = [''] * n
    end = 0
    for line in source:
        lst[end % n] = line
        end += 1
    limit = min(n, end)
    for i in range(limit):
        print(lst[(end - limit + i) % n], end='')

def files_tail(files):
    if len(files) == 1:
        cyclic_read(open(files[0]), 10)
    else:
        for filename in files:
            with open(filename) as f:
                print(f"==> {filename} <==")
                cyclic_read(f, 10)


@click.command()
@click.argument('files', nargs=-1, required=False, type=click.Path(exists=True))
def main(files):
    if len(files) == 0:
        cyclic_read(sys.stdin, 17)
    else:
        files_tail(files)



if __name__ == '__main__':
    main()
