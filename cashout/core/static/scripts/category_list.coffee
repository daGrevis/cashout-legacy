$("#add_category").click (event) ->
    event.preventDefault()
    bootbox.prompt "How do you do?", (result) ->
        data =
            title: result
            csrfmiddlewaretoken: window.main.get_csrf_token()
        $.post "/categories/", data, ->
            location.reload()

$(".delete_category").click (event) ->
    event.preventDefault() # This does not work.
    $el = $(@)
    bootbox.confirm "Are you really sure? It can't be undone.", (is_sure) ->
        if is_sure
            category_pk = ($el.parents "tr").data "category_pk"
            category_url = "/categories/#{ category_pk }"
            data =
                csrf_token: window.main.get_csrf_token()
                delete: true
            $.get category_url, data, ->
                location.reload()
