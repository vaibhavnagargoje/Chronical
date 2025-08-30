document.addEventListener('DOMContentLoaded', function() {
    // Initialize for ParagraphBlock
    const observer = new MutationObserver(function(mutations) {
        if (document.querySelector('.paragraphblock')) {
            tinymce.init({
                selector: '#id_content',
                setup: function(editor) {
                    editor.on('init', function() {
                        // Performance tweak
                        editor.settings.autoresize_bottom_margin = 10;
                        editor.plugins.autoresize.resize();
                    });
                }
            });
            observer.disconnect();
        }
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });

    // Initialize for project editing if textarea exists
    if (document.getElementById('id_text')) {
        tinymce.init({
            selector: '#id_text',
            plugins: 'advlist autolink lists link image charmap print preview hr anchor pagebreak searchreplace wordcount visualblocks visualchars code fullscreen insertdatetime media nonbreaking save table contextmenu directionality emoticons template paste textcolor colorpicker textpattern imagetools codesample toc',
            toolbar1: 'undo redo | insert | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image',
            toolbar2: 'print preview media | forecolor backcolor emoticons | codesample',
            image_advtab: true,
            height: 400,
            menubar: false,
            branding: false,
            content_style: 'body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }'
        });
    }
});