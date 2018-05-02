# pigmy

Are you annoyed by having to maintain your list of active and pending grants in 5 different formats? You have the NIH *Research Support* format, which excludes amounts, the NIH *Other Support* format, which includes amounts, NSF formats, internal formats for P&T committees, and your own personal list to keep track of deadlines and applications... and the list goes on.

What a pain to keep all these things updated, requiring hours of time. Now, `pigmy` can help! `pigmy` (pronounced 'pygmy') is a python application that makes formatting grant metadata easy. It's the PI grant metadata yeoman, here to take care of your grant metadata management needs.

Just maintain your list of grants once, in a human- and computer-readable `yaml` format, and `pigmy` will use `pandoc` to output whatever you want in a template-based, customizable output. We have built-in templates for common output formats (like those specified above), but you can also make whatever output format you want.

# Getting started

## Run on the command line:

```
python pigmy.py -g grants.yaml -f output_format.txt

python pigmy.py --help
```

## Run a web-server

`pigmy` uses the lightweight `flask` microframework to give you a web interface, making it even easier to get the format you need, if you like pointy-clicky.

Run like:

```
FLASK_APP=flask_pigmy.py flask run
```

Then point browser to: http://127.0.0.1:5000

