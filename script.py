import argparse, os, json
from pypdf import PdfReader
from common_utils.log.logger import Logger

logger = Logger('Rewe e-Bon Parser')


def parse_args():
    parser = argparse.ArgumentParser('REWE e-Bon Parser', description='This script parses the PDFs of Rewe e-Bons')
    parser.add_argument('-p', '--path', type=str, help='Path to e-Bons', required=True)
    parser.add_argument('-c', '--config', type=str, help='Path to config file', required=False)
    parser.add_argument('-f', '--filter', type=str, help='Filter for a specific month', required=False)
    return parser.parse_args()

def parse_pdf(path: str) -> dict:
    # Open the PDF
    pdf = PdfReader(path)
    
    # If it has more than two pages, we must concatinate these
    page = ''
    for pdf_page in pdf.pages:
        page += '\n'
        page += pdf_page.extract_text()
    
    # Process line by line and safe it in a dictionary
    lines = page.split('\n')
    out = {}
    for line in lines:
        splitted_line = line.split()
        if 'SUMME                   EUR' in line:
            if len(splitted_line) != 3:
                logger.critical(f'Error in parsing sum of {path}')
                continue
            out['sum'] = float(splitted_line[2].replace(',', '.'))
        elif 'A=  19,0%' in line:
            if len(splitted_line) != 5:
                logger.warning(f'Error in parsing nonfood of {path}')
                continue
            out['nonfood_tax'] = float(splitted_line[3].replace(',', '.'))
            out['nonfood_brutto'] = float(splitted_line[4].replace(',', '.'))
        elif 'B=   7,0%' in line:
            if len(splitted_line) != 5:
                logger.warning(f'Error in parsing food of {path}')
                continue
            out['food_tax'] = float(splitted_line[3].replace(',', '.'))
            out['food_brutto'] = float(splitted_line[4].replace(',', '.'))
        elif 'Markt:' in line:
            # Markt:1234 Kasse:1 Bed.:123456
            # -> Extract Markt:1234, Split at char `:`
            markt_number = splitted_line[0].split(':')[1]
            if not markt_number.isdigit():
                logger.critical(f'Markt number "{markt_number}" is not a number!')
                continue
            out['markt_number'] = markt_number

    return out

def main():
    args = parse_args()
    
    final = {}
    for entry in os.scandir(args.path):
        # Iterate the given directory and search for .pdf files
        if entry.is_file() and entry.name.endswith('.pdf'):
            if args.filter and not args.filter in entry.name:
                # Check if the filename contains the filter string
                logger.warning(f'Skipping file "{entry.name}" because your filter "{args.filter}" didnt match')
                continue
            logger.info(f'Processing file: {entry.path}')
            # Parse the PDF
            data = parse_pdf(entry.path)
            # Error checking
            if 'markt_number' not in data:
                # Cehck if we were able to parse a markt number. This is mandatory
                logger.critical('Markt number could not be parsed!')
                continue
            elif data['markt_number'] not in final:
                final[data['markt_number']] = {}
            
            # Merge / Add the values and data with the final dictionary
            markt_number = data['markt_number']
            del data['markt_number']
            for k, v in data.items():
                if k not in final[markt_number]:
                    final[markt_number][k] = 0.0
                final[markt_number][k] += v

    print(json.dumps(final, indent=4))

if __name__ == '__main__':
    main()
