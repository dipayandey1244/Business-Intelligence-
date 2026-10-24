# Deploy on Streamlit Community Cloud

1. Open https://share.streamlit.io/ and sign in with GitHub.
2. Choose **Create app**, repository `dipayandey1244/Business-Intelligence-`, branch `main`, and main file `app.py`.
3. Deploy. The dashboard works without an API key.
4. For optional AI analysis, open the app settings → **Secrets** and add:

```toml
GROQ_API_KEY = "your-rotated-key"
GROQ_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
```

Never commit the actual key to GitHub. A previously exposed key should be revoked and replaced before use.

## Safety boundary
This project is synthetic and educational. It is not affiliated with HSBC and is not suitable for real client decisions without appropriate governance, data approvals, validation, privacy and security reviews.
