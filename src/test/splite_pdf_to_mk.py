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
        topic = {"heading": "", "content": []}
        for block in page.get_text("text").split("\n"):
            if block.startswith("("):  # subheading
                # topics.append((f"{page_heading} > {block[4:]}", page.number))
                topic["heading"] = block
            else:  # heading
                topic["content"].append(block)
        topics.append(topic)
    doc.close()
    return topics


def write_markdown(topic, output_dir):
    """ Write a list of text blocks to a markdown file. """
    # Remove any invalid characters from the filename
    heading = topic['heading']
    if heading.strip() == "":
        return
    filename = f"{heading}"

    # If the output directory doesn't exist, create it
    with open(f"{output_dir}/{filename}.md", "w") as f:
        f.write(f"""
#dic
### {heading}
?        
""")
        # write content
        content = topic['content']
        for block in content:
            if block.strip() in ["Key Vocabulary", "Supplementary Vocabulary"]:
                f.write(f"#### {block}\n")
            else:
                f.write(f"* {block}\n")
        print(f"write success: {filename} ")


if __name__ == "__main__":
    cur_file_path = os.path.dirname(os.path.realpath(__file__))
    out_file_path = os.path.abspath(os.path.join(cur_file_path, "../../")) + "/output"
    print(out_file_path)
    if not os.path.exists(out_file_path):
        os.makedirs(out_file_path)
    topics = pdf_to_markdown("englishpod365.pdf")
    for topic in topics:
        write_markdown(topic, output_dir=out_file_path)
