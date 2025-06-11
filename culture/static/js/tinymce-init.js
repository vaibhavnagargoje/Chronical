document.addEventListener('DOMContentLoaded', function() {
    // Initialize only when ParagraphBlock is visible
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
});