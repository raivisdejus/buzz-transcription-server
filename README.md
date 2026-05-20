# Buzz transcription server

Server to show live transcripts from [Buzz](https://github.com/chidiwilliams/buzz) on the web. 

You can host this on free version of [render.com](https://render.com/)

Command to start the server `python hosted-server.py`

To protect your transcripts from an unauthorized upload set the environment variable `UPLOAD_PASSWORD` in the hosting panel and add it to the Buzz `BUZZ_UPLOAD_URL` configuration f.e. `http://localhost:5000/upload?password=topSecret`. Transcript uploads for Buzz are configured via [advanced preferences](https://chidiwilliams.github.io/buzz/docs/preferences#advanced-preferences)

To print a debug notes in the server console when new entries get uploaded set `UPLOAD_DEBUG=1`

## Customizing the page

The following environment variables let you customize the client page without editing `client.html`:

- `SITE_TITLE` - Text shown in the browser tab (`<title>`) and the page `<h1>`. Defaults to `Buzz transcription server`.
- `TALK_TITLE` - Text shown in the `#talkTitle` element below the heading (used as the default/fallback talk title). Defaults to `Powered by Mozilla Common Voice data`.
- `SHOW_TRANSLATION` - Whether the translation pane is visible by default. Set to `1`, `true`, `yes`, or `on` to show translations on page load. Defaults to hidden. Users can always toggle visibility from the settings panel.
- `TRAFFIC_COUNTER_CODE` - Optional HTML/JS snippet injected verbatim at the bottom of the page (just before `</body>`). Use this to embed analytics or traffic-counter tags (e.g. Google Analytics, Plausible, a hit-counter `<img>`). Defaults to empty. Note: the value is inserted as raw HTML, so only set it to code you trust.
