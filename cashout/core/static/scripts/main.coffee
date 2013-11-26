$ ->
    Ladda.bind("button.ladda-button")

    $("[name='tags']").select2
        tags: []
        width: "resolve"
        tokenSeparators: [","]
