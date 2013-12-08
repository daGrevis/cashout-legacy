$ ->
    $title = $("[name='title']")
    $title.selectize
        create: true
        maxItems: 1
        load: (query, callback) ->
            return unless query.length
            $.getJSON "/payment_titles/?query=#{ query }", (response) ->
                callback $.map response.titles, text_to_selectize_object
        onChange: (value) ->
            $.getJSON "/payment_guess/?title=#{ value }", (response) ->
                return unless response
                $("[name='price']").val response.price
                $tags = $("[name='tags']")
                $tags.val response.tags
                $tags.trigger "change"
