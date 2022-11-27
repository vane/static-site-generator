static-site-generator
====


## Description

Static website generator that is using jekyll format to generate [vane.pl](https://vane.pl) website.  
No jekyll configuration files or existing markdown data was changed to generate output.


## Dependencies
pygments - for syntax hightlighting  
libsass - for sass style compile  
csscompressor - for css compression  
markdown - for makrdown parsing generation  
liquidpy - for liquid template parsing  

Emulate
- jekyll
- rouge
- jekyll-feed  
- jekyll-sitemap  
- jekyll-seo-tag  

## Install
```bash
git clone https://github.com/vane/static-site-generator.git
python3 -m .venv static-site-generator-env
source static-site-generator-env/bin/activate
pip install -r static-site-generator/requirements.txt
```
## Usage
```bash
python static_site_generator.py -h
```  
- input - directory with jekyll website data (the one containing _config.yml)
- output - directory for generated files (assets directory in output will be deleted during generation)

## Sample run
```bash
#!/bin/bash
.venv/bin/python3 static_site_generator.py \
-i /home/user/jekyl-blog-root \
-o /home/user/blog-generated
```
