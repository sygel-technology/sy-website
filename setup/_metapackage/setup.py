import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo12-addons-sygel-technology-sy-website",
    description="Meta package for sygel-technology-sy-website Odoo addons",
    version=version,
    install_requires=[
        'odoo12-addon-website_chartjs',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 12.0',
    ]
)
