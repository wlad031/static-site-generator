Static Site Generator
===================

This application can help you if you want generate static web application such as blog or something else. 

### Plugins

The main point of application is it's plugins-based architecture. 

Implemented plugins:
- blog
- 'about me' page

You can write your own plugin using some of existing as example and use it in your application.

### Configuration

In `config.py` file you can register needed plugins and change the build directory or site header/footer text.

### Installation and running
 
 - Clone this repository:

```
git clone https://github.com/wlad031/static-site-generator static-site-generator
cd static-site-generator/
```

 - Install python dependencies:

```
pip3 install -r requirements.txt
```

 - Run application:

```
python3 src/generate-static-site.py [--watch] --config /path/to/config/folder

# For example:
python3 src/generate-static-site.py --blog-config /path/to/examples
```
