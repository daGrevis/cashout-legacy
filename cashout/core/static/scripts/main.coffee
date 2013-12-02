NProgress.configure trickle: false, speed: 200

$(document).ready ->
    NProgress.start()

    Ladda.bind("button.ladda-button")

    $("[name='tags']").select2
        tags: []
        width: "resolve"
        tokenSeparators: [","]

    $(".confirm").click (event) ->
        $el = $(@)
        event.preventDefault()
        bootbox.confirm "Are you really sure? It can't be undone.", (result) ->
            if result
                location.href = $el.attr "href"

    $(".clickable_row").click ->
        location.href = $("td > a", @).prop("href")

$(window).load ->
    NProgress.done()
