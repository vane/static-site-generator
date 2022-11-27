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
python static_site_generator.py
```
## Usage
Specify config.yml input and output directory  
- input - directory with jekyll website data (where is _config.yml file)
- output - directory for generated files (assets directory in output will be deleted during generation)
