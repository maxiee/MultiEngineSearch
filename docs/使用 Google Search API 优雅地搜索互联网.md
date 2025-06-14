如何获取最新资讯？我发现[[搜索引擎]]是一个很好的信息来源。尤其是构思出关键词，以程序化方式，定期、自动地获取，就像 RSS 订阅一样。

最初，我基于 [[qutebrowser]] 写了一个浏览器自动化工具，对众多关键词进行定期抓取。但是，Google 的反爬比较厉害，很容易就被识别为异常流量了。

之后，我了解到 Google 提供搜索 API，允许开发人员以编程方式访问搜索结果。

并且还有一定的免费额度，定价方面，每天免费提供100次API调用，之后每1000次为5美元，最多可达每天1万次。这个额度足够我个人使用了。

于是，我打算改用正规的 API。在本文中记录了我的实践过程。如果你有好的想法或建议，欢迎在评论区交流！

---

## 视频教程

幸运的是，我搜到了一个视频教程，手把手教我们实现本文目标：

- 《[Getting Started With Google Search API For Beginners In Python](https://www.youtube.com/watch?v=D4tWHX2nCzQ&t=1s)》
- 《[Python中的Google搜索API完整指南- 视频总结 - Glarity](https://glarity.app/zh-CN/youtube-summary/education/getting-started-with-google-search-api-18371781_568494)》

下面是我记录的大致流程，具体的请参见原视频：

- 进入 Google Console，创建一个新项目并进入。侧边栏选择 APIs & Services，子菜单选择 Library。进入页面后有一个搜索框，搜索“search api”。选择 **Custom Search API**，点击 Enable。再次侧边栏选择 APIs & Services，子菜单选择 Credentials。点击 Create Credentials，弹出菜单点击 API Key，把这个 key 保存下来。

- 接下来需要创建一个 Google Search Engine。进入 `programmablesearchengine.google.com`，在其中创建一个搜索引擎。当使用 API 代码的时候，API 使用这里的搜索引擎设置。其中的设置包括，搜索范围（整个互联网还是部分网站）。点击创建后，会出现一个 HTML 的 JavaScript 嵌入代码，用于嵌入网页中。我们不需要，返回到创建的搜索引擎列表，再次进入搜索引擎，会显示其详细信息，复制 **Search Engine ID**。

- 接下来是调用 CustomSearch 的 JSON API。参数：`cx` 对应 **Search Engine ID**。`dateRestrict` 控制日期。

- 视频中给出了一个基于 Requests 的 Python 封装，可以直接使用。并且在 main 方法中提供了翻页爬取逻辑。

相关文档地址：

- 📑 [Google Search API Documentation](https://developers.google.com/custom-search/v1/reference/rest/v1/cse/list)
- 📑 [Create Google Search Engine](https://programmablesearchengine.google.com/about/)
- 📑 [Create Google Project](https://developers.google.com/)

---

## API

文档：📑 [Google Search API Documentation](https://developers.google.com/custom-search/v1/reference/rest/v1/cse/list)

请求参数：

- `cx`：The Programmable Search Engine ID
- `dateRestrict`：检索日期范围，`m1` 表示最近一个月，`w2` 表示最近两周
- `num`：单次请求返回结果数量，取值范围 `1~10`，10 是最大值
- `q`：搜索关键词
- `start`：分页搜索偏移量，如果第一页返回了 10 个结果，`start=11` 表示开始搜索第二页

---

## 代码实现

上一节的视频中给出了代码实现，仅依赖 Request（Pandas 可以不依赖）。在本节中，我将视频中的代码录入如下：

```python
import re
import requests
import pandas as pd

def build_payload(query, start=1, num=10, date_restrict='m1', **params):
	"""
	Function to build the payload for the Google Search API request.

	:param query: Search term
	:param start: The index of the first results to return
	:param link_site: Specifies that all search results should contain a link to a particular URL
	:param search_type: Type of search (default is undefined, 'IMAGE' for image search)
	:param date_restrict: Restricts results based on recency (default is one month 'm1')
	:param params: Additional parameters for the API request

	:return: Dictionary containing the API request parameters
	"""
	payload = {
		'key': API_KEY,
		'q': query,
		'cx': SEARCH_ENGINE_ID,
		'start': start,
		'num': num,
		'dateRestrict': date_restrict
	}
	payload.update(params)
	return payload

def make_request(payload):
	"""
	Function to send a GET request to the Google Search API and handle potential errors.

	:param payload: Dictionary containing the API request parameters
	:return: JSON response from the API
	"""
	response = requests.get('https://www.googleapis.com/customsearch/v1', params=payload)
	if response.status_code != 200:
		raise Exception('Request failed')
	return response.json()

def main(query, result_total=10):
	"""
	Main function to execute the script
	"""
	items = []
	reminder = result_total % 10
	if remainder > 0:
		pages = (result_total // 10) + 1
	else:
		pages = result_total // 10

	for i in range(pages):
		if pages == i + 1 and reminder > 0:
			payload = build_payload(query, start=(i+1)*10, num=reminder)
		else:
			payload = build_payload(query, start=(i+1)*10)
		response = make_request(payload)
		items.extends(response['items'])
	query_string_clean = clean_filename(query)
	# save items to file using pandas
```

---

## 返回值

在接口返回中，有一个 `items` 字段，里面包含返回结果。其中每个元素字段：

- `kind`
- `title`：标题
- `htmlTitle`
- `link`：url
- `displayLink`：站点域名
- `snippet`：描述
- `htmlSnippet`
- `formattedUrl`
- `htmlFormattedUrl`
- `pagemap`
	- `cse_thumbnail`：缩略图，列表，内部格式（`src`, `width`, `height`），走 Google 服务器
	- `cse_image`：图像原图，列表，内部格式（`src`)，走文章网页自己的 URL 地址

---

## 其他网络资料

[Programmatically searching google in Python using custom search - Stack Overflow](https://stackoverflow.com/questions/37083058/programmatically-searching-google-in-python-using-custom-search)

[What are the alternatives now that the Google web search API has been deprecated? - Stack Overflow](https://stackoverflow.com/questions/4082966/what-are-the-alternatives-now-that-the-google-web-search-api-has-been-deprecated/11206266#11206266)

[googleapis/google-api-python-client: 🐍 The official Python client library for Google's discovery based APIs.](https://github.com/googleapis/google-api-python-client)
[bisohns/search-engine-parser: Lightweight package to query popular search engines and scrape for result titles, links and descriptions](https://github.com/bisohns/search-engine-parser)

[web scraping - Is it ok to scrape data from Google results? - Stack Overflow](https://stackoverflow.com/questions/22657548/is-it-ok-to-scrape-data-from-google-results#22703153)


