# BKMK
A chatGPT-powered web app to do Q&A with your bookmarks using retrieval augmented generation

### Motivation:
1. [My friend](https://www.linkedin.com/in/michael-agaby/) and I both have an overflowing knowledge base stored in our bookmarks. We wanted to have a Bing-like experience with that knowledge base
2. It's just one of those afternoons where two non-engineers want to build something :3


### What we built:
We built a quick and dirty prototype (in under 2 hours!) with the help of chatGPT. It's a locally hosted web app that will index website urls you add semantically based on its content, and answer any questions for you, similar to Bing but personalized to your own knowledge base. It has a lot of limitations (mainly in what it is able to index), but most of the techniques are quite transferrable if you are interested in expanding its capability.


### Techniques/Learnings:
- Ada-text-embedding-002 with a local store for semantic retrieval
- Segmentation and recursive summarization to fit long articles into chatgpt context window
- ChatGPT API + Prompt engineering to explain the task and enforce formatting
- Used chatGPT GENEROUSLY to learn, code, debug, and iterate (neither of us are engineers by trade)


### What you would need to use this:
- an OPENAI API key: https://openai.com/blog/openai-api, the home page of the web app will prompt you to enter it and you will bear the cost for the usage (embedding cost is basically negligible, our recursive summarizer is costing roughly 1c/query)


### enter API key

<img
  src="/img/Add_key.png" width=500>

### add article and article store

<img
  src="/img/add article.png"
  width=500>

<img
  src="/img/store.png"
  width=500>

### Different QA results:
<img
  src="/img/QA.png"
  width=400>

<img
  src="/img/did I.png"
  width=500>

<img
  src="/img/no answer.png"
  width=500>

<img
  src="/img/adjacent answer.png"
  width=500>


