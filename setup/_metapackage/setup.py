import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-sygel-technology-sy-website",
    description="Meta package for sygel-technology-sy-website Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-website_sale_partner_firstname>=15.0dev,<15.1dev',
        'odoo-addon-website_sale_partner_second_lastname>=15.0dev,<15.1dev',
        'odoo-addon-website_signup_additional_fields>=15.0dev,<15.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 15.0',
    ]
)
