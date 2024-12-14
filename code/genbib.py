import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode
import yaml

def load_bibtex_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as bib_file:
        parser = BibTexParser()
        parser.customization = convert_to_unicode
        bib_database = bibtexparser.load(bib_file, parser=parser)
    return bib_database.entries

def load_coauthor_urls(file_path):
    with open(file_path, 'r', encoding='utf-8') as yml_file:
        coauthors = yaml.safe_load(yml_file)
    return coauthors

def format_authors(authors, coauthor_urls):
    formatted_authors = []
    for author in authors.split(' and '):
        parts = author.split(', ')
        if len(parts) == 2:
            last_name = parts[0]
            first_name = parts[1]
            full_name = f"{first_name} {last_name}"
        else:
            full_name = author
            last_name = author.split()[-1]
            first_name = " ".join(author.split()[:-1])
        
        url = '#'
        if last_name in coauthor_urls:
            for entry in coauthor_urls[last_name]:
                if first_name in entry['firstname']:
                    url = entry['url']
                    break
        
        formatted_authors.append(f'<a href="{url}">{full_name}</a>')
    return ', '.join(formatted_authors)

def generate_markdown(publications, coauthor_urls, output_file):
    # Sort publications by year in descending order
    sorted_publications = sorted(publications, key=lambda x: x.get('year', '0'), reverse=True)
    
    with open(output_file, 'w', encoding='utf-8') as md_file:
        md_file.write("---\n")
        # md_file.write('title: "papers & publications"\n')
        md_file.write("toc: false\n")
        md_file.write("---\n\n")
        # md_file.write("Publications and working papers in reversed chronological order.\n\n")
        
        current_year = None
        for pub in sorted_publications:
            title = pub.get('title', 'No Title')
            authors = pub.get('author', 'No Author')
            formatted_authors = format_authors(authors, coauthor_urls)
            year = pub.get('year', 'No Year')
            journal = pub.get('journal', 'No Journal')
            year = pub.get('year', 'No Year')
            abstract = pub.get('abstract', '')

            pdf_link = f"assets/pdf/{pub.get('pdf', '')}"
            html_link = pub.get('html', '')

            # Create a valid ID by replacing spaces with hyphens
            abstract_id = f"abstract-{year}-{title}".replace(' ', '-')

            if year != current_year:
                if current_year is not None:
                    md_file.write("\n\n")
                current_year = year
                md_file.write(f"## {year}\n")
            
            md_file.write(f"**{title}**<br>\n")
            md_file.write(f"{formatted_authors}<br>\n")
            md_file.write(f"*{journal}*<br>\n")
            md_file.write('<div style="margin-bottom: 2px;"></div>\n')
            if pdf_link != 'assets/pdf/':
                md_file.write(f'<a href="{pdf_link}" style="border: 1px solid #007a04; color: #007a04; padding: 1px 8px; text-decoration: none; font-size: 0.7em; display: inline-block;">  PDF  </a>&nbsp;&nbsp;')
            if html_link:
                md_file.write(f'<a href="{html_link}" style="border: 1px solid #007a04; color: #007a04; padding: 1px 8px; text-decoration: none; font-size: 0.7em; display: inline-block;">  WEB  </a>&nbsp;&nbsp;')
            if abstract:
                md_file.write(f'<button onclick="toggleAbstract(\'{abstract_id}\')" style="border: 1px solid #007a04; color: #007a04; padding: 1px 8px; text-decoration: none; font-size: 0.7em; background: none; display: inline-block;">Abstract</button>\n')
                md_file.write(f'<div id="{abstract_id}" style="display:none; border: 1px solid #ccc; padding: 10px; margin-top: 10px;">{abstract}</div>\n')
            md_file.write("<br><br>\n")
        
        # Add the JavaScript function to toggle the abstract visibility
        md_file.write("<script>\n")
        md_file.write("function toggleAbstract(id) {\n")
        md_file.write("    var element = document.getElementById(id);\n")
        md_file.write("    if (element.style.display === 'none' || element.style.display === '') {\n")
        md_file.write("        element.style.display = 'block';\n")
        md_file.write("    } else {\n")
        md_file.write("        element.style.display = 'none';\n")
        md_file.write("    }\n")
        md_file.write("}\n")
        md_file.write("</script>\n")

def main():
    bib_file_path = 'assets/bibliography/papers.bib'
    coauthor_file_path = 'code/coauthors.yml'
    output_file_path = 'papers.qmd'
    publications = load_bibtex_file(bib_file_path)
    coauthor_urls = load_coauthor_urls(coauthor_file_path)
    generate_markdown(publications, coauthor_urls, output_file_path)

if __name__ == "__main__":
    main()