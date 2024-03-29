$ ->
    $("[name='title']").selectize
        plugins: [
            "restore_on_backspace",
        ]
        create: true
        maxItems: 1
        load: (query, callback) ->
            return unless query.length
            $.getJSON "/payment_titles/?query=#{ query }", (response) ->
                callback $.map response.titles, text_to_selectize_object
        onChange: (value) ->
            $.getJSON "/payment_guess/?title=#{ value }", (response) ->
                $price = $("[name='price']")
                $tags = $("[name='tags']")
                selectize_tags = $tags[0].selectize
                return unless response
                if not $price.val()
                    $price.val response.price
                if not $tags.val()
                    $.each response.tags, (i, tag) ->
                        selectize_tags.addOption text_to_selectize_object tag
                        selectize_tags.addItem tag
