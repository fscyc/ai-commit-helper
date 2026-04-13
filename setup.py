"""
打包配置
"""

from setuptools import setup, find_packages
import os

# 读取README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# 读取requirements.txt
def read_requirements():
    requirements = []
    req_file = "requirements.txt"
    
    if os.path.exists(req_file):
        with open(req_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    requirements.append(line)
    
    return requirements

setup(
    name="ai-commit-helper",
    version="0.1.0",
    author="fscyc",
    author_email="5888161@qq.com",
    description="AI-powered Git commit message generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fscyc/ai-commit-helper",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Version Control :: Git",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    extras_require={
        "web": [
            "fastapi>=0.104.0",
            "uvicorn[standard]>=0.24.0",
            "pydantic>=2.0.0",
        ],
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "twine>=4.0.0",
            "build>=1.0.0",
        ],
        "color": [
            "colorama>=0.4.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "aicommit=ai_commit_helper.cli:main",
            "ai-commit-helper=ai_commit_helper.cli:main",
        ],
    },
    include_package_data=True,
    project_urls={
        "Bug Reports": "https://github.com/fscyc/ai-commit-helper/issues",
        "Source": "https://github.com/fscyc/ai-commit-helper",
        "Documentation": "https://github.com/fscyc/ai-commit-helper#readme",
    },
)