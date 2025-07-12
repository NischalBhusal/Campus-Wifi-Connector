from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="campus-wifi-connector",
    version="1.0.0",
    author="Campus WiFi Team",
    author_email="support@campuswifi.app",
    description="A Python mobile app for connecting to campus WiFi networks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/campus-wifi-connector",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Education",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: System :: Networking",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=0.991",
            "pre-commit>=2.20.0",
        ],
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.0.0",
            "myst-parser>=0.18.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "campus-wifi-connector=main:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/yourusername/campus-wifi-connector/issues",
        "Source": "https://github.com/yourusername/campus-wifi-connector",
        "Documentation": "https://campus-wifi-connector.readthedocs.io/",
    },
    keywords="wifi campus education mobile kivy python networking",
    include_package_data=True,
    package_data={
        "": ["*.txt", "*.md", "*.json", "*.kv", "*.png", "*.jpg", "*.jpeg"],
        "assets": ["*"],
        "config": ["*.py", "*.json"],
    },
    zip_safe=False,
)
