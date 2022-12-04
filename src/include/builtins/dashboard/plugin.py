# from ez import ez
import ez


@ez.get("/page/{page}")
def on_page(page: str):
    ez.response.html(f"Page: {page}")
    print("Page:", page)
