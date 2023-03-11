import fitz
import os


def pdf_to_markdown(pdf_path):
    """
    Extracts the topics from a PDF file based on headings and subheadings.
    Returns a list of (topic_title, page_number) tuples.
    """
    doc = fitz.open(pdf_path)
    topics = []
    for page in doc:
        page_heading = ""
        for block in page.get_text("text").split("\n"):
            if block.startswith("### "):  # subheading
                topics.append((f"{page_heading} > {block[4:]}", page.number))
            elif block.startswith("## "):  # heading
                page_heading = block[3:]
                topics.append((page_heading, page.number))
    doc.close()
    return topics


def get_text_blocks(doc, page_num):
    """ Get a list of text blocks on a given page. """
    page = doc[page_num]
    text_blocks = []

    for block in page.getText("text").split("\n"):
        if block.strip():
            text_blocks.append(block)

    return text_blocks


def write_markdown(text_blocks, filename, output_dir):
    """ Write a list of text blocks to a markdown file. """
    # Remove any invalid characters from the filename
    filename = ''.join(x for x in filename if x.isalnum() or x in ('-', '_'))

    # If the output directory doesn't exist, create it
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(f"{output_dir}/{filename}.md", "w") as f:
        for block in text_blocks:
            f.write(f"{block}\n\n")

"""
To use this code, you can call the `split_pdf_to_markdown` function with the path to the input PDF file and the path to the output folder where you want to save the generated Markdown files. For example:
"""

if __name__ == "__main__":
    cur_file_path = os.path.dirname(os.path.realpath(__file__))
    out_file_path = os.path.abspath(os.path.join(cur_file_path, "../../")) + "/output"
    print(out_file_path)
    if not os.path.exists(out_file_path):
        os.makedirs(out_file_path)
    split_pdf_to_markdown("englishpod365.pdf", output_folder=out_file_path)


