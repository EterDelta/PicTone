from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as readme:
    long_description = readme.read()

setup(
    name='pictone',
    version='1.0.0',
    description="Fun image to Vectorscope audio CLI tool. With support for complex sequences.",
    long_description_content_type="text/markdown",
    long_description=long_description,
    author='EterDelta',
    license='MIT',
    url='https://github.com/EterDelta/PicTone',
    package_dir={'': 'src'},
    packages=[
        'pictone'
    ],
    install_requires=[
        'opencv-python',
        'numpy'
    ],
    entry_points={
        'console_scripts': [
            "pictone = pictone.cli:entry",
        ],
    },
    classifiers=[
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Artistic Software",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    python_requires='>=3.6'
)
