$ ->
    $title = $("[name='title']")
    $title.select2
        width: "resolve"
        ajax:
            url: "/payment_titles/"
            dataType: "json"
            data: (title) -> query: title
            results: (data) -> results: $.map data.titles, text_to_select2_object
        createSearchChoice: text_to_select2_object
    $title.on "change", (event) ->
        title = event.added["text"]
        $.getJSON "/payment_guess/?title=#{ title }", (response) ->
            if not response
                return
            $("[name='price']").val response.price
            $tags = $("[name='tags']")
            $tags.val response.tags
            $tags.trigger "change"
