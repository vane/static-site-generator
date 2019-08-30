static-site-generator
====


## Description

Static website generator based that is using jekyll format to generate [vane.pl](https://vane.pl) website.  
No site configuration files or existing markdown data was changed to generate output.


## Dependencies
pygments - for syntax hightlighting  
libsass - for sass style compile  
csscompressor - for css compression  
markdown - for makrdown parsing generation  
liquidpy - for liquid template parsing  

Emulate
- jekyl
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
- input - directory with jekyll data
- output - directory for generated files (assets directory in output will be deleted during generation)
