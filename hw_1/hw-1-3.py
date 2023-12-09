import sys
import click



def wc_input(source):
    chars = 0
    words = 0
    lines = 0
    for line in source:
        lines += 1
        chars += len(line)
        words += len(line.split())

    return [lines, words, chars]


@click.command()
@click.argument('files', nargs=-1, required=False, type=click.Path(exists=True))
def main(files):
    if (len(files) == 0):
        ans = wc_input(sys.stdin)
        print(f"\t{ans[0]}\t{ans[1]}\t{ans[2]}")
    else:
        total_c = 0
        total_w = 0
        total_l = 0
        for filename in files:
            ans = wc_input(open(filename))
            print(f"{ans[0]:8}{ans[1]:8}{ans[2]:8} {filename}")
            total_c += ans[2]
            total_w += ans[1]
            total_l += ans[0]
        if len(files) > 1:
            print(f"{total_l:8}{total_w:8}{total_c:8} total")
        



if __name__ == '__main__':
    main()
