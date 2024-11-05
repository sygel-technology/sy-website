import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo13-addons-sygel-technology-sy-website",
    description="Meta package for sygel-technology-sy-website Odoo addons",
    version=version,
    install_requires=[
        'odoo13-addon-website_disable_lang_menu',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 13.0',
    ]
)
