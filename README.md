# pigmy

Are you annoyed by having to maintain your list of active and pending grants in 5 different formats? You have the NIH *Research Support* format, which excludes amounts, the NIH *Other Support* format, which includes amounts, NSF formats, internal formats for P&T committees, and your own personal list to keep track of deadlines and applications... and the list goes on.

What a pain to keep all these things updated, requiring hours of time. Now, `pigmy` can help! `pigmy` (pronounced 'pygmy') is a python application that makes formatting grant metadata easy. It's the PI grant metadata yeoman, here to take care of your grant metadata management needs.

Just maintain your list of grants once, in a human- and computer-readable `yaml` format, and `pigmy` will use `pandoc` to output whatever you want in a template-based, customizable output. We have built-in templates for common output formats (like those specified above), but you can also make whatever output format you want.

# Getting started

## Examples

The grant metadata file [example_grants.yaml](grant_metadata/example_grants.yaml) can create the output file [example_research_support.pdf](output/example_research_support.pdf). This example is based on the [nih_other_support.txt format](formats/nih_other_support.txt) and the [research_support_template.md document template](document_templates/research_support_template.md). 

Further example `grants.yaml` files are in [grant_metadata](/grant_metadata), and example output is in [output](/output).


## Run on the command line:

```
python pigmy.py -g grants.yaml -f output_format.txt

python pigmy.py --help
```

## How it works

`pigmy` is quite simple. It will read your `grants.yaml` file, which is just a list of grants in `yaml` format, and then uses a user-provided template to output those grants in the format you want. The built-in templates are in `markdown` format, so `pigmy` will output `markdown` text, which you can then pipe through `pandoc` to get a PDF or docx.

There are two user-customizable files that determine how `pigmy` will format the output: the format files and document templates.

**Format files**, found in [/formats](formats), provide a way for you specify how text from a single grant will be organized. An example is:

```
{namePlusPI} &nbsp; &nbsp; &nbsp; {dates} &nbsp; &nbsp; &nbsp; {effort}  
{funder}  
Title: {title}  
Role: {role}
```

The bracketed values (like `{title}`) will be populated with information from the grant. These formats specify how each individual grant will be formatted.

**Document files**, found in [/document_templates](/document_templates), show how the grants will be organized in a file. An example is the NIH research support template, which looks like this:

```
# D. Research support

## Active

{active}
	
```

Here, you use bracketed *status* codes. In this example, all the active grants, formatted according to the *format file* and appended in a list, will replace the `{active}` tag. You can use this to insert your grants list into any document format you like.


# Recipes

Generate an NIH-style 'research support' that can be appended to the end of a NIH-format Biosketch:

```
python pigmy.py -e -g grant_metadata/example_grants.yaml \
	-d document_templates/research_support_template.md \
	-f formats/nih_other_support.txt \
	| pandoc --reference-doc pandoc_templates/template.docx \
	-o output/example_research_support.docx
```

Use LibreOffice to generate a PDF of said output

```
python pigmy.py -e -g grant_metadata/example_grants.yaml \
	-d document_templates/research_support_template.md \
	-f formats/nih_other_support.txt \
	| pandoc --reference-doc pandoc_templates/template.docx \
	-o output/example_research_support.docx

soffice --convert-to pdf output/example_research_support.docx --outdir output

```


# Run a web-server

`pigmy` uses the lightweight `flask` microframework to give you a web interface, making it even easier to get the format you need, if you like pointy-clicky.

Run like:

```
FLASK_APP=flask_pigmy.py flask run
```

Then point browser to: http://127.0.0.1:5000

