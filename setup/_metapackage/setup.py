import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-sygel-technology-sy-website",
    description="Meta package for sygel-technology-sy-website Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-website_hide_portal_my_timesheets>=16.0dev,<16.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 16.0',
    ]
)
