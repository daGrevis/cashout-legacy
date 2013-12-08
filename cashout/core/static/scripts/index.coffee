$ ->
    $("[name='title']").selectize
        create: true
        maxItems: 1
        load: (query, callback) ->
            return unless query.length
            $.getJSON "/payment_titles/?query=#{ query }", (response) ->
                callback $.map response.titles, text_to_selectize_object
        onChange: (value) ->
            $.getJSON "/payment_guess/?title=#{ value }", (response) ->
                $price = $("[name='price']")
                selectize_tags = $("[name='tags']")[0].selectize
                $price.val ""
                selectize_tags.clear()
                return unless response
                $price.val response.price
                $.each response.tags, (i, tag) ->
                    selectize_tags.addOption text_to_selectize_object tag
                    selectize_tags.addItem tag
