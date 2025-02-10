from pytube import YouTube
import yt_dlp

# yt = YouTube()
# title = yt.title


# print(title)

link = "https://youtube.com/watch?v=vTuL2_4VOBA"
def yt_title(link):
    try:
        ydl_opts = {}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=False)
            return info.get("title", "Title not found")
    except Exception as e:
        return f"Error: {str(e)}"
    

title = yt_title(link)

# print(title)

# url = "https://youtube.com/watch?v=vTuL2_4VOBA"

# ydl_opts = {}
# with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#     info = ydl.extract_info(url, download=False)
#     print("Title:", info.get("title"))