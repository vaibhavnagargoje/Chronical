// document.addEventListener('DOMContentLoaded', function () {
//   // Word definitions dictionary
//   const wordDefinitions = {
//     "features": "A Swiss architectural historian and critic known for his influential writings on modern architecture",
//     "mandirs": "Hindu temples or places of worship",
//     "mandir": "A Hindu temple or place of worship",
//     "Jyotirlinga": "A sacred shrine where Shiva is worshipped in the form of a light pillar",
//     "shikhara": "The rising tower or spire above the main shrine in Hindu temple architecture",
//     "garbhagriha": "The innermost sanctum of a Hindu temple where the main deity is housed"
//   };


document.addEventListener('DOMContentLoaded', function () {
  // NEW: Dynamically load definitions from the HTML
  let wordDefinitions = {}; 
  const dataElement = document.getElementById('side-panel-data');
  
  if (dataElement) {
    try {
      // Parse the JSON data provided by the Django template tag
      wordDefinitions = JSON.parse(dataElement.textContent);
    } catch (e) {
      console.error("Error parsing side panel data:", e);
    }
  }

  // If there are no definitions for this chapter, stop right here.
  if (Object.keys(wordDefinitions).length === 0) {
    return;
  }
 
  function highlightWords() {
    const paragraphs = document.querySelectorAll('.prose p');

    paragraphs.forEach(paragraph => {
      let content = paragraph.innerHTML;
      content = content.replace(/<span class="word-highlight(.*?)>(.*?)<\/span>/gi, '$2');

      Object.keys(wordDefinitions).forEach(word => {
        const regex = new RegExp(`\\b(${word})\\b`, 'gi');
        content = content.replace(regex, function (match) {
          return `<span class="word-highlight" data-word="${word}" style="color: #863F3F; font-weight: 500; text-decoration: underline; text-decoration-color: #DAB20C; text-decoration-thickness: 2px; cursor: pointer; transition: all 0.2s ease;">${match}</span>`;
        });
      });

      paragraph.innerHTML = content;
    });
  }

  // Function to create and show the popup tooltip
  function showPopup(word, definition, clickEvent) {
    // Remove any existing popup
    const existingPopup = document.getElementById('definition-popup');
    if (existingPopup) existingPopup.remove();

    // Create the popup
    const popup = document.createElement('div');
    popup.id = 'definition-popup';
    popup.className = 'absolute z-50';
    popup.style.cssText = `
      background: white;
      border: 1px solid #863F3F;
      border-radius: 8px;
      box-shadow: 0 4px 20px rgba(134, 63, 63, 0.15);
      padding: 16px 20px;
      max-width: 320px;
      font-size: 14px;
      line-height: 1.5;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      transform: translateY(-5px);
      opacity: 0;
      animation: popupFadeIn 0.2s ease-out forwards;
    `;

    popup.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px;">
        <h4 style="margin: 0; font-size: 16px; font-weight: 600; color: #863F3F; flex: 1;">${word}</h4>
        <button id="close-popup" style="border: none; background: none; font-size: 18px; color: #6b7280; cursor: pointer; padding: 0; margin-left: 12px; line-height: 1; transition: color 0.2s ease;" onmouseover="this.style.color='#863F3F'" onmouseout="this.style.color='#6b7280'">×</button>
      </div>
      <div style="height: 1px; background: linear-gradient(to right, #DAB20C, transparent); margin-bottom: 12px;"></div>
      <p style="margin: 0; color: #374151; text-align: justify; font-size: 13px;">${definition}</p>
    `;

    // Add CSS animation
    if (!document.getElementById('popup-styles')) {
      const style = document.createElement('style');
      style.id = 'popup-styles';
      style.textContent = `
        @keyframes popupFadeIn {
          from { opacity: 0; transform: translateY(-10px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .word-highlight:hover {
          background-color: rgba(218, 178, 12, 0.1) !important;
          text-decoration-thickness: 3px !important;
        }
      `;
      document.head.appendChild(style);
    }

    // Position the popup near the clicked element
    const rect = clickEvent.target.getBoundingClientRect();
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    const scrollLeft = window.pageXOffset || document.documentElement.scrollLeft;

    // Calculate initial position
    let top = rect.bottom + scrollTop + 8;
    let left = rect.left + scrollLeft;

    // Append to body first to get dimensions
    document.body.appendChild(popup);
    const popupRect = popup.getBoundingClientRect();

    // Adjust position if popup goes outside viewport
    if (left + popupRect.width > window.innerWidth) {
      left = window.innerWidth - popupRect.width - 16;
    }
    
    if (top + popupRect.height > window.innerHeight + scrollTop) {
      top = rect.top + scrollTop - popupRect.height - 8;
    }

    // Ensure popup doesn't go off the left edge
    if (left < 16) {
      left = 16;
    }

    // Apply final position
    popup.style.left = left + 'px';
    popup.style.top = top + 'px';

    // Add event listener to close button
    document.getElementById('close-popup').addEventListener('click', function () {
      popup.style.animation = 'popupFadeIn 0.15s ease-out reverse';
      setTimeout(() => popup.remove(), 150);
    });

    // Close popup when clicking outside
    setTimeout(() => {
      document.addEventListener('click', function closeOutside(event) {
        if (!popup.contains(event.target) && !event.target.classList.contains('word-highlight')) {
          popup.style.animation = 'popupFadeIn 0.15s ease-out reverse';
          setTimeout(() => popup.remove(), 150);
          document.removeEventListener('click', closeOutside);
        }
      });
    }, 100);
  }

  // Highlight all defined words
  highlightWords();

  // Add click listeners to all highlighted words
  document.addEventListener('click', function (event) {
    if (event.target.classList.contains('word-highlight')) {
      event.preventDefault();
      event.stopPropagation();
      
      const word = event.target.getAttribute('data-word');
      if (word && wordDefinitions[word]) {
        showPopup(word, wordDefinitions[word], event);
      }
    }
  });

  // Close popup on escape key
  document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape') {
      const popup = document.getElementById('definition-popup');
      if (popup) {
        popup.style.animation = 'popupFadeIn 0.15s ease-out reverse';
        setTimeout(() => popup.remove(), 150);
      }
    }
  });
});


