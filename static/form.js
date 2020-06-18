$(function() {
    // Remove button click
    $(document).on(
        'click',
        '[data-role="dynamic-fields"] > .form-inline [data-role="remove"]',
        function(e) {
            e.preventDefault();
            $(this).closest('.form-inline').remove();
        }
    );
    // Add button click
    $(document).on(
        'click',
        '[data-role="dynamic-fields"] > .form-inline [data-role="add"]',
        function(e) {
            e.preventDefault();
            var container = $(this).closest('[data-role="dynamic-fields"]');
            new_field_group = container.children().filter('.form-inline:first-child').clone();
            new_field_group.find('input').each(function(){
                $(this).val('');
            });
            container.append(new_field_group);
        }
    );
    // generate
    document.onkeyup = function(e) {
        var container = $('[data-role="dynamic-fields"]');
        var listOfObjects = [];
        container.children().each(function(){
            let obj = {
                key: $(this).find('input#field-key').val(),
                title: $(this).find('input#field-title').val(),
                description: $(this).find('input#field-desc').val(),
                dependencies: $(this).find('input#field-dependencies').val(),
                start_date: $(this).find('input#field-start').val(),
                duration: $(this).find('input#field-duration').val(),
                resource: $(this).find('input#field-resource').val(),
            }
            listOfObjects.push(obj);
        })
        console.log("length of " + listOfObjects.length)
        var data = {
            title : "Gantt Chart",
            items : listOfObjects
        }
        var encoded = JSON.stringify(data)
        encoded = btoa(encoded);
        $("#generatedBase").val(encoded);
        $("#generatedJSON").val(JSON.stringify(data));
    }
});

