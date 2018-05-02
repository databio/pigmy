from argparse import ArgumentParser
import yaml
import os 

from flask import Flask, render_template, redirect, url_for, request
app = Flask(__name__)

@app.route("/")
def pigmy():
    import glob
    files = glob.glob("formats/*.txt")
    format_sources = [{"name": f} for f in files]
    files = glob.glob("grant_metadata/*.yaml")
    grant_sources = [{"name": f} for f in files]
    
    return render_template('select.html',
        format_sources=format_sources,
        grant_sources=grant_sources,
        route="process")


@app.route("/process" , methods=['GET', 'POST'])
def process():
    format_source = request.form.get('format_source')
    grant_source = request.form.get('grant_source')
    status = request.form.getlist('status_filter')
    print(status)
    outfolder = "output"  # to be made variable
    outfile = os.path.join(outfolder, "output.docx")

    import subprocess
    cmd = "python pigmy.py -g {grant_source} -s {status} -f {format_source}".format(
        grant_source=grant_source, format_source=format_source, status=" ".join(status))

    ps1 = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    ps = subprocess.Popen(
        ["pandoc", "--reference-doc", "pandoc_templates/template.docx",
        "-o", outfile, "--preserve-tabs"], 
        stdin=ps1.stdout, stdout=subprocess.PIPE)
    res = ps.communicate()
    print(res)
    result = cmd + "<br><br>You can find your output file at " + outfile
    result += pigmy()
    return(result)
   