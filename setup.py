from setuptools import setup, find_packages

setup(
    name='Terminalgemini',
    version='2.0.3',  # Update this as you make changes
    author='ticklecatisback',
    author_email='alesaholder@gmail.com',
    description='AI chat assistant in your terminal powered by Gemini models.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),  # Automatically find all packages in the directory
    include_package_data=True,  # Include all files specified in MANIFEST.in
    package_data={
        'terminalgemini': ['terminalgemini/tests/*.py', 'terminalgemini/tests/e2e/*.py', 'terminalgemini/tests/integration/*.py', 'tterminalgemini/ests/unit/*.py', 'terminalgemini/terminalgpt/*.py']
    },
    install_requires=[
        'google-generativeai',
        'tiktoken',
        'colorama',
        'cryptography',
        'click',
        'prompt-toolkit',
        'yaspin',
        'rich',
        'isort',
        'pytest',
        'pylint'
    ],
    entry_points={
        'console_scripts': [
            'terminalgpt=terminalgpt.main:cli'
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.10',  # Specify the minimum required Python version
)