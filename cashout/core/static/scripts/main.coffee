NProgress.configure trickle: false, speed: 200

$(document).ready ->
    NProgress.start()

    Ladda.bind("button.ladda-button")

    $("[name='tags']").select2
        tags: []
        width: "resolve"
        tokenSeparators: [","]

$(window).load ->
    NProgress.done()
