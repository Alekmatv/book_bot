async def del_the_bookmark(del_page, bookmarks):

    for page, text in bookmarks:
        if del_page == page:
            delete = (page, text)
            break

    bookmarks.remove(delete)
