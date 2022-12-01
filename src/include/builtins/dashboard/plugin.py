from ez import Ez


@Ez.get("/page/{page}")
def on_page(page: str):
    Ez.response.html(f"Page: {page}")
    print("Page:", page)
