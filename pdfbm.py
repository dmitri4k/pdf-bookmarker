import argparse
import os
from PyPDF2 import PdfWriter, PdfReader

def add_bookmarks_from_file(pdf_file):
    base_name = os.path.splitext(pdf_file)[0]
    bookmarks_file = f"{base_name}.txt"
    output_file = f"{base_name}_with_bookmarks.pdf"

    reader = PdfReader(pdf_file)
    writer = PdfWriter()

    # Copy all pages from the reader to the writer
    for page in reader.pages:
        writer.add_page(page)

    # Keep track of the parent bookmarks to handle levels
    parents = [None] * 10  # Adjust based on the maximum expected depth

    try:
        with open(bookmarks_file, 'r', encoding='utf-8') as f:
            for line in f:
                # Expecting tab-delimited values for: page number, level, title
                parts = line.strip().split('\t')
                if len(parts) == 3:
                    page_number = int(parts[0].strip()) - 1  # Convert page number to 0-based index
                    level = int(parts[1].strip())
                    title = parts[2].strip()

                    # Adding bookmark at the correct level
                    if level == 0:
                        bm = writer.add_outline_item(title, page_number, parent=None)
                        parents[level] = bm
                    else:
                        parent_bm = parents[level-1]  # Get the parent at one level up
                        bm = writer.add_outline_item(title, page_number, parent=parent_bm)
                        parents[level] = bm

    except FileNotFoundError:
        print(f"Bookmark file {bookmarks_file} not found.")
        exit(1)

    # Write the output PDF with bookmarks
    with open(output_file, 'wb') as f_out:
        writer.write(f_out)

    print(f"Output PDF saved as {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Automatically add hierarchical bookmarks to a PDF file from a corresponding text file.")
    parser.add_argument('pdf_file', type=str, help='The input PDF file path')
    args = parser.parse_args()
    add_bookmarks_from_file(args.pdf_file)

if __name__ == "__main__":
    main()