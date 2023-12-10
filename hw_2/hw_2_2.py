import click
from hw_2_1 import latex_table
import subprocess

__doc_template = """\\documentclass{{article}}
\\usepackage{{graphicx}}
\\begin{{document}}
{contents}
\\end{{document}}"""

__pic_template="""\\\\
\\includegraphics[width=\\linewidth]{{{picfile}}}\\\\
"""

def latex_pic(filename):
    return __pic_template.format_map({'picfile': filename})


@click.command()
@click.argument('filename', required=False)
def main(filename):
   if filename is None:
       filename = 'example_2'
   
   tmp_file = filename + '.tex'
   with open(tmp_file, 'w') as out:
       contents = latex_table([[10, 20, 30], ['i', 'love', 'cats']]) + latex_pic('artifacts/random_cat.jpeg')
       out.write(__doc_template.format_map({'contents': contents}))

   cmd = f"pdflatex -interaction nonstopmode -output-directory=out/ {tmp_file}"
   res = subprocess.run(cmd, shell=True)


if __name__ == '__main__':
    main()
