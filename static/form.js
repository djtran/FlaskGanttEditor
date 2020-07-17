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
        generate();
    }
});

function generate() {
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
        title : $("#titleText").val(),
        items : listOfObjects
    }
    var asString = JSON.stringify(data)
    var encoded = btoa(asString);
    $("#generatedBase").val(encoded);
    $("#generatedJSON").val(asString);
}

function importFromFile() {
    const input = document.getElementById('jsonReloadFile')
    if (input) {
        const file = input.files[0];
        let reader = new FileReader();
        reader.addEventListener('load', (event) => {
            const data = JSON.parse(reader.result);
            console.log(data)

            $("#titleText").val(data['title']);

            var container = $("#theForm");
            var field_group = container.children().filter('.form-inline:first-child').clone();
            for (const item of data['items']) {
                new_field_group = field_group.clone();
                new_field_group.find('input').each(function(){
                    $(this).val('');
                });

                if (item['key']) new_field_group.find('input#field-key').val(item['key']);
                if (item['title']) new_field_group.find('input#field-title').val(item['title']);
                if (item['description']) new_field_group.find('input#field-desc').val(item['description']);
                if (item['dependencies']) new_field_group.find('input#field-dependencies').val(item['dependencies']);
                if (item['start_date']) new_field_group.find('input#field-start').val(item['start_date']);
                if (item['duration']) new_field_group.find('input#field-duration').val(item['duration']);
                if (item['resource']) new_field_group.find('input#field-resource').val(item['resource']);
                
                container.append(new_field_group);
            }
            generate();
        })
        reader.readAsText(file);
    }
}

function saveToFile() {
    const input = $('#generatedJSON').val();
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(input));
    element.setAttribute('download', "gantt.json");

    element.style.display = 'none';
    document.body.appendChild(element);

    element.click();

    document.body.removeChild(element);
}