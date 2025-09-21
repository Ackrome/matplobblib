from setuptools import setup, find_packages
import re
import os


def readme():
  with open('README.md', 'r', encoding='utf-8') as f:
    return f.read()

def get_version():
    with open(os.path.join('matplobblib', '__init__.py'), 'r') as f:
        version_file_content = f.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file_content, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='matplobblib',
    version=get_version(),
    packages=find_packages(),
    description='Just a library for some subjects',
    author='Ackrome',
    author_email='ivansergeyevicht@gmail.com',
    url='https://github.com/Ackrome/matplobblib',
    long_description=readme(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    include_package_data=True,  # Include non-Python files specified in MANIFEST.in or package_data
    # spackage_data=package_data,
    install_requires=[
        "numpy",
        "sympy",
        "pandas",
        "scipy",
        "pyperclip",
        "PyMuPDF",
        "graphviz",
        "statsmodels",
        "cvxopt",
        "beautifulsoup4",
        "matplotlib",
        "numba",
        "IPython",
        "tqdm",
        "scikit-learn",
        "scikit-image",
        "requests",
        "Pillow"
    ],
    license='MIT'
)
