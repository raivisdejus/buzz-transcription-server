# Buzz transcription server

Server to show live transcripts from [Buzz](https://github.com/chidiwilliams/buzz) on the web. 

You can host this on free version of [render.com](https://render.com/)

To protect your transcripts from an unauthorized upload set the environment variable `UPLOAD_PASSWORD` in the hosting panel and add it to the Buzz `BUZZ_UPLOAD_URL` configuration f.e. `http://localhost:5000/upload?password=topSecret`. Transcript uploads for Buzz are configured via [advanced preferences](https://chidiwilliams.github.io/buzz/docs/preferences#advanced-preferences)