import click
import pdflatex as pl
from hw_2_1 import latex_table



@click.command()
@click.argument('filename', required=False)
def main(filename):
   pdfl = pl.PDFLaTeX.from_texfile('artifacts/example.tex')
   pdf, log, completed_process = pdfl.create_pdf(keep_pdf_file=True, keep_log_file=True)
if __name__ == '__main__':
    main()
