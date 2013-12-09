ISO_8601_DATEFORMAT_PLACEHOLDER = "YYYY-MM-DD HH:mm:ss" # W/o timezone.
DELAY_BEFORE_HIDE_ALERTS = 1000 * 10

delay = (ms, callable) -> setTimeout callable, ms

window.text_to_selectize_object = (title) -> value: title, text: title

NProgress.configure trickle: false, speed: 200

$(document).ready ->
    NProgress.start()

    Ladda.bind(".ladda-button")

    $("[name='tags']").selectize
        create: true
        load: (query, callback) ->
            if not query.length
                return callback()
            $.getJSON "/payment_tags/?query=#{ query }", (response) ->
                callback $.map response.tags, text_to_selectize_object

    $(".confirm").click (event) ->
        $el = $(@)
        event.preventDefault()
        bootbox.confirm "Are you really sure? It can't be undone.", (result) ->
            if result
                location.href = $el.attr "href"

    $(".clickable_row").click ->
        location.href = $("td > a", @).prop("href")

    $("[name='created']").datetimepicker format: ISO_8601_DATEFORMAT_PLACEHOLDER

    $(".alert").click (event) ->
        $(@).slideUp()

    delay DELAY_BEFORE_HIDE_ALERTS, -> $(".alert").slideUp()

$(window).load ->
    NProgress.done()
