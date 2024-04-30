# What is this

LLamaIndex's custom LLM, a Proxy-enabled version of Gemini!


# How to use

`pip install git+https://github.com/HawkClaws/proxy_gemini.git`

```python
from proxy_gemini import ProxyGemini

llm = ProxyGemini(
    api_key="your api_key",
    proxy_url="http://hogehoge",
)

res = llm.complete("HOGE HUGA world")
print(res.text)

```

