# Local App

To run locally:

```powershell
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

# Knowledge Base Endpoints

You can now upload files or URLs to the knowledge base and query it:

- `POST /knowledge/upload` — Upload a file (form-data, field: `file`)
- `POST /knowledge/url` — Add a web page by URL (form field: `url`)
- `POST /knowledge/query` — Query the knowledge base (form field: `query`)

Example using `curl` to upload a file:

```sh
curl -F "file=@yourfile.txt" http://localhost:8000/knowledge/upload
```

Example to add a URL:

```sh
curl -F "url=https://example.com" http://localhost:8000/knowledge/url
```

Example to query:

```sh
curl -F "query=What is X?" http://localhost:8000/knowledge/query
```
