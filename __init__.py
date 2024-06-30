import Wikipedia_Searcher as WS
from typing import Any
from flask import *

SERVER: Flask = Flask(__name__)


@SERVER.route("/")
def HOME() -> str:
    return render_template("index.html")


@SERVER.route("/findHtml", methods=['GET', 'POST'])
def Search() -> bytes:
    TITLE = str(request.form.get("TITLE"))
    ARTICAL_HTML: bytes = WS.Find_HTML(TITLE)

    return ARTICAL_HTML


@SERVER.route("/Related_Pages", methods=['GET', 'POST'])
def Related_Pages() -> str:
    TITLE = str(request.form.get("TITLE"))
    RELATED_PAGES: str = WS.Related_titles(TITLE)
    
    return f"{RELATED_PAGES}"


@SERVER.route("/Summary", methods=['GET', 'POST'])
def Summary_Page() -> Any:
    TITLE = str(request.form.get("TITLE"))
    Summary: Any = WS.Summary(TITLE)

    return f"{Summary}"


@SERVER.route("/News", methods=['GET', 'POST'])
def News() -> Any:
    news: Any = WS.Current_News()

    return f"{news}"

if __name__ == "__main__":
    SERVER.run(debug=True)