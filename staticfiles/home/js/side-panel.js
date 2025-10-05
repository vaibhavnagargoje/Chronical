document.addEventListener('DOMContentLoaded', function () {
  console.log("Side panel script loaded");
  
  // Word definitions dictionary
  // home side panel
const definitionsDataElement = document.getElementById('side-panel-definitions');
  const wordDefinitions = definitionsDataElement
    ? JSON.parse(definitionsDataElement.textContent)
    : {};
  
  console.log("Word definitions loaded:", Object.keys(wordDefinitions).length, "terms");

  // Function to find and highlight all words in the content - FIXED VERSION
  function highlightWords() {
    // Inject CSS once (same styling as previous inline style)
    if (!document.getElementById('word-highlight-style')) {
      const style = document.createElement('style');
      style.id = 'word-highlight-style';
      style.textContent = `
        .word-highlight {
          color: #863F3F;
          font-weight: 400;
          // text-decoration: underline;
          // text-decoration-color: #DAB20C;
          text-decoration-thickness: 1px;
          cursor: pointer;
          transition: all 0.2s ease;
        }
        // .word-highlight:hover {
        //   // background-color: rgba(218, 178, 12, 0.1);
        //   // text-decoration-thickness: 3px;
        // }
      `;
      document.head.appendChild(style);
    }

    const containers = document.querySelectorAll('.district-intro');
    containers.forEach(container => {
      if (container.classList.contains('no-highlight') || container.closest('.no-highlight')) {
        return;
      }
      if (container.querySelector('.word-highlight')) return;
      highlightWordsInNode(container);
    });
  }

  // Helper: escape regex special chars
  function escapeRegex(str) {
    return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }

  // Build one combined regex (longest phrases first to avoid partial overshadow)
  const highlightPhrases = Object.keys(wordDefinitions).sort((a,b)=> b.length - a.length);
  const combinedPattern = highlightPhrases.map(escapeRegex).join('|');
  const hasHighlightable = combinedPattern ? new RegExp(combinedPattern, 'i') : null;

  // Safe DOM-based highlighter (no innerHTML mutation)
  function highlightWordsInNode(root) {
    if (!hasHighlightable) return;

    const walker = document.createTreeWalker(
      root,
      NodeFilter.SHOW_TEXT,
      {
        acceptNode: function(textNode) {
          const parent = textNode.parentNode;
            // Skip if inside existing highlight or script/style/pre/code
          if (!parent) return NodeFilter.FILTER_REJECT;
          const tag = parent.nodeName.toLowerCase();
          if (parent.classList && parent.classList.contains('word-highlight')) return NodeFilter.FILTER_REJECT;
          if (['script','style','code','pre','noscript'].includes(tag)) return NodeFilter.FILTER_REJECT;
          if (!hasHighlightable.test(textNode.textContent)) return NodeFilter.FILTER_REJECT;
          return NodeFilter.FILTER_ACCEPT;
        }
      }
    );

    const toProcess = [];
    let node;
    while ((node = walker.nextNode())) {
      toProcess.push(node);
    }

    toProcess.forEach(textNode => {
      const original = textNode.textContent;
      // Fresh regex per node to avoid lastIndex side effects
      const regex = new RegExp(`\\b(${combinedPattern})\\b`, 'gi');
      let matchFound = false;
      const frag = document.createDocumentFragment();
      let lastIndex = 0;

      original.replace(regex, (match, p1, offset) => {
        matchFound = true;
        if (offset > lastIndex) {
          frag.appendChild(document.createTextNode(original.slice(lastIndex, offset)));
        }
        const span = document.createElement('span');
        // Retrieve canonical key (case-insensitive match)
        const key = highlightPhrases.find(k => k.toLowerCase() === match.toLowerCase());
        span.className = 'word-highlight';
        span.dataset.word = key || match;
        span.textContent = match;
        frag.appendChild(span);
        lastIndex = offset + match.length;
        return match;
      });

      if (!matchFound) return;

      if (lastIndex < original.length) {
        frag.appendChild(document.createTextNode(original.slice(lastIndex)));
      }

      textNode.parentNode.replaceChild(frag, textNode);
    });
  }

  // Function to truncate text to specified word count
  function truncateText(text, wordLimit) {
    const words = text.trim().split(/\s+/);
    if (words.length <= wordLimit) {
      return { truncated: text, isTruncated: false };
    }
    return {
      truncated: words.slice(0, wordLimit).join(' ') + '...',
      isTruncated: true,
      full: text
    };
  }

  // Function to create and show the popup tooltip
  function showPopup(word, definition, clickEvent) {
    // Remove any existing popup
    const existingPopup = document.getElementById('definition-popup');
    if (existingPopup) existingPopup.remove();

    const textData = truncateText(definition, 50);

    // Create the popup
    const popup = document.createElement('div');
    popup.id = 'definition-popup';
    popup.className = 'absolute z-1';
    popup.style.cssText = `
      background: white;
      border: 1px solid #863F3F;
      border-radius: 8px;
      box-shadow: 0 4px 20px rgba(134, 63, 63, 0.15);
      padding: 16px 20px;
      max-width: 320px;
      max-height: 400px;
      font-size: 14px;
      line-height: 1.5;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      transform: translateY(-5px);
      opacity: 0;
      animation: popupFadeIn 0.2s ease-out forwards;
    `;

    const readMoreButton = textData.isTruncated ? 
      `<button id="read-more-btn" style="color: #863F3F; background: none; border: none; text-decoration: underline; cursor: pointer; font-size: 12px; margin-top: 8px; padding: 0;">Read more</button>` : '';

    popup.innerHTML = `
      <div style="display: flex; justify; align-items: flex-start; margin-bottom: 10px;">
        <h4 style="margin: 0; font-size: 16px; font-weight: 600; color: #863F3F; flex: 1;">${word}</h4>
        <button id="close-popup" style="border: none; background: none; font-size: 18px; color: #6b7280; cursor: pointer; padding: 0; margin-left: 12px; line-height: 1; transition: color 0.2s ease;" onmouseover="this.style.color='#863F3F'" onmouseout="this.style.color='#6b7280'">×</button>
      </div>
      <div style="height: 1px; background: linear-gradient(to right, #DAB20C, transparent); margin-bottom: 12px;"></div>
      <div id="definition-content" style="overflow-y: auto; max-height: 300px;">
        <p id="definition-text" style="margin: 0; color: #374151; font-size: 13px;">${textData.truncated}</p>
        ${readMoreButton}
      </div>
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
        #definition-content {
          padding-right: 12px;
          box-sizing: border-box;
        }
        #definition-content::-webkit-scrollbar {
          width: 6px;
        }
        #definition-content::-webkit-scrollbar-track {
          background: #f1f1f1;
          border-radius: 3px;
          margin: 4px 0;
        }
        #definition-content::-webkit-scrollbar-thumb {
          background: #DAB20C;
          border-radius: 3px;
        }
        #definition-content::-webkit-scrollbar-thumb:hover {
          background: #b8940a;
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

    // Add event listener to read more button
    if (textData.isTruncated) {
      document.getElementById('read-more-btn').addEventListener('click', function(event) {
        event.preventDefault();
        event.stopPropagation();
        
        const definitionText = document.getElementById('definition-text');
        const readMoreBtn = document.getElementById('read-more-btn');
        definitionText.textContent = textData.full;
        readMoreBtn.remove();
      });
    }

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


