from functools import reduce
import click

__table_template = """\\begin{{center}}
\\begin{{tabular}}{{{header}}}
\\hline
{data}
\\hline
\\end{{tabular}}
\\end{{center}}"""

def latex_table(lines):
    n=len(lines[0])
    formated = [' & '.join([str(w) for w in x]) + '\\\\' for x in lines]
    data = '\n\\hline\n'.join(formated)
    return __table_template.format_map({'header': '|' + 'c|'*n, 'data': data})

@click.command()
@click.argument('filename', required=False)
def main(filename):
    st = latex_table([[1,2,3], [5,6,7], ['four', 'big', 'guys']])
    if filename is None or len(filename) == 0:
        print(st)
    else:
        fname = filename
        if not filename.endswith('.tex'):
            fname += '.tex'
        with open('artifacts/' + fname, 'w', encoding='utf-8') as out:
            out.write(st)

if __name__ == '__main__':
    main()
