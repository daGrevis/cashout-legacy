ISO_8601_DATEFORMAT_PLACEHOLDER = "YYYY-MM-DD HH:mm:ss" # W/o timezone.

window.text_to_select2_object = (text) -> id: text, text: text

NProgress.configure trickle: false, speed: 200

$(document).ready ->
    NProgress.start()

    Ladda.bind(".ladda-button")

    $("[name='tags']").select2
        width: "resolve"
        tokenSeparators: [","]
        tags: true
        ajax:
            url: "/payment_tags/"
            dataType: "json"
            data: (term) -> query: term
            results: (data) -> results: $.map data.tags, text_to_select2_object
        initSelection: ($tag, callback) -> callback $.map (($tag.val()).split ","), text_to_select2_object
        createSearchChoice: text_to_select2_object

    $(".confirm").click (event) ->
        $el = $(@)
        event.preventDefault()
        bootbox.confirm "Are you really sure? It can't be undone.", (result) ->
            if result
                location.href = $el.attr "href"

    $(".clickable_row").click ->
        location.href = $("td > a", @).prop("href")

    $("[name='created']").datetimepicker format: ISO_8601_DATEFORMAT_PLACEHOLDER

$(window).load ->
    NProgress.done()
