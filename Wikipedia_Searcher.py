from typing import Any
import requests

# API Endpoint
url: str = "https://en.wikipedia.org/api/rest_v1"
# Bootstrap Url For Beautifying Some Of The pages
BOOTSTRAP_URL: str = """<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css"integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" crossorigin="anonymous">"""

# Finding The Html( Or The Whole Artical With Images, lists and other html componenets ) For The Given Title
def Find_HTML(title: str) -> bytes:
    try:
        # Editing The Title So The API Url Can Read It
        title: str = str(title.replace(" ", "_", -1).lower())
        Find_HTML_URL: str = f"{url}/page/html/{title}"
        Response: requests.Response = requests.request("GET", Find_HTML_URL)
        # Getting The Response Content ( HTML )
        Html_Data: bytes = Response.content

    # If There Is An Spellig Error Then The Server Would Return A key error Because It Couldn't Find The Requested URL
    except KeyError:
        return f"{BOOTSTRAP_URL} <body class='bg-dark text-light'><h1> -- Page Not Found, Maybe There Is A Spelling Error ! -- </h1></body>"

    return Html_Data

# Finding The Related Pages
def Related_titles(title: str) -> str:
    try:
        # Editing The Title So The API Url Can Read It
        title: str = str(title.replace(" ", "_", -1).lower())
        Related_titles_URL: str = f"{url}/page/related/{title}"
        Response: requests.Response = requests.request("GET", Related_titles_URL)
        # List Of Related Urls
        URLS = []

        Data = Response.json()
        # Getting The Lenght Of Pages Returned For Iteration
        Pages_Length = len(list(Data["pages"]))
        # Iterating Through The Data And Adding The Url To The List Of Related URLS
        for i in range(Pages_Length - 1):
            data = Data["pages"][i]["content_urls"]["desktop"]["page"]
            URLS.append(data)
            i += 1

        html = ""

        for i in range(len(URLS)):
            html = html + "<br>" + f"<a href={URLS[i]}>{URLS[i]}</a>"
    # If There Is An Spellig Error Then The Server Would Return A key error Because It Couldn't Find The Requested URL Or the Wanted Key In The Dictionary
    except KeyError:
        return f"{BOOTSTRAP_URL} <body class='bg-dark text-light'><h1> -- Page Not Found, Maybe There Is A Spelling Error ! -- </h1></body>"

    return html

# Getting The Summary Of A Title
def Summary(title: str) -> Any:
    try:
        # Editing The Title So The API Url Can Read It
        title: str = str(title.replace(" ", "_", -1).lower())
        Page_Summary_URL: str = f"{url}/page/summary/{title}"
        Response: requests.Response = requests.get(Page_Summary_URL)

        JsonData = Response.json()
        # Getting The Wanted Data From The Json
        URL: str = str(JsonData["content_urls"]["desktop"]["page"])
        DISPLAY_TITLE: str = str(JsonData["displaytitle"])
        DESCRIPTION: str = str(JsonData["description"])
        SUMMARY_HTML: str = str(JsonData["extract_html"])
    # If There Is An Spellig Error Then The Server Would Return A key error Because It Couldn't Find The Requested URL Or the Wanted Key In The Dictionary    
    except KeyError:
        return f"{BOOTSTRAP_URL} <body class='bg-dark text-light'><h1> -- Page Not Found, Maybe There Is A Spelling Error ! -- </h1></body>"

    # Beautifying The Data And Html
    return f"""{BOOTSTRAP_URL} <body class='bg-dark text-light'>
        <br>
        <a href={URL}>{URL}</a>
        <br>
        <br>
        {DISPLAY_TITLE}
        <br>
        <br>
        {DESCRIPTION}
        <br>
        <br>
        {SUMMARY_HTML}</body>"""

# Getting The Current Announcements
def Current_News() -> Any:
    try :
        Current_News_Url: str = f"{url}/feed/announcements"
        Response: requests.Response = requests.get(Current_News_Url)

        Json_Data = Response.json()
        Announcements = Json_Data["announce"]

        HTML = ""
        # Beautifying The Returned Data
        for i in range(len(Announcements)):
            HTML = HTML + "<br>" + f"{Announcements[i]}" 
    # If There Is No Announcements then When We Want To Iterate Through The List The Program Would Throw An Error
    except IndexError:
        return f"{BOOTSTRAP_URL} <body class='bg-dark text-light'><h1> -- No Announcements Today -- </h1></body>"
    # If There Is An Spellig Error Then The Server Would Return A key error Because It Couldn't Find The Requested URL Or the Wanted Key In The Dictionary
    except KeyError:
        return f"{BOOTSTRAP_URL} <body class='bg-dark text-light'><h1> -- Page Not Found, Maybe There Is A Spelling Error ! -- </h1></body>"
    # If The HTML Was Empty It Means That There Is No Announcements
    if HTML == "":
        return f"{BOOTSTRAP_URL} <body class='bg-dark text-light'><h1> -- No Announcements Today -- </h1></body>"
    
    else:
        return HTML
    