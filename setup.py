from setuptools import setup, find_packages

with open("README.md", "r") as fp:
    readme = fp.read()

DESCRIPTION = "LLamaIndex's custom LLM, a Proxy-enabled version of Gemini!"

setup(
    name="ProxyGemini",
    version="0.0.1",
    author="HawkClaws",
    packages=find_packages(),
    install_requires=[
        "llama-index-core>=0.10.0",
    ],
    python_requires=">=3.6",
    include_package_data=True,
    url="https://github.com/HawkClaws/ProxyGemini",
    project_urls={"Source Code": "https://github.com/HawkClaws/ProxyGemini"},
    description=DESCRIPTION,
    long_description=readme,
    long_description_content_type='text/markdown',
    license="MIT",
)