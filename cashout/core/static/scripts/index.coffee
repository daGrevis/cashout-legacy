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
