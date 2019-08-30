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
git clone
pip install requirements.txt
```
## Usage
Specify config.yml input and output directory  
- input - directory with jekyll website data (where is _config.yml file)
- output - directory for generated files (assets directory in output will be deleted during generation)

## Why
Because I can.  
I can't manage meta tags properly or generate sitemap for each tag or custom pages. Generate one page only or read update page date from git repository instead of using some jekyll internal system. So I recreated jekyll with all above plugins output using 400 lines of python code.
