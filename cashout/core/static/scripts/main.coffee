window.main = {}

MIDDLE_CLICK = 2

ISO_8601_DATEFORMAT_PLACEHOLDER = "YYYY-MM-DD HH:mm:ss" # W/o timezone.
DELAY_BEFORE_HIDE_ALERTS = 1000 * 10

window.main.get_csrf_token = ->
    $("#csrf_token").val()

# clrs.cc
window.main.color_names_to_colors =
    "navy": "#001f3f",
    "blue": "#0074d9",
    "aqua": "#7fdbff",
    "teal": "#39cccc",
    "olive": "#3d9970",
    "green": "#2ecc40",
    "lime": "#01ff70",
    "yellow": "#ffdc00",
    "orange": "#ff851b",
    "red": "#ff4136",
    "maroon": "#85144b",
    "fuchsia": "#f012be",
    "purple": "#b10dc9",
    "white": "#ffffff",
    "silver": "#dddddd",
    "gray": "#aaaaaa",
    "black": "#111111",

window.main.colors =
    ($.map window.main.color_names_to_colors, (value, key) -> value)

delay = (ms, callable) -> setTimeout callable, ms

window.text_to_selectize_object = (title) -> value: title, text: title

NProgress.configure trickle: false, speed: 200

$(document).ready ->
    NProgress.start()

    Ladda.bind(".ladda-button")

    $("[name='tags']").selectize
        plugins: [
            "remove_button",
            "restore_on_backspace",
        ]
        create: true
        load: (query, callback) ->
            if not query.length
                return callback()
            $.getJSON "/payment_tags/?query=#{ query }", (response) ->
                callback $.map response.tags, text_to_selectize_object

    $(".confirm").click (event) ->
        $el = $(@)
        event.preventDefault()
        bootbox.confirm "Are you really sure? It can't be undone.", (is_sure) ->
            if is_sure
                link = $el.attr "href"
                if link?
                    location.href = link
                else
                    $($el.parents "form").submit()

    $(".clickable_row").click (event) ->
        url = $("td > a", @).prop("href")
        if event.which == MIDDLE_CLICK
            window.open url, "_blank"
            return
        location.href = url

    $("[name='created']").datetimepicker format: ISO_8601_DATEFORMAT_PLACEHOLDER

    $(".alert").click (event) ->
        $(@).slideUp()

    delay DELAY_BEFORE_HIDE_ALERTS, -> $(".alert").slideUp()

$(window).load ->
    NProgress.done()
