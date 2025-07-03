// // document.addEventListener('DOMContentLoaded', function () {
// //   // Word definitions dictionary
// //   const wordDefinitions = {
// //     "features": "A Swiss architectural historian and critic known for his influential writings on modern architecture",
// //     "mandirs": "Hindu temples or places of worship",
// //     "mandir": "A Hindu temple or place of worship",
// //     "Jyotirlinga": "A sacred shrine where Shiva is worshipped in the form of a light pillar",
// //     "shikhara": "The rising tower or spire above the main shrine in Hindu temple architecture",
// //     "garbhagriha": "The innermost sanctum of a Hindu temple where the main deity is housed"
// //   };


// document.addEventListener('DOMContentLoaded', function () {
//   // NEW: Dynamically load definitions from the HTML
//   let wordDefinitions = {}; 
//   const dataElement = document.getElementById('side-panel-data');
  
//   if (dataElement) {
//     try {
//       // Parse the JSON data provided by the Django template tag
//       wordDefinitions = JSON.parse(dataElement.textContent);
//     } catch (e) {
//       console.error("Error parsing side panel data:", e);
//     }
//   }

//   // If there are no definitions for this chapter, stop right here.
//   if (Object.keys(wordDefinitions).length === 0) {
//     return;
//   }
 
//   function highlightWords() {
//     const paragraphs = document.querySelectorAll('.prose p');

//     paragraphs.forEach(paragraph => {
//       let content = paragraph.innerHTML;
//       content = content.replace(/<span class="word-highlight(.*?)>(.*?)<\/span>/gi, '$2');

//       Object.keys(wordDefinitions).forEach(word => {
//         const regex = new RegExp(`\\b(${word})\\b`, 'gi');
//         content = content.replace(regex, function (match) {
//           return `<span class="word-highlight" data-word="${word}" style="color: #863F3F; font-weight: 500; text-decoration: underline; text-decoration-color: #DAB20C; text-decoration-thickness: 2px; cursor: pointer; transition: all 0.2s ease;">${match}</span>`;
//         });
//       });

//       paragraph.innerHTML = content;
//     });
//   }

//   // Function to create and show the popup tooltip
//   function showPopup(word, definition, clickEvent) {
//     // Remove any existing popup
//     const existingPopup = document.getElementById('definition-popup');
//     if (existingPopup) existingPopup.remove();

//     // Create the popup
//     const popup = document.createElement('div');
//     popup.id = 'definition-popup';
//     popup.className = 'absolute z-50';
//     popup.style.cssText = `
//       background: white;
//       border: 1px solid #863F3F;
//       border-radius: 8px;
//       box-shadow: 0 4px 20px rgba(134, 63, 63, 0.15);
//       padding: 16px 20px;
//       max-width: 320px;
//       font-size: 14px;
//       line-height: 1.5;
//       font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
//       transform: translateY(-5px);
//       opacity: 0;
//       animation: popupFadeIn 0.2s ease-out forwards;
//     `;

//     popup.innerHTML = `
//       <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px;">
//         <h4 style="margin: 0; font-size: 16px; font-weight: 600; color: #863F3F; flex: 1;">${word}</h4>
//         <button id="close-popup" style="border: none; background: none; font-size: 18px; color: #6b7280; cursor: pointer; padding: 0; margin-left: 12px; line-height: 1; transition: color 0.2s ease;" onmouseover="this.style.color='#863F3F'" onmouseout="this.style.color='#6b7280'">×</button>
//       </div>
//       <div style="height: 1px; background: linear-gradient(to right, #DAB20C, transparent); margin-bottom: 12px;"></div>
//       <p style="margin: 0; color: #374151; text-align: justify; font-size: 13px;">${definition}</p>
//     `;

//     // Add CSS animation
//     if (!document.getElementById('popup-styles')) {
//       const style = document.createElement('style');
//       style.id = 'popup-styles';
//       style.textContent = `
//         @keyframes popupFadeIn {
//           from { opacity: 0; transform: translateY(-10px); }
//           to { opacity: 1; transform: translateY(0); }
//         }
//         .word-highlight:hover {
//           background-color: rgba(218, 178, 12, 0.1) !important;
//           text-decoration-thickness: 3px !important;
//         }
//       `;
//       document.head.appendChild(style);
//     }

//     // Position the popup near the clicked element
//     const rect = clickEvent.target.getBoundingClientRect();
//     const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
//     const scrollLeft = window.pageXOffset || document.documentElement.scrollLeft;

//     // Calculate initial position
//     let top = rect.bottom + scrollTop + 8;
//     let left = rect.left + scrollLeft;

//     // Append to body first to get dimensions
//     document.body.appendChild(popup);
//     const popupRect = popup.getBoundingClientRect();

//     // Adjust position if popup goes outside viewport
//     if (left + popupRect.width > window.innerWidth) {
//       left = window.innerWidth - popupRect.width - 16;
//     }
    
//     if (top + popupRect.height > window.innerHeight + scrollTop) {
//       top = rect.top + scrollTop - popupRect.height - 8;
//     }

//     // Ensure popup doesn't go off the left edge
//     if (left < 16) {
//       left = 16;
//     }

//     // Apply final position
//     popup.style.left = left + 'px';
//     popup.style.top = top + 'px';

//     // Add event listener to close button
//     document.getElementById('close-popup').addEventListener('click', function () {
//       popup.style.animation = 'popupFadeIn 0.15s ease-out reverse';
//       setTimeout(() => popup.remove(), 150);
//     });

//     // Close popup when clicking outside
//     setTimeout(() => {
//       document.addEventListener('click', function closeOutside(event) {
//         if (!popup.contains(event.target) && !event.target.classList.contains('word-highlight')) {
//           popup.style.animation = 'popupFadeIn 0.15s ease-out reverse';
//           setTimeout(() => popup.remove(), 150);
//           document.removeEventListener('click', closeOutside);
//         }
//       });
//     }, 100);
//   }

//   // Highlight all defined words
//   highlightWords();

//   // Add click listeners to all highlighted words
//   document.addEventListener('click', function (event) {
//     if (event.target.classList.contains('word-highlight')) {
//       event.preventDefault();
//       event.stopPropagation();
      
//       const word = event.target.getAttribute('data-word');
//       if (word && wordDefinitions[word]) {
//         showPopup(word, wordDefinitions[word], event);
//       }
//     }
//   });

//   // Close popup on escape key
//   document.addEventListener('keydown', function (event) {
//     if (event.key === 'Escape') {
//       const popup = document.getElementById('definition-popup');
//       if (popup) {
//         popup.style.animation = 'popupFadeIn 0.15s ease-out reverse';
//         setTimeout(() => popup.remove(), 150);
//       }
//     }
//   });
// });






// side panal for only testing perpose ( static one )

document.addEventListener('DOMContentLoaded', function () {
  // Word definitions dictionary
  const wordDefinitions = {
  "traditional ":" only for testing",
    // 1
    "Improved sources of drinking water": " Improved Sources Of Drinking Water Include piped water, public taps, standpipes, tube wells, boreholes, protected dug wells and springs, rainwater, and community reverse osmosis (RO) plants.  ",
    // 2
    "Improved toilet facilities": " Improved Toilet Facilities Include any non-shared toilet of the following types: flush/pour flush toilets to piped sewer systems, septic tanks, and pit latrines; ventilated improved pit (VIP)/biogas latrines; pit latrines with slabs; and twin pit/composting toilets.  ",
    // 3
    "Net attendance ratio": " Net Attendance Ratio Percentage of the school-age population that attends primary or secondary school.  ",
    // 4
    "Gross attendance ratio": " Gross Attendance Ratio The total number of children attending primary school divided by the official primary school age population and the total number of children attending secondary school divided by the official secondary school age population.  ",
    // 5
    "Gender parity index": " Gender Parity Index The ratio of female to male children attending primary school and the ratio of female to male children attending secondary school. The index reflects the magnitude of the gender gap.  ",
    // 6
    "Literacy": " Literacy Respondents who have completed standard six or higher are assumed to be literate. All other respondents were given a sentence to read, and they were considered to be literate if they could read all or part of the sentence.  ",
    // 7
    "Total fertility rate": " Total Fertility Rate The average number of children a woman would have by the end of her childbearing years if she bore children at the current age- Age-specific fertility rates are calculated for the three years before the survey, based on detailed birth histories provided by women.  ",
    // 8
    "Anganwadi Buildings": " Anganwadi Buildings Started by the Indian government in 1975 as part of the Integrated Child Development Services (ICDS) program, Anganwadis aim to combat child hunger and malnutrition, with the term meaning \"courtyard shelter.\u201d  ",
    // 9
    "Anganwadi Workers": " Anganwadi Workers Anganwadi Workers (AWWs) are responsible for implementing the ICDS program at the grassroots level, providing essential services such as nutrition education, health monitoring, and early childhood education.   ",
    // 10
    "Anganwadis with Toilets": " Anganwadis With Toilets Health and Wellness Centres (Sub-centres and PHCs), in both rural and urban areas provide primary care services.  ",
    // 11
    "Primary Health Centers": " Primary Health Centers  Health and Wellness Centres (Sub-centres and PHCs), in both rural and urban areas provide primary care services.  ",
    // 12
    "Community Health Centers": " Community Health Centers Community Health Centres, in rural areas can be either non-FRU (First Referral Unit) or FRU depending on the range of services provided. In urban areas, CHCs will provide services at par with FRU  ",
    // 13
    "Sub-District Hospitals": " Sub-District Hospitals District and Sub-district hospitals provide secondary care services. Health and Wellness Centres (Sub-centres and PHCs), in both rural and urban areas provide primary care services.  ",
    // 14
    "District Hospitals": " District Hospitals District and Sub-district hospitals provide secondary care services.  ",
    // 15
    "Ante Natal Care": " Ante Natal Care ANC registration rate is the % of pregnant women who used ANC care provided by skilled health personnel = Total ANC registered/Estimated pregnancies* 100  ",
    // 16
    "nan": " Nan Proportion of women who were registered within first trimester (12weeks) of pregnancy = Total no. of ANC registered within first trimester (12weeks)/Total ANC registered*100  ",
    // 17
    "Auxiliary Nurse Midwife": " Auxiliary Nurse Midwife India has three cadres of CHWs. The first created is the Auxiliary Nurse-Midwife (ANM), who is based at a sub-center and visits villages in addition to providing care at the subcenter. The second is the Anganwadi Worker (AWW), who works solely in her village and focuses on provision of food supplements to young children, adolescent girls, and lactating women. The most recently created cadre is the Accredited Social Health Activist (ASHA), who also works solely in her village.  ",
    // 18
    "Cardiovascular Disease": " Cardiovascular Disease CVDs are a group of disorders of the heart and blood vessels and include coronary heart disease, cerebrovascular disease, rheumatic heart disease and other conditions.  ",
    // 19
    "First Referral Unit": " First Referral Unit Health facilities providing comprehensive emergency obstetric and newborn care services including deliveries by Caesarean section (C-section) surgery and blood transfusion services are designated as First Referral Units (FRUs) in India.   ",
    // 20
    "Integrated Child Development Services": " Integrated Child Development Services Integrated Child Development Services (ICDS) scheme is world's largest community based programme. The scheme is targeted at children upto the age of 6 years, pregnant and lactating mothers and women 16\u201344 years of age.  ",
    // 21
    "Iron and Folic Acid": " Iron And Folic Acid Weekly Iron and Folic Acid supplementation (WIFS) is a Government of India programme under which iron folic acid tablets are given free-of-cost to all school-going adolescent boys and girls studying in government/government-aided schools/municipal schools from classes 6th to 12th, and to out-of-school adolescent girls through Anganwadi Centres (AWCs) once every week. In addition to IFA supplements, albendazole tablets for de-worming are also administered twice a year.  ",
    // 22
    "Indian Public Health Standards": " Indian Public Health Standards IPHS are the benchmarks for quality of service delivery expected from various public health care faciltiies at all levels. They can also form the basis for assessing performance of public health care delivery system.   ",
    // 23
    "Low Birth Weight": " Low Birth Weight Low birth weight (LBW) is defined as a birth weight of less than 2500 g (up to and including 2499 g)  ",
    // 24
    "Post Natal Care": " Post Natal Care Postnatal care (PNC) refers to the care provided to mothers and their newborns immediately after childbirth. This care is essential for monitoring the health of both the mother and the infant, addressing any complications, and providing education on breastfeeding, nutrition, and family planning.   ",
    // 25
    "Severe Acute Malnutrition": " Severe Acute Malnutrition Severe acute malnutrition (SAM) is a life-threatening condition characterized by a very low weight-for-height ratio, visible severe wasting, or nutritional edema.  ",
    // 26
    "Sustainable Development Goals": " Sustainable Development Goals The Sustainable Development Goals (SDGs) are a set of 17 global goals established by the United Nations in 2015 to address various social, economic, and environmental challenges.  ",
    // 27
    "Health and Wellness Centre-Sub Health Centre": " Health And Wellness Centre-Sub Health Centre A Health and Wellness Centre \u2013 Sub Health Centre (HWC-SHC) is the most peripheral and first point of contact in the Indian public healthcare delivery system, especially in rural and remote areas. It is part of the Ayushman Bharat program launched in 2018, which aims to strengthen primary health care.  ",
    // 28
    "Sexual Reproductive Health": " Sexual Reproductive Health Sexual reproductive health (SRH) encompasses a range of services related to sexual health, reproductive rights, family planning, and maternal health. Promoting SRH is essential for empowering individuals to make informed choices about their bodies and relationships, ultimately contributing to improved health outcomes.   ",
    // 29
    "Sexually Transmitted Infections": " Sexually Transmitted Infections Sexually transmitted infections (STIs) are infections that are primarily spread through sexual contact. Common STIs include chlamydia, gonorrhea, syphilis, and HIV/AIDS.  ",
    // 30
    "Universal Health Coverage": " Universal Health Coverage Universal Health Coverage (UHC) ensures that all individuals have access to necessary health services without financial hardship. UHC aims to provide comprehensive healthcare services that include prevention, treatment, rehabilitation, and palliative care.   ",
    // 31
    "Rassa": " Rassa A thin soup of meat or fish or vegetable stock  ",
    // 32
    "Goushala": " Goushala Goshala, a Sanskrit word (\"Go\" means cow and \"Shala\" means a shelter place: Go + Shala = shelter for cows), means the abode or sanctuary for cows, calves and oxen.  ",
    // 33
    "Palkhi": " Palkhi It is a traditional vehicle which is usually made out of wood into a rectangular or a oval shaped box with the openings from the side [ along the length of the box] and fitted with long sticks along the closed sides [i.e. the breath of the box] which will be carried by four or more [minimum 4 persons]. It is usually used to carry devtas or a Person of a very high honour like a king, a Guru etc;  ",
    // 34
    "Dindi": " Dindi It is a traditional vehicle which is usually made out of wood into a rectangular or a oval shaped box with the openings from the side [ along the length of the box] and fitted with long sticks along the closed sides [i.e. the breath of the box] which will be carried by four or more [minimum 4 persons]. It is usually used to carry devtas or a Person of a very high honour like a king, a Guru etc;  ",
    // 35
    "Sutak": " Sutak In astrology, Sutak is a period before significant events like eclipses, weddings, births, and death ceremonies. It's considered an inauspicious time when negative energies are believed to prevail. During this time, it's recommended to avoid starting new projects or important activities. For example, during a solar eclipse, the Sutak period begins 12 hours before the eclipse.   ",
    // 36
    "Saag": " Saag Stir fried vegetables in Indian spices/pastes.  ",
    // 37
    "Sabzi": " Sabzi Stir fried vegetables in Indian spices/pastes.  ",
    // 38
    "Bhaji": " Bhaji Stir fried vegetables in Indian spices/pastes.  ",
    // 39
    "Jagran": " Jagran Jagaran or jagraata refers to the Hindu functions, especially religious ones, which go on for the whole night. It is usually- ~a mass reading of some holy book or scripture, people taking shifts to read the whole thing in 24 hours or in the night. AND/OR ~singing of bhajans (hymns), listening to katha (stories)  ",
    // 40
    "Mukhwaas": " Mukhwaas Mukhwas is a mouth freshener that can be prepared in various ways and flavours. Indians eat mukhwas after a meal because it freshens their breath and helps them digest. It comprises various seeds, including sesame seeds, fennel seeds, flax seeds (alsi), ajwain, suva seeds, and dhana dal seeds.  ",
    // 41
    "Mukhvas": " Mukhvas Mukhwas is a mouth freshener that can be prepared in various ways and flavours. Indians eat mukhwas after a meal because it freshens their breath and helps them digest. It comprises various seeds, including sesame seeds, fennel seeds, flax seeds (alsi), ajwain, suva seeds, and dhana dal seeds.  ",
    // 42
    "Mazar": " Mazar Kabr: In Hindi and Urdu, \"kabr\" (\u0915\u092c\u094d\u0930) translates to \"grave\" or \"tomb,\" referring to a burial site where a deceased body is interred23. It can also imply a broader concept of a burial chamber or sepulcher. Mazar: This term is commonly used in South Asian contexts to denote a grave, particularly one dedicated to a Sant. Tomb: A general term in English for a burial structure, typically above or below ground, that houses the remains of the deceased. It can be ornate, like a mausoleum, or simple, like a grave.  ",
    // 43
    "Kabr": " Kabr Kabr: In Hindi and Urdu, \"kabr\" (\u0915\u092c\u094d\u0930) translates to \"grave\" or \"tomb,\" referring to a burial site where a deceased body is interred23. It can also imply a broader concept of a burial chamber or sepulcher. Mazar: This term is commonly used in South Asian contexts to denote a grave, particularly one dedicated to a Sant. Tomb: A general term in English for a burial structure, typically above or below ground, that houses the remains of the deceased. It can be ornate, like a mausoleum, or simple, like a grave.  ",
    // 44
    "Pav": " Pav  A soft and puffy indian style bread recipe made with plain flour and dry yeast.   ",
    // 45
    "Paav": " Paav  A soft and puffy indian style bread recipe made with plain flour and dry yeast.   ",
    // 46
    "Egg Bhurji": " Egg Bhurji Egg Bhurji also known as Anda Bhurji, is an Indian dish of spiced scrambled eggs. It is made by scrambling beaten eggs with saut\u00e9ed onions, tomatoes, spices and herbs.  ",
    // 47
    "Prasad": " Prasad Prasada is derived from the verb prasad which consists of the verb \u0938\u0926\u094d (sad - to sit, dwell) which is prefixed with \u092a\u094d\u0930 (pra - before, afore, in front) and used as finite verb \u092a\u094d\u0930\u0938\u0940\u0926\u0924\u093f (prasidati - dwells, presides, pleases or favours etc.). It is offered as an offering to Devis/Devtas.   ",
    // 48
    "Vada Pav": " Vada Pav The various types of vadas are made from different ingredients, ranging from legumes (such as medu vada of South India) to potatoes (such as batata vada of Maharashtra). They are often served as a breakfast item or a snack, and also used in other food preparations (such as dahi vada, vada pav, and doubles).  ",
    // 49
    "Tapri": " Tapri Roadside restaurant/Tea stall  ",
    // 50
    "Talab": " Talab Pond  ",
    // 51
    "Talao": " Talao Pond  ",
    // 52
    "Diwali": " Diwali The five days of Diwali include Dhanteras, Naraka Chaturdashi (Choti Diwali), Diwali, Govardhan Puja and Bhai Dooj. Each day of Diwali celebrations has its own rituals and significance: 1. Dhanteras Dhanteras marks the start of Diwali, where people worship Devi Lakshmi and Devta Kuber for wealth and prosperity. It is customary to purchase new items, especially gold. 2. Naraka Chaturdashi (Choti Diwali) This day honors Devta Krishna's victory over the demon Narakasura, symbolizing the removal of evil. 3. Diwali The main day celebrates the return of Devta Rama, Mata Sita, and Lakshman to Ayodhya, representing the triumph of good over evil. Homes are adorned with diyas and rangoli, and Lakshmi and Ganesh Puja is performed. 4. Govardhan Puja This day commemorates Devta Krishna lifting Govardhan Hill to protect the people of Mathura from Indra's wrath. 5. Bhai Dooj The final day celebrates the bond between brothers and sisters, where sisters pray for their brothers' well-being and receive gifts in return.  ",
    // 53
    "Agarbatti": " Agarbatti Incense sticks, also called Agarbatti/Mombatti are made of fragrant herbs and flowers that are burned to create a pleasant aroma. They come in a variety of fragrances and aromas, from traditional jasmine and sandalwood to more exotic scents like Mogra and Rose. Incense sticks are lit on fire and the smoke is then inhaled, while dhoop is left to burn without any smoke being inhaled. Incense sticks can be used with prayers, meditations or mantras, while dhoop is mostly used for meditation. Dhoop sticks typically come in smaller sizes than Incense sticks.   ",
    // 54
    "Mombatti": " Mombatti Incense sticks, also called Agarbatti/Mombatti are made of fragrant herbs and flowers that are burned to create a pleasant aroma. They come in a variety of fragrances and aromas, from traditional jasmine and sandalwood to more exotic scents like Mogra and Rose. Incense sticks are lit on fire and the smoke is then inhaled, while dhoop is left to burn without any smoke being inhaled. Incense sticks can be used with prayers, meditations or mantras, while dhoop is mostly used for meditation. Dhoop sticks typically come in smaller sizes than Incense sticks.   ",
    // 55
    "Arangetram": " Arangetram An Arangetram is a Bharathanatyam dancer\u2019s first full-length solo performance signifying that he/she is able to present the complete suite of traditional repertoire   ",
    // 56
    "Payal": " Payal hungroos are especially worn by dancers whereas the payal anklet is an evolved version of ghungroos, having a very sleek design and only a few bells. They are worn by women for adornment. Ghungroos are considered sacred to every Indian classical dancer.  ",
    // 57
    "Surma": " Surma People frequently use Kajal and Surma or Antimony interchangeably, however there is a distinction between the two. Antimony, on the other hand, is a traditional Indian cosmetic, typically in the form of powder. Surma, which is located in the Arabian Sea, is supposed to be made from a stone named Kohinoor. Kajal, on the other hand, is formed from antimony powder in the form of a mildly moistened paste. Women, on the other hand, can make their own kajal.  ",
    // 58
    "Maut Ka Kaun": " Maut Ka Kaun The Wall of Death, motordrome, silodrome or Well of Death (aka \u201cMaut ka Kuaa\u201c, India) is a carnival sideshow featuring a silo- or barrel-shaped wooden cylinder, ranging from 20 to 36 feet (6.1 to 11 m) in diameter, inside of which motorcyclists, or the drivers of miniature automobiles, travel along the vertical wall and perform stunts, held in place by centripetal force.  ",
    // 59
    "Buddhi ke Baal": " Buddhi Ke Baal Refers to \"cotton spun by an old woman\"  ",
    // 60
    "Gobar": " Gobar Dried cow dung used directly as fuel or as a source of gas.  ",
    // 61
    "Sanrakshan": " Sanrakshan Conservation efforts.  ",
    // 62
    "Jugaad": " Jugaad  That idea of patching something together in a very makeshift way to get a result you want.  ",
    // 63
    "Artificial Insemination": " Artificial Insemination Artificial insemination is a widely used method in livestock rearing with multiple benefits, including increased production efficiency, better genetics of animals and longer lifespans and productive years for animals. It can reduce many risks of natural mating, including injuries, accidents, and the spread of diseases. As such, the government has introduced targets for number of artificial inseminations per year. The artificial Insemination has direct co-relation with breeding and increased milk production. In India, the application of Artificial Insemination (AI) is predominantly limited to cattle and buffaloes.  ",
    // 64
    "Draught Animals": " Draught Animals A working animal is an animal, usually domesticated, that is kept by humans and trained to perform tasks instead of being slaughtered to harvest animal products.  ",
    // 65
    "Attar": " Attar A perfume or essential oil obtained from flowers or petals.  ",
    // 66
    "Mela": " Mela A public event that is organized to celebrate a special occasion or an event where goods can be bought and sold  ",
    // 67
    "Masala": " Masala A mixture of Indian spices used in cooking.  ",
    // 68
    "Gola": " Gola Shaved ice with different syrups and toppings.   ",
    // 69
    "Chuski": " Chuski Shaved ice with different syrups and toppings.   ",
    // 70
    "Barf ka Gola": " Barf Ka Gola Shaved ice with different syrups and toppings.   ",
    // 71
    "Common Property Resource": " Common Property Resource  A natural or man-made resource that is collectively owned or managed by a group of people or a community. These goods are non-excludable, but rival that their value diminishes as they are used up.  ",
    // 72
    "Credit Subsidy": " Credit Subsidy Credit subsidy denotes the difference between interest charged from farmers, and the actual cost of providing credit, plus other costs such as write-offs bad loans or loan waivers. Credit subsidy is offered by the government to farmers to protect their larger interest.   ",
    // 73
    "Disguised Unemployment": " Disguised Unemployment It is the form of unemployment under which workers seem to be working but don\u2019t contribute anything towards the level of output making the aggregate economic output to be the same. In this case, the marginal productivity of the workers which is the addition to total productivity becomes zero (MP=0).  ",
    // 74
    "Direct Tax": " Direct Tax A tax that is paid directly to the government by individuals or organizations, such as income tax or corporate tax.   ",
    // 75
    "Jal Shakti": " Jal Shakti Jal Shakti Abhiyaan was started by the Department of Drinking Water and Sanitation, Ministry of Jal Shakti, Government of India in 2019 in water-stressed districts to promote water conservation and water resource management.  ",
    // 76
    "Janani Suraksha Yojana (JSY)": " Janani Suraksha Yojana (Jsy) The Janani Suraksha Yojana (JSY) is a part of the National Health Mission and serves as a crucial initiative to ensure safe motherhood. Its primary aim is to decrease maternal and neonatal mortality rates by encouraging impoverished pregnant women to opt for institutional deliveries.   ",
    // 77
    "Mahatma Gandhi National Rural Guarantee Act (MGNREGA)": " Mahatma Gandhi National Rural Guarantee Act (Mgnrega) In 2006, the Ministry of Rural Development introduced MGNREGA to provide 100 days of guaranteed wage employment in a financial year to every household in rural areas. The graphs below demonstrate a close match between the people and households that were assigned work and those that requested work.  ",
    // 78
    "Pradhan Mantri Kaushal Vikas Yojana (PMKVY)": " Pradhan Mantri Kaushal Vikas Yojana (Pmkvy) In the year 2015, PMKVY was launched by the Ministry of Skill Development and Entrepreneurship implemented by National Skill Development Corporation to enable a large number of Indian youth to take up industry relevant training.  ",
    // 79
    "Craftsmen Training Scheme": " Craftsmen Training Scheme The Craftsmen Training Scheme (CTS) was established by the Government of India in 1950 with the purpose of ensuring a consistent supply of skilled workers across various trades for the country's industries.   ",
    // 80
    "Swachh Bharat Mission (SBM)": " Swachh Bharat Mission (Sbm) Launched in 2014, SBM was aimed at eliminating open defection and improving solid waste management. The district has over 250 public toilets and over 32 thousand individual household laterines (IHHL).  ",
    // 81
    "Aadhaar": " Aadhaar The Unique Identification Authority of India (UIDAI) defines Aadhaar as a 12-digit unique ID number given to Indian residents. It's based on their biometric and demographic details and serves as a universal identity proof. It's voluntary and available to all residents, regardless of existing documents.  ",
    // 82
    "Pradhan Mantri Fasal Bima Yojana (PMFBY)": " Pradhan Mantri Fasal Bima Yojana (Pmfby) The Pradhan Mantri Fasal Bima Yojana was launched in 2016 by Prime Minister Narendra Modi as an insurance scheme for famers and their yield. The Pradhan Mantri Fasal Bima Yojana (PMFBY) has a fundamental objective: to offer an all-encompassing insurance safeguard that shields farmers from crop losses.  ",
    // 83
    "Martha Empire": " Martha Empire The Maratha Empire, led by Chhatrapati Shivaji Maharaj (the first king), was formed in the late 17th century. It expanded rapidly while challenging the Mughal rule. It dominated much of the Indian subcontinent in the 18th century becoming the biggest South Asian state by the middle of the 18th century.  ",
    // 84
    "Maurya Empire": " Maurya Empire The Mauryan Empire was founded by Chandragupta Maurya (lasted approx. 322 BCE to 185 BCE) At one point, the empire's reign stretched across parts of modern-day Iran and a majority of the Indian subcontinent. Its capital was Patliputra, which is present-day Patna.   ",
    // 85
    "Chalukyas": " Chalukyas The Chalukya Dynasty ruled over Deccan region and Southern parts of India from the 6th to 12th centuries. The reigned in three related yet individual dynasties: Badami Chalukyas, Western Chalukyas, and Eastern Chalukyas.   ",
    // 86
    "Silharas": " Silharas Silhara Dynasty was established itself in the 8th Ccentury CE and ruled over northern and southern Konkan. The dynasty operated in three branches with each branch ruling over an area of its own. They ruled over North Konkan, South Konkan, and the districts of Kolhapur, Satara, and Belagavi. The rise of the Yadavas led to the eventual demise of the Silhara.   ",
    // 87
    "Vijayanagar Empire": " Vijayanagar Empire Vijayanagar Dynasty, an empire that ruled mostly over south India, was established in 1336 by Harihara I and his brother Bukka Raya I. While the reign lasted till 1646, much of its power started declining from 1565 onwards. The empire derived its name from its capital city Vijaynagara whose ruins are now a UNESCO World Heritage Site in present-day Karnataka.   ",
    // 88
    "Yadavas of Devagiri/Yadavas": " Yadavas Of Devagiri/Yadavas The Yadava dynasty's realm stretched from the Narmada River in the north to the Tungabhadra River in the south. Its territory included present-day Maharashtra, Northern Karnataka, and parts of Madhya Pradesh. Devagiri (present-day Daulatabad) served as its capital city. The Khalji dynasty's (of the Delhi Sultanate) annexation led to the fall of the Yadava dynasty.   ",
    // 89
    "Alauddin Khilji": " Alauddin Khilji Alauddin Khlaji, originally known as Ali Gurshasp before his ascension in 1296, was the second ruler of the Khalji dynasty and the 13th Sultan of the Delhi Sultanate. Renowned for implementing significant administrative reforms, he seized the throne by assassinating his predecessor and uncle, Jalaluddin Khalji. Alauddin was also the first Muslim ruler to successfully conquer parts of southern India.   ",
    // 90
    "Harihara I": " Harihara I Harihara I (1336 to 1356 ), also known as Hakka and Vira Harihara I, was the founder of the Vijayanagar Empire, which constituted present-day Karnataka. He along with his successors established the Sanagama dynasty which was one of the four dynasties that went to rule the empire. Harihara I and his brother Bukka Raya were originally governors under the Kakatiya dynasty and upon its defeat by Muhammad bin Tughlaq, they were held prisoners and sent to Delhi.   ",
    // 91
    "Bukka Raya I": " Bukka Raya I Bukka Raya I (1356 to 1377 ), was the second emperor of the Vijayanagara Empire. He succeeded his brother Harihara I. He belonged to the Sangama dynasty. Bukka Raya's reign saw the expansion of the empire's territory as Bukka Raya conquered most of the kingdoms of Southern India. Bukka Raya I and his brother Harihara were originally governors under the Kakatiya dynasty and upon its defeat by Muhammad bin Tughlaq, they were held prisoners and sent to Delhi.   ",
    // 92
    "Battle of Talikota": " Battle Of Talikota The battle of Talikota was fought in 1565 between the Vijayanagara Empire and an alliance of the Deccan Sultanates. It took place in the town of Talikota, which is located in present-day Karnataka. The battle resulted in the defeat and death of the de facto ruler of the Vijayanagara Empire, Rama Raya. Although the Vijayanagara forces initially had the upper hand, they eventually met their defeat. One of the reasons for the same was the Gilani brother's (Muslim commanders under Rama Raya) defection to the Sultanate's side.   ",
    // 93
    "Bahmani Sultanate": " Bahmani Sultanate Following Ismail Mukh's rebellion against Muhammad bin Tughlaq, Ala-ud-Din Hasan Bahman Shah (originally named Zafar Khan) established the Bahmni Sultanate in 1347. It became the first independent Islamic kingdom in South India. The Bahmani kingdom was often at war with the neighbouring Vijayanagara Empire. The Bahmani Sultanate eventually fragmented into five states - Ahmednagar, Berar, Bidar, Bijapur, and Golconda. Collectively, they were the Deccan Sultanates.   ",
    // 94
    "Raja Bhoja II": " Raja Bhoja Ii Bhoja II was the last ruler of the Silhara dynasty. In or around 1219-1220, he was defeated at the hands of Singhana, a Yadava Dynasty king. His reign marked the final phase of Silhara rule before the dynasty was overthrown. Raja Bhola II is known to have built 15 forts across the Sahyadri range of Western Maharashtra.   ",
    // 95
    "Adil Shahis of Bijapur": " Adil Shahis Of Bijapur Adil Shahis of Bijapur (also known as the Sultanate of Bijapur or Adil Shahi dynasty) ruled the kingdom of Bijapur from 1489 to 1686. The dynasty was established by Yusuf Adil Shah. It was one of the Deccan Sultanates. In 1686, Aurangzeb annexed Bijapur therefore overthrowing the Adil Shahi rule.  ",
    // 96
    "Yusuf Adil Shah": " Yusuf Adil Shah Yusuf Adil Shah (also known as Yusuf Adil Khan) was the founder of the Adil Shahi dynasy that ruled the Bijapur Sultanate for over two centuries. According to one of many theories, Yusuf Adil Shah may have been the son of the Ottoman Sultan Muad II. He was killed at the hands of Krishna Deva Raya, the Vijayanagara king, in a battle in December 1510.   ",
    // 97
    "Sambhaji Bhosale": " Sambhaji Bhosale Sambhaji Bhonsle was the second ruler of the Maratha Empire, reigning from 1681 to 1689. He was the eldest son of Chhatrapati Shivaji Maharaj. He is known to have led the Marathas against the Muhgals, Portugese, and Siddis of Janjira. In 1689, he was captured by the Mughals and upon Aurangzeb's orders he was executed. Additionally, Sambhaji was a very well-educated individual who was well-versed in several languages. Sambhaji had even authored several books in his lifetime  ",
    // 98
    "Rajaram I/Rajaram Bhosale": " Rajaram I/Rajaram Bhosale Rajaram I was the third ruler of the Maratha empire. He was the second son of Chhatrapati Shivaji Maharaj and the younger half-brother of Sambhaji. His ascension to the throne in 1689 followed his brother Sambhaji's execution at the hands of Aurangzeb. Rajaram died of what is suspected to be a liver disease in 1700 at Sinhagad near Pune.   ",
    // 99
    "Shahuji": " Shahuji Shahu I was the fifth ruler (Chhatrapati) of the Maratha empire. He was the son of Sambhaji and Yesubai making him Chhatrapati Shivaji Maharaj's grandson. In 1689 when he was just seven years old, Shahu along with his mother was captured and imprisoned by Aurangzeb. Following Aurangzeb's death in 1707, Shahu was released and returned to claim his throne. Upon his return, he found that his aunt Tarabai had been governing the Maratha empire as a regent for her young son. As a result, the Battle of Khed took place between Shahu and Tarabai. He emerged victorious, thereby gaining the throne in 1708.   ",
    // 100
    "Battle of Khed": " Battle Of Khed The Battle of Khed was a succession conflict fought between Shahu I and Tarabai over the Maratha Throne. While Shahu I was away imprisoned, Tarabai ruled the Maratha empire as a regent for her young son. Shahu I discovered the same upon his release and return. Thus ensued the Battle of Khed which resulted in Shahu I's victory, making him the fifth ruler (Chhatrapati) of the Maratha empire.   ",
    // 101
    "Siddis of Janjira": " Siddis Of Janjira The Siddis were originally brought to the Indian subcontinent as slaves, bodyguards, and soldiers during the Delhi Sultanate. Janjira State was a princely state in India during the British Raj. It was located on the Konkan coast in the present-day Raigad district. It was governed by the Siddi Khan dynasty of Habesha descent. During the 17th and 18th centuries, the Siddis of Janjira successfully fended off multiple attacks from the Dutch, Portuguese, French, British, Mughals, and the Marathas.  ",
    // 102
    "Kanhoji Angre": " Kanhoji Angre Kanhoji Angre was a commander of the Maratha Naval. He is known for successfully defending the Konkan coast from foreign powers like the Portuguese, British, and the Siddis of Janjira. Kanhoji Angre raided the foreign ships and collected a form of tax (jakat) from them. Angre managed to do this successfully until his death in 1729. Angre's contribution to maritime security ensured that the Marathas remained a significant power.   ",
    // 103
    "Sakharam Madhav": " Sakharam Madhav Sakharam Madhav was born in Ambadpal in the Sindhudurg district of Maharashtra in August in 1910. Upon the death of both of his parents, the Maratha warrior Tanhaji Rane took four-year-old Sakharam under his care. When he was 19 he got recruited by the British and his first posting was at Belgaon. In 1939 he was sent to the Burma War. After 1945, he joined the Azad Hind Sena. Sukharam Madhav died on 21st May 1999, aged 90.   ",
    // 104
    "Netaji Subhash Chandra Bose": " Netaji Subhash Chandra Bose Netaji Subhash Chandra Bose was one of India's most celebrated freedom fighters. In 1921, he joined the nationalist movement led by Mahatma Gandhi and became an active member of the Indian National Congress (INC). Eventually, he was elected Congress president in 1938, but soon, differences arose between him and his peers. One of the major points of conflict was Bose's disagreement with Mahatma Gandhi's idealogy of non-violence. In 1943, with Japanesse support, Bose reorganized the 40,000-strong Indian National Army (also known as the Azad Hind Fauj) to fight against the British rule. However, Japan and the INA were defeated in World War II. It is said that Bose died in a Japanese hospital from burn injuries sustained in a plane crash in Taiwan.   ",
    // 105
    "Azad Hind Sena": " Azad Hind Sena Azad Hind Sena was initially formed by Mohan Singh in 1942 with the support of the Japanese. However, due to Mohan Singh's unwillingness to align with the Japanese, he was arrested which resukted in the disbandment of the Azad Hind Sena. Subhash Chandra Bose upon his return in 1943 reestablished the Azad Hind Sena  ",
    // 106
    "Samyukta Maharashtra Movement": " Samyukta Maharashtra Movement The Samyukta Maharashtra Movement (also known as Samyukta Maharashtra Samiti) was an organization that campaigned for the creation of a separate Marathi-speaking state between 1956 and 1960. The organization demanded that this separate state have the city of Bombay as its capital. The Samyukta Maharashtra Movement finally achieved its goal on 1st May 1960 when the State of Bombay was split into two parts- the Marathi-speaking state of Maharashtra and the Gujarati-speaking state of Gujarat. On 1st May, Maharashtrians celebrate Maharashtra Day.   ",
    // 107
    "Mahagujarat Movement": " Mahagujarat Movement Mahagujarat Movement (also known as the MahaGujarat Andolan) was a political movement with the agenda of creating a Gujarati-speaking state for the Gujarati speakers residing in the state of Bombay. This movement culminated in the formation of Gujarat on 1st May 1960.   ",
    // 108
    "Satavahan dynasty": " Satavahan Dynasty They arrived in c.a. 200 CE, and expanded an empire stretching across the Northern Deccan, covering lands that today make up Andhra Pradesh, Maharashtra, and Telangana. Although their realm was not a continuous stretch of land, it was nonetheless a diverse territory. They ruled the longest in the Deccan history, with their seat of power established in Dharanikota, also known as Dhanakot (in present Andhra Pradesh). From this stronghold, they cast their influence across the landscape, likely including Jalgaon. Their reigns shaped the destiny of Vidarbha (Berar) and, perhaps by extension, Akola, adding layers to the historical narrative of the region.   ",
    // 109
    "Paithan": " Paithan Paithan( historically known as Pratishthan (\u092a\u094d\u0930\u0924\u093f\u0937\u094d\u0920\u093e\u0928)), located 56 km south of present-day Chh. Sambhaji Nagar is an ancient town. Situated on the banks of the Godavari River, Paithan was the capital of the Satavahana dynasty, one of the earliest rulers of Deccan India. It was a major center for trade, culture, and learning. The town is argued to had trade links with Rome, Mesopotamia, and Greece. The city is known for world-famous Paithani sarees, which are made of pure silk and gold zari. The town remains an important cultural destination in Maharashtra today.   ",
    // 110
    "Rani Ahilya Bai Holkar": " Rani Ahilya Bai Holkar Rani Ahilya Bai Holkar (1725 \u2013 1795) was a prominent ruler of the Malwa Kingdom. After losing both her husband Khanderao Holkar (1754) and son Malerao Holkar (1766) , Ahilya Bai Holkar took over the administration of the Malwa kingdom and ruled for over two decades. Under her rule, the capital city Maheshwar (presently in Khargone district, Madhya Pradesh) prospered into an industrial and cultural hub. Apart from being one of the greatest females leaders in India history, she is widely known for her construction and restoration of mandirs across India. Grishneshwar Jyotirlinga Mandir in Chhatrapati Sambhajinagar district (Maharashtra) is one such expamle. She played a crucial role in its restoration. Known as \u2018The Philosopher Queen\u2019, Rani Ahilya Bai Holkar passed away on 13 August 1795, but her undying legacy lives on through the numerous mandirs, dharamshalas, and public works she comissioned.   ",
    // 111
    "Daulatabad": " Daulatabad Devagiri, now known as Daulatabad, is an ancient hill fortress and town located near Chhatrapati Sambhajinagar. ) is a city in present-day Sambhaji Nagar (Aurangabad). It was a strategic location of great significance. It was once the capital of two dynasties Yadavas and Tughlaqs. It is famous for its strategic location, architectural brilliance, and historical importance. In 1327, Muhammad bin Tughlaq, the Sultan of Delhi, renamed Devagiri as Daulatabad (abode of wealth) and shifted his capital from Delhi to Daulatabad. The Devagiri Fort located in the town is one of the strongest forts in India, built on a steep hill with only one access route.   ",
    // 112
    "Devagiri": " Devagiri Devagiri, now known as Daulatabad, is an ancient hill fortress and town located near Chhatrapati Sambhajinagar. ) is a city in present-day Sambhaji Nagar (Aurangabad). It was a strategic location of great significance. It was once the capital of two dynasties Yadavas and Tughlaqs. It is famous for its strategic location, architectural brilliance, and historical importance. In 1327, Muhammad bin Tughlaq, the Sultan of Delhi, renamed Devagiri as Daulatabad (abode of wealth) and shifted his capital from Delhi to Daulatabad. The Devagiri Fort located in the town is one of the strongest forts in India, built on a steep hill with only one access route.   ",
    // 113
    "Muhammad bin Tughluq": " Muhammad Bin Tughluq Muhammad bin Tughluq (1290 \u2013 March 1351) Muhammad bin Tughluq was the second ruler of the Tughluq dynasty of the Delhi Sultanate. was the eighteenth Sultan of Delhi. He was nicknamed \"The Wise Fool\" (Pagal Sultan) because of his brilliant yet disastrous policies. Some of the policies included shifting the capital from Delhi to Daulatabad (1327) \u2013a massive failure and Introduction of token Currency \u2013 a financial disaster. However, he was one of the most learned rulers of the Delhi Sultanate, well-versed in philosophy, mathematics, astronomy, medicine, and Persian literature.   ",
    // 114
    "Satavahan dynasty": " Satavahan Dynasty The Satavahana Dynasty (c. 1st century BCE \u2013 3rd century CE) was one of the earliest and most powerful ruling dynasties in Deccan India (present-day Maharashtra, Andhra Pradesh, Telangana, Karnataka, and Madhya Pradesh). They ruled after the decline of the Maurya Empire and played a key role in uniting the Deccan region. The first important king was Simuka Satavahana, who established the dynasty around 1st century BCE. Their capital cities included Paithan (Pratishthana, Maharashtra) and Amaravati (Andhra Pradesh). They ruled for about 400 years, reaching their peak under Gautamiputra Satakarni.  ",
    // 115
    "Nizam Shahis": " Nizam Shahis The Ahmednagar Sultanate (1490\u20131636) was one of the five Deccan Sultanates that emerged after the fall of the Bahmani Sultanate in 1490. It ruled over parts of Maharashtra, Telangana, and Madhya Pradesh, with its capital at Ahmednagar (present Ahilyanagar). Founded by Malik Ahmad Nizam Shah I in 1490, breaking away from the Bahmani Sultanate. It was ruled by the Nizam Shahi dynasty and was a major player in Deccan politics. The dynasty lasted until 1636, when it was annexed by the Mughal Empire under Shah Jahan.  ",
    // 116
    "Hussain Nizam Shah I": " Hussain Nizam Shah I Malik Ahmad Nizam Shah I was the founder of the Ahmednagar Sultanate and the Nizam Shahi dynasty in 1490. He was a former governor under the Bahmani Sultanate but declared independence, establishing his rule in the Deccan region of India. He control extended large parts of present-day Maharashtra, including Pune, Nashik, and Daulatabad. He argued to have constructed the Ahmednagar Fort, one of the strongest forts in India, which later served as an important defense structure.  ",
    // 117
    "The Second Anglo-Maratha War": " The Second Anglo-Maratha War The Second Anglo-Maratha War (1803\u20131805) was fought between the British East India Company and the Maratha Empire due to internal conflicts among Maratha leaders. The war began after Peshwa Baji Rao II signed the Treaty of Bassein (1802). Major battles were fought , including the Battle of Assaye, Battle of Laswari, and Battle of Argaon in Maharashtra. The war ended with British dominance growing further, setting the stage for the Third Anglo-Maratha War (1817\u20131818), which ultimately led to the fall of the Maratha Empire and British occupation over most of India.  ",
    // 118
    "Arthur Wellesley": " Arthur Wellesley Arthur Wellesley, 1st Duke of Wellington (May 1769 \u2013 September 1852), Arthur Wellesley was a British general and statesman who played a crucial role in British occupation of India. He began his military career as a young officer in Ireland and, in 1794, was sent to Flanders with the 33rd Regiment. He later arrived in India, where he played a crucial role in the Anglo-Mysore Wars, helping defeat Tipu Sultan in 1799, and later, as a major general, led British forces in the Second Anglo-Maratha War (1803\u20131805). After returning to Europe, he fought in the Peninsular War (1807\u20131814), leading British forces alongside Portugal and Spain against Napoleon\u2019s army. His most famous victory came in 1815 at the Battle of Waterloo, where he played a decisive role in Napoleon\u2019s final defeat.   ",
    // 119
    "Akbar": " Akbar Jalal-ud-din Muhammad Akbar, (1542\u20131605) commonly known as Emperor Akbar, was the third and most powerful ruler of the Mughal Empire (ruled 1556\u20131605). He expanded the empire significantly, making it one of the largest and most stable empires in Indian history. He first reclaimed Delhi by defeating Hemu at the Second Battle of Panipat (1556) and, throughout his reign, expanded his empire through the conquest of Malwa, Rajputana, Gujarat, Bengal, Bihar, and Afghanistan. He is known to have promoted Hindu-Muslim unity, abolished the Jizya tax on non-Muslims, and introduced Din-i-Ilahi, a syncretic religious philosophy. In 1593, Akbar began military operations against the Deccan Sultans, and later, his forces captured Ahmednagar in 1600. He also built Agra Fort and Fatehpur Sikri, which includes the Buland Darwaza and Jama Masjid. His reign firmly established Mughal dominance across northern and central India.  ",
    // 120
    "Aurangzeb": " Aurangzeb Aurangzeb (1618\u20131707), the sixth Mughal emperor, ruled for 49 years and expanded the empire to its greatest territorial extent across the Indian subcontinent but his policies led to internal strife and the empire's eventual decline. Before becoming emperor, he served as Viceroy of the Deccan (1636\u20131637) and Governor of Gujarat (1645\u20131647). After constant conflicts with his elder brother Dara Shikoh, he seized the throne by defeating him and imprisoning his father, Shah Jahan. Under his rule, the Mughal Empire reached its peak, stretching across most of the Indian subcontinent. Hence, he was given the title Alamgir, meaning \"Conqueror of the World.\" He faced prolonged conflicts with the Marathas, Jats, Sikhs, and Pashtuns. His policies, including the reintroduction of the jizya tax and the demolition of Hindu temples, were widely criticized. Aurangzeb, often referred to as \"The Last Great Mughal Emperor,\" died in 1707 near Ahmednagar, marking the beginning of the empire\u2019s decline.  ",
    // 121
    "Shaista Khan": " Shaista Khan Shaista Khan (1600\u20131694) was a Mughal general and the Subahdar of Bengal. He was a maternal uncle of Aurangzeb. In 1660, he arrived in Aurangabad and later captured Pune, Chakan, and Kalyan, enforcing strict Mughal rule. In 1663, Shivaji launched a raid on his palace in Pune, forcing Shaista Khan to flee. Aurangzeb transferred him to Bengal, where he focused on expanding trade with Europe, Southeast Asia, and other parts of India. In 1666, he led a successful campaign in Chittagong (present-day Bangladesh), driving out the Portuguese forces.  ",
    // 122
    "Nizams": " Nizams Nizam-ul-Mulk Asaf Jah I (11 August 1671 \u2013 1 June 1748), also known as Nizam I. Under Aurangzeb\u2019s rule, he was a general. He became the Subahdar of Bijapur in 1702 and was appointed Governor of Oudh in 1707. In 1714, he was appointed as Viceroy of the Deccan. In 1724, Muhammad Shah, the then Mughal emperor, was compelled to declare Asaf as the permanent viceroy over the Deccan region, thereby founding the Asaf Jahi dynasty, even though he remained loyal to the Mughal emperor. Subsequent rulers retained the title Nizam-ul-Mulk and were referred to as Nizams of Hyderabad. The Nizams struggled against the Marathas, losing key battles and paying Chauth (taxes) to them. In 1805, after the Second Anglo-Maratha War, the Nizam came under British protection and later became a princely state within British India.  ",
    // 123
    "Berar": " Berar  Berar is a historical region in present-day Maharashtra, known for its rich history, fertile land, and strategic importance. It was ruled by various dynasties and played a key role in Deccan politics. It became an independent Berar Sultanate (1490\u20131574) before being annexed by the Ahmednagar Sultanate and later the Mughals (1596) under Akbar. The Marathas took control in the 18th century, and it was later ruled by the British before merging with Maharashtra after India\u2019s independence.   ",
    // 124
    "Malik Hasan Bahri": " Malik Hasan Bahri Malik Hasan Bahri was a military commander and noble under the Bahmani Sultanate. He played a crucial role in the political turmoil of the Deccan and later became the founder of the Berar Sultanate in 1490. It is belived that he was originally a Hindu Brahmin who was converted to Islam. He was the founder of the Berar Sultanate (1490) after declared independence from the Bahmani rule, and established Berar as an independent kingdom. He was overthrown and replaced by Fathullah Imad-ul-Mulk, who continued ruling Berar under the Imad Shahi dynasty.   ",
    // 125
    "Mahmood Shah Bahmani": " Mahmood Shah Bahmani Mahmood Shah Bahmani (r. 1482\u20131518) was the last nominal ruler of the Bahmani Sultanate, which ruled over the Deccan region of India. His reign marked the final decline and breakup of the Bahmani Empire, leading to the emergence of the five Deccan Sultanates. He is believed to be a weak ruler as he struggled to maintain control over his powerful regional governors. This led to the breakup of the Bahmani Sultanate into five independent Deccan states paving the way for Deccan Sultnates. By the late 15th century, Mahmood Shah lost most of his empire and ruled only Bidar (Karnataka).   ",
    // 126
    "Ala-ud-Din Hasan Bahman Shah": " Ala-Ud-Din Hasan Bahman Shah  Alauddin Hasan Bahman Shah (1290\u20131358) founded the Bahmani Sultanate in 1347, making it the first independent Muslim kingdom in the Deccan after rebelling against the Tughlaq dynasty. He gained prominence by leading the siege of Gulbarga (now Kalaburagi, Karnataka) and later overthrew Ismail Mukh to establish his rule. His conquests expanded the Bahmani Sultanate to Kotgir, Qandhar, and Telangana, though his reign was marked by frequent conflicts with the Vijayanagara Empire.   ",
    // 127
    "Jawhar": " Jawhar  Jawhar, Jawhar is a historic city and hill station in Palghar district. It was the capital of the Jawhar princely state, ruled by the Mukne dynasty of the Warli communities under British India. In June 1306, he conquered the fort of Jawhar and went on to capture 22 forts across the Nashik and Thane districts.   ",
    // 128
    "Western Chalukyas": " Western Chalukyas The Western Chalukya Empire (973-1190 CE), also known as the Kalyani Chalukyas, was a major Indian dynasty that ruled most of Deccan India . Their rule marked a golden period of architecture, administration, and military power in South India. Founded by Tailapa II after defeating the Rashtrakutas, the empire initially had its capital at Manyakheta (Karnataka). In 1042, Someshvara I shifted the capital to Kalyani (present-day Basavakalyan, Karnataka). The Western Chalukyas were in constant conflict with the Chola dynasty over Vengi (Andhra Pradesh) but maintained control over Konkan, Gujarat, Malwa, and Kalinga. In 1076, Vikramaditya VI took over, and his fifty-year reign was the empire\u2019s most successful. However, by the mid-12th century, the empire began to decline.   ",
    // 129
    "Vidarbha Kingdom": " Vidarbha Kingdom The Vidarbha Kingdom was an ancient Indian kingdom mentioned in the Mahabharat and other ancient texts. It was located in what is now eastern Maharashtra and parts of Madhya Pradesh. Vidarbha is also historically significant as a political and cultural center in central India. The kingdom is most famously well-known for its association with Rukmini; the daughter of Bhishmaka, the king of the Vidarbha kingdom, and the first wife of Bhagwan Krishna. Various dynasties inlduing the Mauryas, Satavahanas, Vakatakas, and Chalukyas controlled Vidarbha at times. It became Part of Berar Province under the Mughals and British.   ",
    // 130
    "Marathas": " Marathas The Maratha Empire, led by Chhatrapati Shivaji Maharaj (the first king), was formed in the late 17th century and became one of the most powerful empires in Indian history. It played a crucial role in ending Mughal rule and resisting British expansion before its decline in 1818. They ruled from Raigad as its capital. At its peak in 1758, the Maratha Empire controlled a vast region covering almost two-thirds of the Indian subcontinent. In the north, it reached Attock (now in Pakistan) and Punjab, briefly controlling Delhi. To the south, Maratha influence extended deep into Tamil Nadu and Karnataka, including Thanjavur. In the west, they ruled over Gujarat, Maharashtra, and parts of Rajasthan, while in the east, their dominance spread across Orissa, Bengal, and parts of modern-day Bangladesh. The central regions of Madhya Pradesh, Chhattisgarh, and Telangana were also under Maratha control, making them the most powerful force in India by the mid-18th century. It is belived that after Shivaji\u2019s empire expanded, the administration became complex, and by the early 18th century, the empire transitioned into a confederacy led by Peshwas and powerful houses suhc as : Holkars (Indore) \u2013 Ruled Malwa and Central India, Scindias (Gwalior) \u2013 Controlled North India and Delhi, Gaekwads (Baroda) \u2013 Dominated Gujarat, Bhonsles (Nagpur) \u2013 Ruled Central & Eastern India (Orissa, Chhattisgarh). After the Battle of Panipat (1761), internal conflicts weakened Maratha unity. The British exploited their divisions, defeating them in the Anglo-Maratha Wars (1775\u20131818). By 1818, the Maratha Confederacy collapsed, and the British became the dominant power in India.   ",
    // 131
    "Bhagwat Purana": " Bhagwat Purana The Bhagwat Purana is one of Hinduism's eighteen major Puranas (a vast genre of encyclopedic Indian literature encompassing a wide range of legends and traditional lore). Originally composed in Sanskrit, the Bhagwat Purana, emphasizes devotion towards Krishna, an avatar of Vishnu. The Bhagwat Purana discusses a wide range of topics including cosmology, astronomy, geography, culture, legends, etc. The text consists of 12 books, 335 chapters, and 18,000 verses. Among these, the tenth book is the most popular and widely studied book. It narrates the famous episode of Rasa Lila, the episode depicts Krishna dancing with the Gopis.  ",
    // 132
    "Kundinapuri": " Kundinapuri Kundinapuri (the present-day town of Kaundinyapur in Amravati, Maharashtra) was the capital of the ancient Vidarbha kingdom. Kundinapuri served as a gateway for ancient travellers travelling between North India and South India. It was well connected to northern cities of ancient India like Ayodhya and other cities like Avanti and Nishadha. This route is also mentioned in the Mahabharat. Kundinapuri is believed to be the site of the Rukmini Haran, the incident where Krishna elopes with Rukmini.   ",
    // 133
    "Ellichpur": " Ellichpur Ellichpur, now Achalpur, is located in the Amravati district. Historically, in the 8th century, it served as the capital of the Rashtrakuta dynasty and was a battleground between the Rashtrakutas and the Kalachuris. It came under the Delhi Sultanate in 1318 and was later ruled by the Bahmani Kingdom from 1347. In the 15th century, Fathullah Imad-ul-Mulk, founder of the Imad Shahi dynasty, declared independence and made Ellichpur his capital. The city later fell under Mughal rule, followed by the Nizam of Hyderabad, and eventually British administration.  ",
    // 134
    "Fathullah Imad-ul-Mulk": " Fathullah Imad-Ul-Mulk Fathullah Imad-ul-Mulk, the founder of the Imad Shahi dynasty and the Berar Sultanate, was initially the governor of Berar, appointed by Mahmud Gawan. During the unrest in the Bahmani Sultanate in 1490, he declared himself Sultan of Berar. He conquered Mahur (present-day Nanded, Maharashtra) and made Ellichpur his capital. During his reign, he fortified the Gavilgad and Narnala forts. He ruled until 1504 and was succeeded by his son, Alauddin Imad Shah.  ",
    // 135
    "Qasim Barid I": " Qasim Barid I Qasim Barid I, the prime minister of the Bahmani Sultanate, later founded the Bidar Sultanate. He served under Bahmani Sultan Muhammad Shah III. He revolted against the Sultanate and appointed himself vizier (chief minister). However, the Bahmani governors refused to recognize his authority and declared independence, leading to the formation of the Ahmednagar, Bijapur, and Berar Sultanates. He established the Bidar Sultanate in 1492 and ruled until his death in 1504.  ",
    // 136
    "Malik Ambar": " Malik Ambar  Malik Ambar (1548\u20131626) served as the Peshwa (Prime Minister) of the Ahmadnagar Sultanate and its ruler from 1600. Originally a slave from Ethiopia, he rose through the ranks to become Prime Minister. His guerrilla warfare techniques were well known in the Deccan region. Under the Nizam Shahi dynasty of Ahmednagar, he served as a regent and successfully resisted Mughal Emperor Jahangir. He changed the capital to Khadki, which he founded in 1610; it was later renamed Aurangabad by Aurangzeb (now Chhatrapati Sambhaji Nagar). Eventually, he was defeated by Shah Jahan and ceded control of Berar and Ahmadnagar to the Mughals. He built the Neher water system of Khadki and is also credited with constructing the famous Janjira Fort in the Murud area (Raigad). He was known for his leadership and administrative skills.   ",
    // 137
    "King Ramachandra": " King Ramachandra Ramachandra was a ruler of the Yadava dynasty in the Deccan region. He seized the throne from his cousin Ammana and expanded his kingdom through battles against the Paramaras of Malwa, the Vaghelas of Gujarat and Rajasthan, and the Hoysalas of Karnataka. In 1296, Alauddin Khalji of the Delhi Sultanate invaded Devagiri, forcing Ramachandra to pay an annual tribute. When he stopped payments in 1303\u20131304, Alauddin sent his general Malik Kafur, who led another invasion in 1308, capturing Ramachandra and taking him to Delhi. However, Alauddin reinstated him as a vassal, granting him the title Raja-i-Rajan (\"King of Kings\"). Ramachandra remained loyal to Alauddin until his death and assisted Malik Kafur in defeating the Kakatiyas (1309) and the Hoysalas (1311).  ",
    // 138
    "Pir Khan": " Pir Khan Pir Khan (Khan Jahan Lodi) was an Afghan noble who served under the Mughal Empire. In 1609, he was appointed governor of the Deccan and later became the governor of Multan in 1620. In 1626, during Jahangir\u2019s reign and amidst political chaos, he allied with the Nizam Shahis and handed over Balaghat (Madhya Pradesh) to them. Under Shah Jahan\u2019s rule, he was ordered to reclaim these territories but fled to the court of Murtaza Nizam Shah II, prompting Shah Jahan to send 50,000 troops southward. After several battles, he was defeated while attempting to escape toward Punjab and was killed in February 1631. During Jahangir\u2019s reign, he also sponsored Tarikh-i-Khan-Jahani, a Persian historical text documenting the early history of the Afghans and his own biography.   ",
    // 139
    "Jahangir": " Jahangir Jahangir (1569\u20131627) was the fourth Mughal emperor, ruling from 1605 to 1627. Born in Fatehpur Sikri, he was the third son of Akbar. He took over after his father\u2019s death, but his reign was marked by internal conflicts with his son. He conquered the Kangra Fort (Himachal Pradesh) in 1615 and the district of Kishtwar (Jammu and Kashmir) in the same year. In 1616, he sent troops along with his son, Shah Jahan, to capture Ahmednagar, Bijapur, and Golconda. He introduced the Golden Chain of Justice at Agra Fort, allowing anyone to seek justice directly from him. His memoir, Tuzk-e-Jahangiri (Jahangirnama), is an autobiography in Persian where he documented his reign, as well as his reflections on art and politics. He died in October 1627 due to poor health, and his son Shah Jahan succeeded him.  ",
    // 140
    "Shah Jahan": " Shah Jahan Shah Jahan, the fifth Mughal emperor (1592\u20131666), ascended the throne in 1628 after his father Jahangir\u2019s death, crowning himself emperor in Agra Fort after defeating his brothers. As a prince, he made significant military contributions, beginning with the Rajput state of Mewar in 1615 and the Deccan in 1616. During his reign, he captured Daulatabad (Devagiri), Bijapur, and Golconda, as well as Kandahar (present-day Afghanistan) from the Safavids in 1638. Shah Jahan left behind a lasting legacy, particularly in Mughal architecture, most notably the Taj Mahal, built in memory of his wife, Mumtaz Mahal, a project that took 22 years. He also commissioned the Red Fort (Lal Qila), Agra Fort, and Jama Masjid (Delhi). His son Aurangzeb imprisoned him in Agra Fort from July 1658 until his death in January 1666.   ",
    // 141
    "Peshwa Madhavrao I": " Peshwa Madhavrao I Madhavrao I (1745\u20131772) was the 9th Peshwa of the Maratha Empire. He was the son of Nana Saheb and the grandson of Peshwa Bajirao I. After the Marathas\u2019 heavy losses at the Third Battle of Panipat in 1761 and the deaths of his father and brother, he ascended the throne at just 16. Despite inheriting a weakened empire and facing internal conflicts with his uncle Raghunathrao, he restored Maratha power. In 1763, he defeated the Nizam of Hyderabad in the Battle of Rakshasbhuvan (Beed). In 1769, he recaptured territories in northern India, including Udaipur and Bharatpur (Rajasthan). In 1771, he successfully restored Maratha control over Delhi. Suffering from a chronic illness, he chose to spend his last days at the Ganesha Chintamani Temple in Theur (Pune) and died on 18 November 1772 at the age of 27. His early death was a major blow to the Maratha Confederacy, with many historians believing it had a greater impact than their defeat at Panipat.  ",
    // 142
    "Chalukyas of Badami": " Chalukyas Of Badami The Badami Chalukya dynasty was established by Pulakeshin I in 543, with Vatapi (modern Badami, Karnataka) as its capital. They ruled over Karnataka and Andhra Pradesh. His descendant, Pulakeshin II, expanded the empire across the Deccan, defeating Harsha in the north and the Pallava kingdom in the south. However, in 642, Pallava king Narasimhavarman attacked and occupied Badami. The kingdom was later restored during the reign of Vikramaditya I in 696. It reached its peak under Vikramaditya II, who captured territories from the Pandyas and the Cholas. The dynasty ended in 753 when Kirtivarman II was overthrown by the Rashtrakutas.   ",
    // 143
    "Abhiras": " Abhiras The Abhira dynasty ruled parts of western and central India, founded by Ishwarsena around 250 CE after the decline of the Satavahana Empire. As mentioned in the Mahabharat, the Abhiras originally resided along the banks of the Saraswati River near Somnath (Gujarat). Under Ishwarsena\u2019s rule, their territory included present-day Jalgaon, Dhule, Nandurbar, Nashik, Andhra Pradesh, and Gujarat, leaving a lasting impact on the region.   ",
    // 144
    "Delhi Sultanate": " Delhi Sultanate The Delhi Sultanate was a late medieval empire that ruled from the 13th to the 16th century. Established in 1206, it was divided into five dynastic periods. The Mamluk Dynasty (1206\u20131290) was founded by Qutb-ud-din Aibak, a general of Muhammad Ghori, who formally established the sultanate. Notable rulers like Iltutmish and Balban strengthened the administration and expanded the empire to Multan and Bengal. The Khalji Dynasty (1290\u20131320), founded by Jalal-ud-din Khalji, saw its greatest expansion under Ala-ud-din Khalji, who conquered Gujarat, Rajputana, Malwa, and the Deccan. The Tughlaq Dynasty (1320\u20131414), established by Ghiyas-ud-din Tughlaq, saw Muhammad bin Tughlaq rule for over 26 years, during which the empire briefly covered almost the entire Indian subcontinent. The Sayyid Dynasty (1414\u20131451), founded by Khizr Khan, ruled as vassals of Timur, struggling to maintain control. The Lodi Dynasty (1451\u20131526), established by Bahlul Lodi, expanded from Delhi to Bihar but was overthrown when Babur defeated Ibrahim Lodi in the First Battle of Panipat (1526), marking the end of the Sultanate and the beginning of Mughal rule in India.  ",
    // 145
    "Third Battle of Panipat": " Third Battle Of Panipat The Third Battle of Panipat took place on 14 January 1761 between the Maratha Empire and the Durrani Empire, led by Ahmad Shah Abdali. It was one of the largest battles fought in the 18th century, involving over 125,000 soldiers. The battle resulted in a decisive victory for Abdali, leading to massive casualties for the Marathas, with an estimated 40,000 killed. The loss weakened Maratha influence in northern India.  ",
    // 146
    "Chalukyas from Kalyani": " Chalukyas From Kalyani The Western Chalukya Empire ruled most of the Deccan region between the 10th and 12th centuries. Founded by Tailapa II after defeating the Rashtrakutas, the empire initially had its capital at Manyakheta (Karnataka). In 1042, Someshvara I shifted the capital to Kalyani (present-day Basavakalyan, Karnataka). The Western Chalukyas were in constant conflict with the Chola dynasty over Vengi (Andhra Pradesh) but maintained control over Konkan, Gujarat, Malwa, and Kalinga. In 1076, Vikramaditya VI took over, and his fifty-year reign was the empire\u2019s most successful. However, by the mid-12th century, the empire began to decline.  ",
    // 147
    "Rashtrakuta Empire": " Rashtrakuta Empire The Rashtrakuta Empire (753\u2013982 CE) was a dominant power in the Indian subcontinent, established by Dantidurga, who overthrew the Chalukyas of Badami and made Manyakheta (modern-day Malkhed, Karnataka) his capital. His successor, Krishna I, expanded the empire by capturing major regions, including present-day Karnataka and Konkan. Under rulers like Dhruva Dharavarsha, Govinda III, and Amoghavarsha I, the Rashtrakutas extended their domain to Gujarat, Maharashtra, Madhya Pradesh, Tamil Nadu, and Andhra Pradesh. . Despite a few rulers in between, the last great ruler, Krishna III, expanded the empire from the Narmada to the Kaveri River. By 972 CE, the empire declined and was eventually overthrown by the Western Chalukyas.The Rashtrakutas were great patrons of art and architecture, building Hindu and Jain temples, including the Kailasanatha Temple at Ellora.   ",
    // 148
    "Junnar": " Junnar Junnar is a city in the Pune district, historically known as an important trading center. In 1490, under the Nizam Shahi dynasty, Junnar served as their capital city, a status it retained even later under Malik Ambar in the 1600s. Shahji Bhonsale, the father of Chhatrapati Shivaji Maharaj, worked under Malik Ambar, and Shivaji was born at Shivneri Fort in Junnar. The city is also home to more than 200 rock-cut caves, featuring significant Buddhist and Hindu temples. Prominent cave sites include Shivneri, Manmodi, and Lenyadri.  ",
    // 149
    "Maloji Bhonsale": " Maloji Bhonsale Maloji Bhonsale (1552\u20131605) was a Maratha chief who served the Ahmadnagar Sultanate. In 1577, he and his brother joined the service of Murtaza Nizam Shah I and later became a trusted aide of Malik Ambar. Rising rapidly, he was granted the title of Raja and the jagir of Pune, gaining control over Shivneri and Chakan forts. He died in battle against the Bijapur Sultanate. His legacy was carried forward by his son Shahji Bhonsale and later by his grandson Shivaji, the founder of the Maratha Empire.   ",
    // 150
    "Shahaji Bhonsale": " Shahaji Bhonsale Shahaji Bhonsale (1594\u20131664) was a military leader who served the Ahmadnagar, Bijapur, and Mughal Sultanates at different times. He initially served under Malik Ambar, the prime minister of the Ahmadnagar Sultanate, and inherited the Pune jagir from his father, Maloji Bhonsale. He frequently shifted allegiance between Ahmadnagar and Bijapur. In 1629, he led a campaign against the Mughal Emperor Shah Jahan in the Khandesh region (present-day Jalgaon, Dhule, Nandurbar) but was defeated. As the chief minister of Ahmadnagar, he captured Junnar (Pune) and parts of Konkan, but in 1634, the Mughals launched a campaign against him. Later, in 1638, he was granted jagirs in Bangalore and was allowed to rule semi-independently.  ",
    // 151
    "Narayan Rao": " Narayan Rao Narayan Rao (1755\u20131773) was the 10th Peshwa of the Maratha Empire. He was the third son of Balaji Baji Rao (Nana Saheb). His brother Madhavrao appointed him as the next Peshwa right before he died. He started ruling from 1772 but faced constant conflicts with his uncle Raghunathrao. During his reign, he dealt with British naval aggression along the Konkan coast and successfully defended Vasai, Ratnagiri, Thane. Despite strict confinements on Raghunathrao, Narayan Rao was assassinated in 1773 at Shaniwar Wada, Pune, allegedly at the orders of Raghunathrao\u2019s wife, Anandibai.   ",
    // 152
    "Mahadaji Shinde": " Mahadaji Shinde Mahadaji Shinde (1730 \u2013 1794) was a Maratha general and the ruler of Gwalior. He played a crucial role in restoring Maratha power after the Third Battle of Panipat (1761) as a key lieutenant to the Peshwa. He reasserted Maratha control over Delhi, reinstating Mughal Emperor Shah Alam II as a puppet ruler, and served as his deputy regent. Throughout his lifetime, he fought in over 50 battles, defeating the Jats and Rohillas. His role in the First Anglo-Maratha War (1775\u20131782) was instrumental, particularly in the Maratha victory over the British in the Battle of Wadgaon (1779). Later, in 1782, he mediated the Treaty of Salbai between the Peshwas and the British, ensuring peace and securing Maratha dominance. He passed away in 1794, and his memorial, Shinde Chhatri, stands in Pune.  ",
    // 153
    "Baji Rao II": " Baji Rao Ii Baji Rao II (1775\u20131851) was the 13th and last Peshwa of the Maratha Empire. He was the son of Raghunathrao and was appointed as a puppet Peshwa after the death of Madhavrao II. In 1802, the Holkars defeated the combined forces of the Peshwas and Scindias. Later, Baji Rao II sought assistance from the British, leading to the signing of the Treaty of Bassein in December 1802, after which he was reinstated as the Peshwa by the British. Other Maratha chieftains were unhappy with this decision, leading to the Second Anglo-Maratha War (1803\u20131805), which further contributed to the downfall of the Maratha Confederacy. After his defeat at the Battle of Koregaon in 1818, he surrendered and was moved to Bithur (Kanpur, Uttar Pradesh), where he lived until his death in 1851.   ",
    // 154
    "Jyotirao Phule": " Jyotirao Phule Jyotirao Phule (1827\u20131890) was a social reformer, activist, businessman, and writer. He was a strong advocate for abolishing the caste system and promoting education for women and marginalized communities. In 1848, along with his wife, Savitribai Phule, he established the first school for girls in Pune. He also founded the Satyashodhak Samaj in 1873 to promote equality for lower-caste communities. In 1876, he was appointed as a commissioner of the Pune municipality. His legacy remains significant; he was honored with the title of Mahatma in 1888. His work continues to inspire many and is reflected in various structures and places named after him.   ",
    // 155
    "Peshwas": " Peshwas The Peshwas were initially the Prime Ministers of the Maratha Empire and ranked second in prestige after the Chhatrapatis. The position was first held by Moropant Trimbak Pingle under Shivaji. However, it was under Balaji Vishwanath (1713\u20131720) that the office became hereditary to the Bhat family under Shahu. Baji Rao I and Balaji Baji Rao expanded the Maratha Empire across the Indian subcontinent. After the Marathas' defeat in the Third Battle of Panipat in 1761, they lost significant power. The last Peshwa, Baji Rao II, was defeated by the British in the Third Anglo-Maratha War, marking the end of the Peshwa era.  ",
    // 156
    "Baji Rao I": " Baji Rao I Baji Rao I (1700\u20131740) was the 7th Peshwa of the Maratha Empire. Appointed by Chhatrapati Shahu in 1720, he played a crucial role in expanding Maratha influence across India. He led successful campaigns against the Nizam of Hyderabad, defeating him in the Battle of Palkhed (1728). In 1737, he defeated the combined forces of the Mughals, Nizam, Rajputs, and the Nawab of Oudh in the Battle of Bhopal, securing Malwa for the Marathas. He passed away in 1740 at the age of 39 in Raverkhedi (Madhya Pradesh). His legacy remains immense, as he is regarded as one of the greatest Peshwas and military strategists, known for his swift warfare tactics.   ",
    // 157
    "Chhatrapati Shivaji Maharaj": " Chhatrapati Shivaji Maharaj Shivaji Bhonsale (1630\u20131680) was the founder of the Maratha Empire and one of India's greatest warrior-kings. Born in Shivneri Fort (Junnar, Pune), he was trained in military and administration from a young age. In 1646, he began his conquests by capturing Torna, Purandar, Kondhana, Chakan, and Kalyan, establishing his dominance in the region. In 1663, he launched an attack on Mughal general Shaista Khan, forcing him to retreat. However, in 1665, facing a massive Mughal force led by Raja Jai Singh I, Shivaji agreed to the Treaty of Purandar, ceding 23 forts. In 1674, he was formally crowned Chhatrapati at Raigad Fort. That same year, he expanded his empire by capturing Kolhapur and Ponda (Goa). In 1677, he launched successful campaigns in the south, capturing parts of Mysore and Tamil Nadu. Recognizing the importance of naval power, he established a strong navy and built coastal forts like Sindhudurg to protect the Konkan coast. He passed away in 1680 at Raigad Fort, leaving behind a powerful legacy and a strong Maratha Empire.  ",
    // 158
    "Balaji Baji Rao": " Balaji Baji Rao Balaji Baji Rao (1720\u20131761) was the 8th Peshwa of the Maratha Confederacy. He was appointed Peshwa after the death of his father, Baji Rao I, in 1740. During his reign, the Maratha Empire expanded significantly, reaching Peshawar in the north, Bengal in the east, and Karnataka in the south. He successfully resisted attacks from the Mughals, the Nizam of Hyderabad, and the Bengal Sultanate. From the late 1750s, the Marathas were engaged in continuous conflicts with Ahmad Shah Durrani. Between 1759 and 1761, the Marathas and the Durranis clashed repeatedly, resulting in the Third Battle of Panipat, where the Marathas suffered a devastating defeat. In the battle, he lost his eldest son, Vishwasrao, which deeply affected him. He died in June 1761, just months after the battle, and was later succeeded by his younger son, Madhavrao I.  ",
    // 159
    "Moropant Trimbak Pingle": " Moropant Trimbak Pingle Moropant Trimbak Pingle (1620\u20131683) was the first Peshwa (Prime Minister) of the Maratha Empire, appointed by Chhatrapati Shivaji in 1674. He played a crucial role in Shivaji\u2019s military campaigns, including the 1659 battle against Adil Shah, the invasion of Surat, and battles at Dindori (Madhya Pradesh) and Salher (Nashik) against the Mughal Empire. Moropant was also instrumental in revenue administration, resource planning, and the construction of forts like Pratapgad. After Shivaji\u2019s death in 1680, he continued to serve under Sambhaji, participating in the Battle of Burhanpur in 1681, but was later killed by Mughal forces in 1683.  ",
    // 160
    "Maharani Tarabai Bhosale": " Maharani Tarabai Bhosale Maharani Tarabai Bhosale (1675\u20131761) was the regent of the Maratha Kingdom from 1700 to 1714. She was the wife of Chhatrapati Rajaram I. After her husband\u2019s death in 1700, she declared her infant son, Shivaji II, as the ruler and led the Maratha resistance against Aurangzeb. A skilled strategist, she led the Maratha resistance against the Mughal Emperor Aurangzeb. However, after Shahu I was released by the Mughals in 1707 and claimed the Maratha throne, a conflict arose. Tarabai was eventually sidelined, and Shahu took control, leading her to establish a separate rule in Kolhapur. Tarabai remained a key political figure in the Maratha court until her death in 1761.  ",
    // 161
    "Mahmud Gawan": " Mahmud Gawan Mahmud Gawan was a chief minister of the Bahmani Sultanate from 1458 and later became its prime minister in 1466. He was given the title Malik-ut-Tujjar (Prince of Merchants) by Humayun Shah. He served as a noble in the court of Ahmad Shah II and later became a regent to the young Nizam Shah. He played a crucial role in expanding the Sultanate, leading successful campaigns in Konkan, Andhra, Goa, and against the Gajapati rulers of Orissa. In the 1460s, he successfully defended the Bahmani Sultanate against repeated invasions by Mahmud Khalji of Malwa. He led a major campaign against the Vijayanagara Empire in 1469, capturing Kanjeeveram and the Konkan region. In 1481, Sultan Muhammad Shah III, influenced by court conspiracies, ordered his execution. His death led to instability, eventually resulting in the Sultanate's fragmentation by the early 1490s.  ",
    // 162
    "Balaji Vishwanath": " Balaji Vishwanath Balaji Vishwanath (1662\u20131720) was the first Peshwa from the Bhat family. He started out as the head administrator of Pune and Daulatabad. Later, he played a key role in securing Shahu's claim to the Maratha throne. He conquered most of the Konkan coast, after which Chhatrapati Shahu appointed him as Peshwa in November 1713. He played a crucial role in negotiating with the Mughals for chauth and sardeshmukhi (taxes). In 1719, he emerged victorious in the Battle of Panhala (Kolhapur district). He died in 1720 and was succeeded by his son, Baji Rao I.  ",
    // 163
    "Third Anglo-Maratha War": " Third Anglo-Maratha War The Third Anglo-Maratha War (1817\u20131819) was the final conflict between the Maratha Empire and the British East India Company, marking the end of Maratha rule in India. The Maratha forces, led by Peshwa Baji Rao II, along with Mudhoji II Bhonsle of Nagpur and Malharrao Holkar III of Indore, aimed to reclaim their lost power after the Treaty of Bassein. The British army, under Governor-General Lord Hastings, emerged victorious. The Peshwa launched an attack in the Battle of Khadki (1817), but the British defeated him, leading to the surrender of Pune. By April 1818, British forces had taken control of Satara, Sinhagad, and Purandar. The Marathas continued their resistance in battles like Koregaon (1818), but they were ultimately overpowered. Baji Rao II was exiled to Bithur, the Bhonsles were defeated at the Battle of Sitabuldi (Nagpur), and the Holkars at the Battle of Mahidpur (Malwa). The war led to the dissolution of the Maratha Confederacy, with most of its territories annexed into British India as princely states.  ",
    // 164
    "Miraj": " Miraj Miraj, a historic city in Maharashtra, was under the rule of the Shilaharas of Kolhapur in the 10th century. In 1216, it was conquered by the Yadavas of Devagiri and later fell under the Bahmani Sultanate in 1318. In the 15th century, it came under the rule of the Adil Shahi dynasty of Bijapur. After the decline of the Adil Shahi rule, Miraj remained under the Mughal Empire until 1739, when it was captured by Chhatrapati Shahu. During British rule, it became part of the Bombay Presidency and was governed by the Patwardhan dynasty as a princely state under British influence. Miraj is also renowned for its contribution to Indian classical music, particularly for producing exceptional sitar players, as well as manufacturing high-quality musical instruments.  ",
    // 165
    "Mudhoji Bhonsle": " Mudhoji Bhonsle Mudhoji Bhonsle (1772\u20131788) was the ruler of the Nagpur Kingdom. His elder brother, Janoji, had appointed Mudhoji\u2019s infant son as the next ruler, making Mudhoji the regent. From 1772, he began regaining power and also established agreements with the British. In 1778, on the advice of Nana Phadnavis, he fought against Tipu Sultan\u2019s forces. In 1785, he expanded the Nagpur Kingdom by acquiring Mandla (Madhya Pradesh) through a deal with the Poona government. He died in 1788, after which his son, Raghoji II Bhonsle, succeeded him.  ",
    // 166
    "Bithoor": " Bithoor Bithoor, also called Bithur, is in the Kanpur district of Uttar Pradesh and is situated on the banks of the river Ganga. After the Third Anglo-Maratha War, Baji Rao II was exiled to Bithur, and later, his son Nana Sahib made it his headquarters. Bithur is closely associated with the Rebellion of 1857 and was captured by General Havelock on 19 July 1857 in retaliation for the attack on British civilians in Cawnpore (Kanpur). The British army destroyed Nana Sahib\u2019s palace and temples.  ",
    // 167
    "Panhala": " Panhala Panhala is a historic hill station in Kolhapur, Maharashtra. Originally the headquarters of the Shilahara dynasty in the 12th century, it later came under the control of the Yadavas of Devagiri, the Bahmani Sultanate, and the Adil Shahi dynasty of Bijapur. In 1659, Chhatrapati Shivaji Maharaj attempted to capture Panhala and successfully conquered it in 1673. Afterward, the fort frequently changed hands between the Marathas and the Mughals before eventually being taken over by the British in 1844.  ",
    // 168
    "Puranas": " Puranas The Puranas, ancient Hindu texts, contain historical accounts and religious teachings, describing the origins, significance, and sanctity of various temples, including the Mahalaxmi Mandir in Kolhapur. The Skanda Purana, one of the largest Mahapuranas, is primarily dedicated to Lord Kartikeya (Skanda) and includes regional legends, as well as spiritual teachings. Similarly, the Devi Bhagavata Purana glorifies Devi Durga and Shakti, emphasising her supreme power in creation, protection, and destruction. These texts mention Kolhapur as a sacred Shakti Peetha, highlighting its religious importance in Hindu tradition. Source: \"Shakta Traditions in Ancient India\" (academic studies on Shakti Peethas)   ",
    // 169
    "Ptolemy": " Ptolemy Ptolemy (c. 100\u2013170 CE) was a Greek-Egyptian geographer, mathematician, and astronomer who lived in Alexandria, Egypt. He is renowned for mapping various regions of the ancient world. In his writing, Geography by Claudius Ptolemy (J.L. Berggren & Alexander Jones eds. & trans., Princeton Univ. Press 2000) he referred to Kolhapur as \"Hippokoura,\" highlighting its significance as an important trade and cultural centre in ancient India.   ",
    // 170
    "Ambabai": " Ambabai  \"Ambabai\" is a local name for Devi Mahalaxmi in Kolhapur district. The term combines \u201cAmba\u201d (Devi Ma) and \u201cBai\u201d (a respectful term for women in Marathi), signifying her as the pavitra devi and protector of the region. Source: Locals   ",
    // 171
    "Karavira": " Karavira Karavira, is the ancient name of Kolhapur mentioned in Hindu scriptures like the Skanda Purana (Karvir Mahatmya). Over time, the name evolved, and today, Kolhapur is its widely recognised name. The term Karavira refers to the region where Devi Mahalaxmi (Ambabai) is believed to reside permanently. Source: Bombay Presidency Gazetteer (1886) Kolhapur   ",
    // 172
    "Satara": " Satara Satara, located near Kolhapur in Maharashtra, shares a rich historical and cultural connection with its neighbouring district. Established in the 17th century by Chhatrapati Shivaji Maharaj, Satara served as a significant centre during the Maratha Empire. Both regions played pivotal roles in resisting Mughal expansion and fostering Marathi culture. During the British colonial era, Satara, along with Kolhapur, was part of the Bombay Presidency, where British administrators implemented political and economic reforms, shaping the region\u2019s governance and infrastructure while also influencing local resistance movements. (See Satara district for more).   ",
    // 173
    "Peshwa's": " Peshwa'S  Peshwa\u2019s- The Peshwas were considered to be prime ministers of the Maratha Empire. They originally served under the Chhatrapati but later became the de facto rulers of the empire.   ",
    // 174
    "Peshwa Bajirao": " Peshwa Bajirao  Peshwa Bajirao- Peshwa Bajirao I (1700\u20131740) was one of the Maratha Peshwas (prime ministers)and a brilliant military strategist who expanded Maratha's power across India. It is argued that he never lost a battle and is known for his swift cavalry tactics. Sources: Sen, S. N. (1928). Administrative System of the Marathas. Calcutta University. Gordon, S. (1993). The Marathas 1600-1818. Cambridge University Press.   ",
    // 175
    "Ramji Shirsat": " Ramji Shirsat Ramji Shirsat- \u200bRamji Shirsat was one of the prominent local figures in the 1857 revolt in Kolhapur. On 31, July 1857, he led approximately 200 sepoys, primarily Pardesis and Marathas, in an attempt to free the country from the British rule in India. They attacked the regimental treasury and the quarters of European officers before marching towards Ratnagiri to join forces with others. Despite initial successes, the revolt was eventually suppressed by the British, leading to the execution of twenty-six local individuals, including Shirsat, who was shot dead. \u200b Source: International Journal of Research in Social Sciences, Revolt of 1857 in India: A Geographical Perspective.  ",
    // 176
    "Mavlan": " Mavlan  Malvan- Malvan, a coastal town in Maharashtra's Sindhudurg district, is renowned for its historical Sindhudurg Gadh, constructed in the 17th century by Chhatrapati Shivaji Maharaj. Situated on a rocky island just off Malvan's coast, the gadh is accessible by boat and exemplifies Maratha military architecture. While Malvan is approximately 120 kilometres from Kolhapur, there isn't a gadh named \"Malvan Gadh\" within Kolhapur itself. \u200b(See Sindhudurg for more).   ",
    // 177
    "Peshwa Patwardhan Kannherrao Trimbak": " Peshwa Patwardhan Kannherrao Trimbak Peshwa Patwardhan Kannherrao Trimbak was a notable figure in the 18th-century Maratha Empire, associated with the influential Patwardhan family. During the reign of Shivaji II of Kolhapur (1762\u20131812), the kingdom faced vulnerabilities due to internal and external pressures. This period saw incursions by forces including those led by Kannherrao Trimbak Patwardhan and Pant Pratinidhi of Aundh. These raids, alongside other challenges, underscored the complex political dynamics within the Maratha confederacy and the struggles for dominance among its chieftains. \u200b   ",
    // 178
    "Battle of Panipat": " Battle Of Panipat Battle of Panipat- The Third Battle of Panipat (1761) was a decisive conflict between the Marathas, led by Sadashivrao Bhau, and the Durrani Empire, led by Ahmad Shah Abdali. It was fought near Panipat (Haryana) and marked one of the most significant battles in Indian history. It is argued that The Marathas, despite their military strength, suffered a crushing defeat due to strategic miscalculations, lack of supplies, and betrayal by allies. This battle significantly weakened Maratha's power in northern India, allowing the British to strengthen their foothold. However, the Marathas later regained dominance under Peshwa Madhavrao I.   ",
    // 179
    "Parasurambhau Patavardhana": " Parasurambhau Patavardhana Parasurambhau Patavardhana- \u200bParasurambhau Patavardhana was a prominent figure in the late 18th-century Maratha Empire, belonging to the influential Patavardhan family. He allied with the British during certain military campaigns. Upon returning to his saranjam (a type of feudal land grant), he initiated a series of aggressive actions against neighbouring territories, reflecting the complex and often tumultuous political landscape of the time.   ",
    // 180
    "Name and Treaty": " Name And Treaty Name and treaty- The specific name of the 1812 treaty between the British and Raja Shivaji II of Kolhapur is not explicitly mentioned in the available historical records. It is commonly referred to as the Treaty of 1812 or the Treaty of 1 October 1812  ",
    // 181
    "River Arno": " River Arno River Arno - \u200bRajaram II, the Maharaja of Kolhapur, passed away in Florence, Italy, in 1870 during his return journey from England. His attendants sought to perform a traditional Hindu cremation, which was uncommon in Italy at that time. Despite local prohibitions against cremation, the Italian authorities granted special permission, allowing the ceremony to take place at the confluence of the Arno and Mugnone rivers. This event marked one of the earliest modern cremations in Italy and led to the erection of the Monumento all'Indiano in Florence to honor the Maharaja. \u200b   ",
    // 182
    "Lokmanya Tilak": " Lokmanya Tilak Lokmanya Tilak- Bal Gangadhar Tilak (1856\u20131920), popularly known as Lokmanya Tilak, was a prominent Indian nationalist, social reformer, and freedom fighter. He played a key role in the Indian independence movement, advocating Swaraj (self-rule) as India\u2019s birthright. Tilak was a strong critic of British rule and used newspapers like Kesari and Maratha to inspire nationalism. He also revived Ganesh Utsav and Shivaji Jayanti to unite Indians. As one of the Lal-Bal-Pal trio, he played a crucial role in the Swadeshi Movement. He was imprisoned several times and authored The Arctic Home in the Vedas and Gita Rahasya.   ",
    // 183
    "Gopalrao Agarkar": " Gopalrao Agarkar Gopalrao Agarkar- Gopal Ganesh Agarkar (1856\u20131895) was a prominent social reformer, journalist, and educationist in 19th-century India. A close associate of Bal Gangadhar Tilak, he co-founded the Deccan Education Society and played a key role in establishing Fergusson College in Pune. He was the first editor of Kesari but later founded Sudharak, advocating rationalism, social justice, and women\u2019s rights. Unlike Tilak, Agarkar emphasized social reforms over political freedom, especially against caste discrimination and child marriage. His progressive ideas made him a controversial yet significant figure in Maharashtra\u2019s reform movements.   ",
    // 184
    "Otto Rothfeld": " Otto Rothfeld Otto Rothfeld- \u200bOtto Rothfeld (1876\u20131932) was a British civil servant and author who served in the Indian Civil Service during the early 20th century. He is best known for his book Women of India, published around 1920, which provides an insightful exploration of the lives of Indian women across various social strata, from aristocracy to the working class. The book is notably illustrated by Mahadev Vishwanath Dhurandhar, a distinguished Indian artist. Rothfeld's work offers a detailed account of Indian women's roles, customs, and societal positions during that era.  ",
    // 185
    "S.M. Edwardes": " S.M. Edwardes  S.M. Edwardes- Stephen Meredyth Edwardes (1873\u20131927) was a distinguished British civil servant and a colonial historian, noted for his extensive work in India during the British Raj. Educated at Eton and Christ Church, Oxford, he joined the Indian Civil Service in 1896, serving in various administrative capacities. Edwardes made significant contributions to the documentation of Indian history and society through his writings. His notable works include The Gazetteer of Bombay City and Island (1909), By-Ways of Bombay (1912), and The Bombay City Police: A Historical Sketch, 1672\u20131916 (1923). He also collaborated on historical texts such as A History of the Mahrattas and The Oxford History of India. After retiring from the civil service, Edwardes served as the Secretary of the Royal Asiatic Society until he died in 1927. \u200b \u200b   ",
    // 186
    "Bal Gandadhar Tilak": " Bal Gandadhar Tilak Bal Gangadhar Tilak- 1856-1920 He was born in Ratnagiri, Tilak was a brilliant scholar and mathematician before becoming a revolutionary leader. He co-founded the Deccan Education Society to promote modern education but believed in blending it with Indian values. Though known for his slogan \"Swaraj is my birthright and I shall have it,\" few know that he first wrote it in his newspaper, Kesari, in 1896 during the plague epidemic in Pune, where he criticised British policies. Tilak was also a profound historian and Sanskrit scholar. His book \"The Arctic Home in the Vedas\" proposed that the original Aryans lived near the North Pole. Imprisoned for resistance, he spent six years in Mandalay Jail (1908-1914), where he wrote \"Gita Rahasya\", an interpretation of the Bhagavad Gita. A lesser-known fact is that he worked on reforming the Marathi calendar and was one of the first leaders to promote Ganesh Utsav and Shivaji Jayanti to unite people against British rule. Source: Brown, Judith M. Modern India: The Origins of an Asian Democracy (Oxford University Press, 1985).   ",
    // 187
    "King Krishna I": " King Krishna I King Krishna I (reigned circa 756\u2013774 CE) was a significant ruler of the Rashtrakuta dynasty, which dominated large parts of the Indian subcontinent between the 6th and 10th centuries. He ascended to power after his predecessor, Dantidurga, and played a pivotal role in consolidating and expanding the empire's territories. One of his notable achievements was the construction of the Kailasa mandir at Ellora, a monumental rock-cut temple renowned for its architectural brilliance. This mandir stands as a testament to the artistic and engineering prowess of his reign. Under Krishna I's leadership, the Rashtrakutas not only fortified their political dominance but also fostered a rich cultural and architectural legacy that continues to be celebrated today.\u200b   ",
    // 188
    "Punaka Wadi": " Punaka Wadi Punaka Vishaya / Punaka Wadi - The terms \"Punaka Vishaya\" and \"Punaka Wadi\" are historical references to the region now known as Pune. The term \"Vishaya\" denotes an administrative unit akin to a district. In the 8th century, copper plates from the Rashtrakuta dynasty referred to this area as \"Punaka Vishaya,\" highlighting its significance during that era. By the 10th century, inscriptions began using \"Punaka Wadi\" to describe the town, indicating its evolution over time. The prefix \"Punaka\" is derived from \"Punya,\" meaning divine, reflecting the region's esteemed status. These historical designations underscore Pune's longstanding importance as a cultural and administrative centre in ancient India.   ",
    // 189
    "Punaka Vishaya": " Punaka Vishaya Punaka Vishaya / Punaka Wadi - The terms \"Punaka Vishaya\" and \"Punaka Wadi\" are historical references to the region now known as Pune. The term \"Vishaya\" denotes an administrative unit akin to a district. In the 8th century, copper plates from the Rashtrakuta dynasty referred to this area as \"Punaka Vishaya,\" highlighting its significance during that era. By the 10th century, inscriptions began using \"Punaka Wadi\" to describe the town, indicating its evolution over time. The prefix \"Punaka\" is derived from \"Punya,\" meaning divine, reflecting the region's esteemed status. These historical designations underscore Pune's longstanding importance as a cultural and administrative centre in ancient India.   ",
    // 190
    "Naneghat": " Naneghat Naneghat - Naneghat is an ancient mountain pass in the Western Ghats of Maharashtra, historically significant as a trade route connecting the Konkan coast to the Deccan Plateau. Dating back to the Satavahana period (1st century BCE \u2013 2nd century CE), it was used for the transportation of goods like spices, textiles, and precious stones. The name \"Naneghat\" means \"coin pass,\" referring to the toll collection system where traders had to pay a fee. The site is also known for its Brahmi inscriptions, including references to the Satavahana rulers. Source: Sircar, D.C. Inscriptions of the Satavahanas and Western Kshatrapas (1979).   ",
    // 191
    "Mula and Mutha River": " Mula And Mutha River Mula and Mutha River - The Mula and Mutha rivers are integral to Pune's identity, shaping its history, culture, and daily life. These rivers, originating from the Sahyadri mountains, are believed to be as ancient as the mountains themselves, dating back approximately 60 million years. Their confluence within the city forms the Mula-Mutha River, which has historically sustained local communities, providing water for agriculture, drinking, and other daily needs.   ",
    // 192
    "Bengali Sant Chaitanya": " Bengali Sant Chaitanya Bengali Sant Chaitanya- Chaitanya Mahaprabhu (1486-1534), a 16th-century Bengali saint and founder of Gaudiya Vaishnavism, is believed to have visited Pune during his travels across India. While in Pune, an incident occurred where a mischievous individual pointed to a lake, teasing that Krishna resided there. Without hesitation, Chaitanya Mahaprabhu leapt into the lake, demonstrating his profound devotion. After being rescued, he forgave the prankster, emphasizing that Krishna is omnipresent. Source: Locals   ",
    // 193
    "Kasba": " Kasba Kasba- Kasba Peth, established in the 5th century, is considered to be Pune's oldest locality and is often referred to as the \"Heart of Pune City.\" This area holds significant historical and cultural importance, being the cradle from which Pune expanded. A notable landmark in Kasba Peth is the Kasba Ganapati mandir, considered the Gram Devta of Pune. The original mandir was built by Jijabai, mother of Chhatrapati Shivaji Maharaj, underscoring its deep-rooted connection to Maratha history. \u200bAdditionally, the Lal Mahal, the fortified residence of Shivaji Maharaj, was situated in Kasba Peth. Today, a replica of this historic structure stands adjacent to Shaniwar Wada, serving as a testament to the area's rich past. The narrow lanes of Kasba Peth are lined with traditional wadas (residential complexes), reflecting the architectural heritage of Pune. The locality is also known for its specialized artisan communities, such as the Kumbhar Wada (potters' colony) and Tambat Ali (copper utensil makers' lane), preserving age-old crafts that continue to thrive amidst urbanization.   ",
    // 194
    "Information about Peths": " Information About Peths Information about the Peths Somvar to Ravivar Somwar Peth \u2013 Established in 1625, this area was historically home to Brahmins and government officials. It houses the famous Trishund Ganapati Mandir and several old wadas. It is referred to as Somwar Peth because the market is held every Monday. Mangalwar Peth \u2013 Founded by the Peshwas, it served as a military settlement and is now known for its bustling commercial activities and historic temples like Kalasiddhi Vinayak Mandir. Budhwar Peth \u2013 One of Pune\u2019s busiest markets, it is famous for books, electronics, and historical sites like Shreemant Dagdusheth Halwai Ganapati Mandir. Guruwar Peth \u2013 Once a hub for grain traders, this area has many old wadas and temples, including Dattatray Mandir, reflecting Pune\u2019s historic trade connections. Shukrawar Peth \u2013 Known for the Shukrawar Wada, it was a key commercial and residential centre during the Peshwa era, retaining its traditional markets even today. Shaniwar Peth \u2013 Home to the iconic Shaniwar Wada, this area was historically a power centre of the Peshwas and remains one of Pune\u2019s oldest localities. Ravivar Peth \u2013 Established as a trading hub, it is still a prominent wholesale market for metals, especially brass and copper utensils, and traditional artifacts. Source: Locals   ",
    // 195
    "Inamgaon": " Inamgaon Inamgaon: \u200bThe name \"Inamgaon\" likely originates from the term \"inam,\" meaning \"gift\" or \"land grant,\" indicating the village's establishment through such a grant. However, specific historical records detailing the exact origin of the village's name are scarce. Inamgaon is renowned as a significant post-Harappan archaeological site in Maharashtra, offering insights into ancient agrarian societies. Source: Wikipedia   ",
    // 196
    "Sant Namdev": " Sant Namdev Sant Nmdev - \u200bSant Namdev, born in 1270 CE in Narsi, Maharashtra, was a seminal figure in the Bhakti movement. Hailing from a tailor's family, he transcended societal norms through his profound devotion to Lord Vithoba of Pandharpur. Namdev composed numerous abhangas (devotional hymns) in Marathi, emphasizing a personal connection with the divine, making spirituality accessible to the masses. \u200bIn Pune, Namdev's legacy is intertwined with the city's rich spiritual tapestry. His compositions are integral to the kirtan traditions practised in local temples, fostering communal harmony and devotion. A popular local legend narrates that during a kirtan, Lord Vithoba himself appeared to dance alongside Namdev, illustrating the depth of his devotion and the reciprocal love of the deity. \u200b   ",
    // 197
    "Sant Tukaram": " Sant Tukaram Sant Tukaram - \u200bSant Tukaram Maharaj, born around 1608 in Dehu village near Pune, was a prominent 17th-century Marathi poet-sant of the Bhakti movement. Belonging to the Varkari tradition, he is renowned for his devotional compositions known as abhangas, which emphasize a personal devotion to Lord Vithoba (Vitthal) of Pandharpur. These verses, written in Marathi, made spiritual teachings accessible to the common people and continue to inspire devotees. \u200bIn Pune, Tukaram's legacy is deeply cherished. His birthplace, Dehu, is a significant pilgrimage site, housing the Sant Tukaram Shila Mandir\u2014a temple built around the rock (shila) where he is believed to have meditated and composed his abhangas. This site holds immense importance for the Varkari sect, serving as the starting point for the annual Wari pilgrimage to Pandharpur. \u200bA popular local legend narrates that Tukaram, challenged about the authenticity of his abhangas, immersed his writings into the Indrayani River. Miraculously, after 13 days, the manuscripts resurfaced intact, reaffirming their divine inspiration. This event is commemorated by devotees and underscores the enduring significance of his teachings in the region. \u200bReflecting his enduring influence, the Maharashtra government renamed Pune Airport as 'Jagadguru Sant Tukaram Maharaj International Airport', honouring his contributions to spirituality and Marathi literature. \u200b   ",
    // 198
    "Tyambakeshwar": " Tyambakeshwar Tryambakeshwar- Trimbakeshwar, located in Nashik district, Maharashtra, is a sacred Hindu pilgrimage site known for the Trimbakeshwar Jyotirlinga, one of the twelve Jyotirlingas of Lord Shiva. It is the origin of the Godavari River and is associated with various legends from the Puranas. The temple, built in black stone, holds religious and historical significance. (see Nashik for more)   ",
    // 199
    "Nana Phadanvis": " Nana Phadanvis  Nana Phadanvis - Nana Phadnavis (1742\u20131800) was a key statesman and administrator of the Maratha Empire during the Peshwa rule. As a minister in the Ashtapradhan council under Peshwa Madhavrao I and later Sawai Madhavrao, he played a crucial role in preserving Maratha sovereignty against internal conflicts and external threats, including the British and the Nizam. His diplomatic skills helped maintain a power balance in India. He was instrumental in managing the state's finances and administration, ensuring stability during turbulent times. His strategic alliances and political acumen delayed British dominance in western India, making him a significant figure in Maratha history.   ",
    // 200
    "Battle of Bacaim": " Battle Of Bacaim Battle of Bacaim (1739) - The Battle of Bassein (Bacaim) in 1739 was a significant conflict between the Marathas and the Portuguese. Led by Chimaji Appa, the Marathas launched a well-planned campaign to capture the strategically important fort of Bassein (Vasai), north of Mumbai. The Portuguese, despite their strong fortifications and European military tactics, were overwhelmed by the persistent Maratha siege. After months of intense fighting, the Portuguese surrendered on May 16, 1739. This victory marked the decline of Portuguese influence in western India and strengthened Maratha's control over the Konkan coast, enhancing their naval and commercial dominance in the region.   ",
    // 201
    "Pandharpur": " Pandharpur Pandharpur, located in Maharashtra\u2019s Solapur district, is a major pilgrimage center dedicated to Lord Vitthal, a form of Lord Krishna. It is considered the spiritual heart of the Varkari tradition, attracting millions of devotees, especially during the Ashadhi and Kartiki Ekadashi yatras. Pilgrims, known as Varkaris, undertake a sacred journey on foot from various parts of Maharashtra, chanting devotional songs (abhangas) of saints like Sant Tukaram and Sant Dnyaneshwar. The town\u2019s Chandrabhaga River holds religious significance, where devotees take a holy dip before visiting the Vitthal-Rukmini Temple. Pandharpur remains a symbol of Maharashtra\u2019s deep-rooted Bhakti movement. (refer to Solapur for more).   ",
    // 202
    "King Vedisiri": " King Vedisiri King Vedisiri: \u200bKing Vedisiri, associated with the Satavahana dynasty, is primarily known through inscriptions found in the Naneghat caves near Pune, Maharashtra. These inscriptions, attributed to Queen Naganika, detail various Vedic sacrifices performed and mention her husband, King Satakarni, and their son, Vedisiri. The inscriptions highlight the dynasty's patronage of Vedic rituals and their significant role in ancient Indian polity. \u200b   ",
    // 203
    "Kshatrapas Western": " Kshatrapas Western Kshatrapas Western: The Western Kshatrapas (1st\u20134th century CE) were Indo-Scythian rulers who controlled western India, including Gujarat, Maharashtra, and Malwa. They played a crucial role in trade, especially with the Roman Empire, and promoted Sanskrit inscriptions and Buddhist patronage. Their conflicts with the Satavahanas shaped the region\u2019s political and cultural landscape.   ",
    // 204
    "Bhuleshwar Mandir": " Bhuleshwar Mandir Bhuleshwar Mandir: Bhuleshwar Mandir, located near Pune in Maharashtra, is an ancient temple dedicated to Lord Shiva. Built in the 13th century during the Yadava dynasty, the temple is known for its unique architecture, resembling a fortress. Legends suggest that Goddess Parvati performed penance here before marrying Lord Shiva. The temple features intricate carvings, depicting Hindu mythology, and is a significant pilgrimage site, especially during Mahashivratri. A unique aspect of Bhuleshwar is the belief that the Shiva Linga mysteriously receives spontaneously offered sweets (prasadam). The temple\u2019s serene hilltop location offers a spiritual retreat and stunning views of the surrounding landscape.   ",
    // 205
    "Devgiri Yadavas": " Devgiri Yadavas Devgiri Yadavas: The Yadavas of Devgiri (850\u20131317 CE) were a powerful dynasty that ruled over the Deccan region, with Devgiri (modern Daulatabad) as their capital. They played a key role in shaping medieval Maharashtra, promoting Marathi language and literature, and patronizing saints like Dnyaneshwar. The dynasty reached its peak under King Singhana (c. 1200\u20131247 CE). However, Alauddin Khilji\u2019s invasion in 1296 weakened them, and in 1317, the Delhi Sultanate ended their rule. Their contributions laid the foundation for the later Maratha identity.   ",
    // 206
    "Shivneri Fort": " Shivneri Fort Shivneri Fort: Shivneri Fort, located near Junnar in Maharashtra, is historically significant as the birthplace of Chhatrapati Shivaji Maharaj in 1630. Built during the Satavahana period and later fortified by the Yadavas and Bahamanis, it played a crucial role in medieval military defence. The fort has strong gates, rock-cut water tanks, and temples, including one dedicated to Goddess Shivai, after whom Shivaji was named. The strategic location of Shivneri made it an important watchtower, controlling trade routes. Today, it stands as a revered site, attracting historians and devotees who honour its legacy in Maratha history.   ",
    // 207
    "Dadoji Kondadev": " Dadoji Kondadev Dadoji Kondadev: Dadoji Kondadev was a 17th-century administrator and military leader in the service of the Bhosale family of Pune under the Adil Shahi Sultanate. He is credited with developing Pune by constructing temples, water reservoirs, and markets. According to some accounts, he played a role in mentoring young Chhatrapati Shivaji Maharaj, though this claim remains debated. He efficiently managed Pune\u2019s administration and fortifications, laying the foundation for its later prominence under the Marathas. His legacy remains a subject of historical discussion.   ",
    // 208
    "Guerrilla Warfare": " Guerrilla Warfare Guerrilla Warfare: \u200bGuerrilla warfare, characterized by swift, unconventional tactics, was notably advanced by Chhatrapati Shivaji Maharaj in 17th-century Maharashtra, particularly around Pune. Facing larger Mughal and Adil Shahi forces, Shivaji innovated Ganimi Kava, emphasizing surprise attacks, rapid mobility, and intimate knowledge of the rugged Western Ghats terrain. This approach allowed his smaller forces to outmaneuver and destabilize more substantial armies effectively. \u200bSwift Cavalry Raids: Utilizing fast-moving horsemen to launch unexpected assaults.\u200b Hit-and-Run Tactics: Engaging enemies briefly before retreating to avoid counterattacks.\u200b Terrain Advantage: Exploiting the region's hills and forests for concealment and strategic positioning.\u200b Intelligence Gathering: Employing spies to monitor enemy movements and plan precise strikes. Sources: Wikipedia and locals   ",
    // 209
    "Tanaji": " Tanaji Tanaji: Tanaji Malusare was a trusted commander of Chhatrapati Shivaji Maharaj, known for his bravery and sacrifice during the Battle of Sinhagad in 1670. Tasked with recapturing the fort from the Mughal commander Udaybhan Rathod, Tanaji led a daring night assault using rope-climbing techniques. Despite fierce resistance, he fought valiantly but was mortally wounded. His death deeply affected Shivaji, who famously said, \"Gad ala pan Sinh gela\" (The fort is won, but the lion is lost). In honour of his sacrifice, the fort was renamed Sinhagad (Lion\u2019s Fort). His legacy remains a symbol of courage and patriotism.   ",
    // 210
    "Treaty of Purandar": " Treaty Of Purandar Treaty of Purandar: The Treaty of Purandar was signed on 11 June 1665 between Chhatrapati Shivaji Maharaj and Mirza Raja Jai Singh I, a general of the Mughal Emperor Aurangzeb. After a fierce Mughal campaign, Shivaji agreed to surrender 23 forts while retaining control over 12 forts. He also agreed to assist the Mughals in their Deccan campaigns. As part of the treaty, Shivaji\u2019s son Sambhaji was sent to the Mughal court as a mansabdar. Though the treaty was a temporary setback, Shivaji later reasserted his strength, recapturing lost territory and continuing his fight against Mughal rule.   ",
    // 211
    "Sahyadri": " Sahyadri Sahyadri: The Sahyadri Hills, also known as the Western Ghats, hold immense historical, ecological, and cultural significance. Stretching along the western coast of India, they are home to ancient forts, including Raigad, Pratapgad, and Sinhagad, which played a crucial role in Maratha history. The region is also sacred, housing temples like Bhimashankar and Mahabaleshwar.   ",
    // 212
    "Sardeshimukhi rights": " Sardeshimukhi Rights Sardeshimukhi right: Sardeshmukhi was an additional tax levied by the Marathas, amounting to 10% of revenue collected from territories under their influence. It was imposed alongside Chauth, a 25% tax on revenue from non-Maratha territories. Sardeshmukhi was claimed by the Chhatrapati of the Maratha Empire as a hereditary right, symbolizing his supreme authority over the region. This tax helped finance Maratha military campaigns and administration. Introduced under Chhatrapati Shivaji Maharaj, it became a crucial financial instrument for later rulers like Shahu Maharaj and the Peshwas, ensuring sustained expansion and governance of the empire.   ",
    // 213
    "Ryotwari Settlement": " Ryotwari Settlement Ryotwari Settlement: The Ryotwari Settlement was a land revenue system introduced by the British East India Company, primarily in Madras, Bombay, and parts of Bengal Presidencies. Developed by Thomas Munro in the early 19th century, it directly taxed individual farmers (ryots) instead of intermediaries like zamindars. Under this system, the British government collected revenue directly from cultivators, based on land fertility and produce. Though intended to ensure fair taxation, it often led to high revenue demands, forcing farmers into debt. In Maharashtra, the Ryotwari system significantly impacted rural agrarian life, shaping land ownership patterns and economic hardships during British rule.   ",
    // 214
    "Quit India Movement 1942": " Quit India Movement 1942 Quit India movement: 1942: The Quit India Movement was launched by Mahatma Gandhi on 8 August 1942, demanding an end to British rule in India. It was a mass civil disobedience movement, following the failure of the Cripps Mission. Gandhi\u2019s slogan, \u201cDo or Die,\u201d inspired nationwide protests, strikes, and sabotage of British infrastructure. The British arrested key leaders, including Gandhi, crippling the movement. Despite severe repression, it ignited widespread resistance, uniting Indians against colonial rule. Though it was eventually suppressed, the movement strengthened the call for independence, leading to India\u2019s freedom in 1947. Pune and Maharashtra played a significant role in the uprising.   ",
    // 215
    "Jijau": " Jijau Jijau- Jijabai, fondly known as Jijau, was the mother of Chhatrapati Shivaji Maharaj and a key architect of the Maratha Empire. Born in 1598 in Sindkhed Raja (Buldhana district), she was the daughter of Lakhuji Jadhav, a respected noble. She instilled values of Swarajya, justice, and resilience in Shivaji, shaping his leadership. Jijau managed the administration of Pune and Shahaji\u2019s jagirs, overseeing fort development and governance. She played a crucial role in planning Maratha expansion and inspired the foundation of Hindavi Swarajya. Her teachings on ethics, warfare, and governance significantly influenced Maratha rule, making her a revered historical figure. (refer to Buldhana)   ",
    // 216
    "Tarabai": " Tarabai Tarabai: Tarabai was a fierce Maratha queen and regent who led the empire after the death of her husband, Chhatrapati Rajaram Maharaj, in 1700. A skilled strategist, she fought against the Mughals, defending Maratha sovereignty during the War of Independence (1700\u20131707). As regent for her son, Shivaji II, she administered the empire from Kolhapur and played a crucial role in keeping the Maratha resistance alive. Her leadership laid the foundation for later Maratha expansion, making her one of the most significant women in Maratha history. (refer to Kolhapur).   ",
    // 217
    "Jotirao Phule": " Jotirao Phule Jotirao Phule: Jotirao Phule (1827\u20131890) was a social reformer, thinker, and writer from Maharashtra who fought against caste discrimination and championed women\u2019s education and social equality. Born in Pune in a lower-caste Mali family, Phule was deeply affected by the injustices of the caste system. In 1848, he and his wife, Savitribai Phule, established the first school for girls in Pune, breaking societal norms. Phule strongly opposed Brahminical dominance, untouchability, and oppression of women. He founded the Satyashodhak Samaj (Truth-Seeking Society) in 1873, advocating for equality and self-respect among lower castes. His famous work, \"Gulamgiri\" (Slavery), criticized social hierarchies and British policies that supported caste-based oppression. Phule also promoted widow remarriage, opposed child marriage, and started homes for orphans. His efforts laid the foundation for social justice movements in Maharashtra. Recognized as Mahatma for his selfless work, Phule remains a pioneer of anti-caste and educational reforms in India.   ",
    // 218
    "Malwa Culture": " Malwa Culture Malwa Culture- Malwa culture is a combination of Rajput, Maratha, and tribal influences, reflecting its rich historical legacy. The region, located in present-day Madhya Pradesh, has been a cultural hub since ancient times, influenced by rulers like the Paramaras, Mughals, and Marathas. Malwa is renowned for its folk music, dance forms like Matki and Nirguni Bhajans, and traditional handicrafts. It has a deep connection with literature, being home to poets like Kalidasa. The cuisine, including Dal Bafla, is unique to the region. The famous Ganesh Chaturthi and Navratri celebrations highlight its vibrant traditions and religious significance  ",
    // 219
    "Jorwe Culture": " Jorwe Culture Jorwe Culture - The Jorwe culture (1400\u2013700 BCE) was a Chalcolithic (Copper Age) culture that thrived in present-day Maharashtra, particularly along the Godavari River. Named after the site of Jorwe in Ahmednagar district, it was characterized by well-planned settlements, mud houses, and advanced pottery, especially red and black wares. The people practised agriculture, cultivating barley and millet, and engaged in cattle rearing. They had trade links with other contemporary cultures and showed evidence of social hierarchy. Declining around 700 BCE, Jorwe culture represents an important transition from early agrarian societies to more complex social structures in western India.   ",
    // 220
    "Salvadas": " Salvadas Salvadas - \u200bGhashiram Savaldas was a historical figure who migrated to Pune, during the late 18th century. Originally from North India, he sought fortune in Pune, then under Peshwa rule. His life inspired Vijay Tendulkar's 1972 Marathi play \"Ghashiram Kotwal,\" which critiques the socio-political dynamics of that era. \u200b Source: Locals   ",
    // 221
    "Salvada Culture": " Salvada Culture Salvada Culture - The Savalda culture (circa 2000\u20131800 BCE) was a Chalcolithic culture primarily centred in the Tapi Valley of Maharashtra, with notable sites like Daimabad and Kaothe. At Daimabad, excavations revealed mud-walled houses with rounded ends, hearths, and storage pits, indicating a settled lifestyle. The Savalda culture represents a significant phase in the Pune prehistoric period, showcasing early advancements in agriculture, craftsmanship, and settlement organization.\u200b   ",
    // 222
    "Basalt Rock": " Basalt Rock Basalt Rock: Basalt rock is known for its dark, fine-grained texture and durability, which has made it a preferred material for constructing historical forts like Sinhagad, Purandar, and Shaniwar Wada. The rock also plays a crucial role in the region\u2019s water retention capacity, supporting agriculture and groundwater reserves. The hilly terrain of Pune, including the Sahyadri ranges, is largely shaped by basalt formations. Pune is primarily located on the Deccan Traps, a vast volcanic plateau composed of basalt rock, formed due to massive volcanic eruptions around 66 million years ago during the late Cretaceous period.   ",
    // 223
    "Deccan Traps": " Deccan Traps Deccan Traps- The Deccan Traps are one of the world\u2019s largest volcanic formations, covering parts of Maharashtra, Madhya Pradesh, Gujarat, and Karnataka. Formed around 66 million years ago due to massive volcanic eruptions, these basalt rock layers extend over 500,000 square kilometers. The eruptions are believed to have contributed to the mass extinction of dinosaurs. The Western Ghats and Pune\u2019s terrain are shaped by these lava flows, impacting soil fertility and groundwater storage, making them significant for agriculture and human settlement. Source: Geological Survey of India   ",
    // 224
    "Nandi Mandapa": " Nandi Mandapa Nandi Mandapa - \u200bThe Pataleshwar Cave mandir in Pune, dating back to the 8th century, features a distinctive circular Nandi Mandapa (pavilion) carved from basalt rock. This monolithic structure, supported by 16 pillars, houses a Nandi idol facing the main sanctum dedicated to Lord Shiva. The temple's architecture reflects the Rashtrakuta dynasty's rock-cut style, mirroring the grandeur of the Ellora caves. \u200b   ",
    // 225
    "Saptamatrikas": " Saptamatrikas Saptamatrikas \u2013 \u200bThe Saptamatrikas, or \"seven mother goddesses,\" are significant in Hindu tradition, representing feminine divinity and power. In Pune, the Pataleshwar Cave mandir, an 8th-century rock-cut shrine, features reliefs of the Saptamatrikas, showcasing their importance in the region's religious art. These carvings highlight the cultural and spiritual reverence for these deities during the Rashtrakuta dynasty. \u200b Source: Wikipedia   ",
    // 226
    "Gajalakshmi": " Gajalakshmi Gajalakshmi\u2013 Gajalakshmi is a revered form of Devi Lakshmi, depicted with two elephants (Gaja) showering her with water, symbolizing prosperity, abundance, and fertility. This iconography is commonly found in mandir and ancient carvings across Maharashtra, including Pune, signifying blessings of wealth and well-being in Hindu tradition. Sources: Stories and locals   ",
    // 227
    "Tripurantaka": " Tripurantaka Tripurantaka- Tripurantaka is a fierce form of Bhagwan Shiva, depicted as the destroyer of the three demon cities, Tripura. According to Hindu stories, Shiva, armed with a single arrow, annihilated the three asuras\u2014Taraka, Vidyunmali, and Kamalaksha\u2014who had created impregnable floating cities. This event symbolizes the triumph of divine power over evil. In Pune, Shiva pooja is prominent, with mandirs such as Pataleshwar reflecting his various forms, including Tripurantaka, reinforcing his role as the cosmic protector and destroyer of ignorance. Source: locals   ",
    // 228
    "Anantasayin": " Anantasayin Anantasayin refers to Bhagwan Vishnu in his reclining form on the serpent Ananta (Shesha), symbolizing cosmic balance and eternal existence. This depiction is found in various Vishnu mandir across India, including Maharashtra. In Pune, Vishnu's traditional knowledge is evident in the historical mandir where he is worshipped in different forms. The Anantasayin iconography signifies the cycle of creation, preservation, and dissolution. This divine imagery reinforces Vishnu\u2019s role as the protector of the universe, ensuring stability and righteousness (Dharma) in the cosmic order. Source: Locals   ",
    // 229
    "Lingodbhava": " Lingodbhava Lingodbhava is a significant depiction of Bhagwan Shiva emerging from an infinite pillar of light (Shiva Linga), symbolizing his limitless and formless nature. This form is associated with the legend where Vishnu and Brahma sought the origin and end of Shiva\u2019s cosmic pillar, ultimately realizing his supremacy. In Pune, Shiva mandir, including Pataleshwar, emphasize his worship through the Lingodbhava form, highlighting the eternal presence of Shiva. This representation underscores his role as the creator, preserver, and destroyer in Hindu tradition.   ",
    // 230
    "Fergusson": " Fergusson  Sir James Fergusson was a British administrator who served as the Governor of Bombay from 1880 to 1885. He played a significant role in the development of education and infrastructure in Pune. Fergusson College, one of India\u2019s premier institutions, was established in 1885 by the Deccan Education Society and named in his honor due to his support for higher education. His tenure also saw improvements in municipal governance and public services in Pune. Fergusson\u2019s legacy remains prominent in the city's educational landscape, reflecting his influence on Maharashtra\u2019s intellectual and social progress.   ",
    // 231
    "Burges": " Burges  Sir James Burges was a British administrator and architect who contributed to the colonial-era development of the Bombay Presidency, including Pune. He played a role in designing several government buildings and infrastructure projects. His work reflected the Indo-Saracenic architectural style, blending British and Indian influences to create enduring landmarks.   ",
    // 232
    "Nagara Style": " Nagara Style \u200bThe Nagara style is a prominent form of Hindu mandir architecture that originated in northern India. It is characterized by its beehive-shaped tower, known as a shikhara, rising above the sanctum sanctorum (garbhagriha). This architectural style is prevalent in various regions, including Maharashtra. In Pune, the Parvati mandir exemplifies the Nagara architectural style. Perched atop Parvati Hill, this temple complex offers panoramic views of the city and holds significant historical and spiritual importance. The mandir\u2019s design features the characteristic shikhara, reflecting the vertical emphasis typical of Nagara architecture. The Parvati mandir serves as a vital cultural and religious landmark in Pune, attracting devotees and tourists alike.\u200b   ",
    // 233
    "Malik-ul-Jujar": " Malik-Ul-Jujar In 1443, Malik-ul-Tujar led forces that defeated the Yadavas and captured Shivneri Fort, bringing it under the Bahamani Sultanate's control. This strategic fortification, located near Pune, later became notable as the birthplace of Chhatrapati Shivaji Maharaj, the founder of the Maratha Empire. The fort's capture marked a significant shift in regional power dynamics, influencing the area's historical trajectory.\u200b   ",
    // 234
    "Chakan": " Chakan  Chakan, located near Pune, is historically significant for its strategic fort, which played a key role during the Mughal-Maratha conflicts. In 1660, Firangoji Narsala defended Chakan Fort against Shaista Khan\u2019s Mughal forces for almost two months. Today, Chakan is an industrial hub with major automobile and manufacturing industries.  ",
    // 235
    "Raja Todar Mal Revenue System": " Raja Todar Mal Revenue System \u200bRaja Todar Mal, Akbar's finance minister and one of his nine Navratnas, introduced the Dahsala system (also known as Zabt) in 1580 to streamline the Mughal Empire's land revenue collection. This system involved a meticulous survey of crop yields, prices, and cultivated areas over a ten-year period (1570-1580). Based on this data, the average produce of different crops was assessed, and one-third of this average was designated as the state's share, payable in cash. This approach provided a standardized and equitable revenue assessment, benefiting both the state and cultivators. The Dahsala system was implemented in regions where detailed surveys were feasible, ensuring a fair and consistent tax structure. \u200b   ",
    // 236
    "Scinda": " Scinda Scinda \u2014 The Scindia (Shinde) dynasty was a prominent Maratha lineage that played a crucial role in 18th and 19th-century Indian history. Originating from Kanherkhed in Maharashtra, the dynasty rose under Ranoji Scindia, a commander of Peshwa Bajirao I. Mahadji Scindia later became a key power broker in North India, rebuilding Maratha influence after the Third Battle of Panipat (1761). The Scindias ruled Gwalior and held strategic control over several regions, including parts of Maharashtra, until British intervention. Their legacy remains influential in Indian history. Source: Sarkar, Jadunath. Fall of the Mughal Empire, Vol. III, Orient Blackswan, 1979.   ",
    // 237
    "Holkars": " Holkars Holkars \u2013 The Holkars were a prominent Maratha dynasty that ruled Indore and played a key role in the 18th-century expansion of the Maratha Empire. Founded by Malhar Rao Holkar, they were known for their military prowess and governance. Ahilyabai Holkar is especially revered for her administrative skills and temple restorations across India. Source: G.S. Sardesai, New History of the Marathas, Vol. III, Phoenix Publications, 1958.   ",
    // 238
    "General Wellesly": " General Wellesly General Wellesly \u2014 General Arthur Wellesley, later the Duke of Wellington, played a crucial role in the Second Anglo-Maratha War (1803-1805). He led British forces against the Marathas, securing victories in battles like Assaye and Argaon, which weakened Maratha power in India and expanded British control. Source: M.S. Naravane, Battles of the Honourable East India Company, A.P.H. Publishing, 2006.   ",
    // 239
    "Krishna River": " Krishna River Krishna River \u2013 The Krishna River is one of the most significant rivers in Maharashtra, deeply intertwined with local folklore and spiritual beliefs. According to a popular legend, the river is believed to be an incarnation of Krishna Bai, a devotee of Bhagwan Vishnu who took the form of a river to serve the land. Another tale connects the river to the Sahyadri Hills, where it is said that Devi Mahalakshmi blessed the river to bring prosperity. The Krishna River nourishes Pune and surrounding regions, supporting agriculture and cultural traditions. Source: Maharashtra State Gazetteers, Government of Maharashtra.(Pune)  ",
    // 240
    "Bor Pass": " Bor Pass Bor Pass \u2014 Bor Pass, located in the Sahyadri mountain range near Pune, played a significant role in historical trade and military movements. It served as a crucial route connecting the Deccan Plateau with the coastal Konkan region, facilitating commerce and strategic troop movements during the Maratha and British periods. The pass was historically used for transporting goods and communication between Pune and the western coast. Its rugged terrain and elevation made it a natural defensive point in battles. Source: Maharashtra State Gazetteers, Government of Maharashtra. (Pune)  ",
    // 241
    "Panvel": " Panvel Panvel \u2013 Panvel, located in Raigad district near Mumbai, is an important historical and commercial hub. Known as the gateway to the Konkan, it was a key trade route during the Maratha and British eras. Its proximity to major forts like Karnala made it strategically significant. Today, it is a rapidly developing city. Source: Maharashtra State Gazetteers, Government of Maharashtra. (Pune)   ",
    // 242
    "Maysore": " Maysore Mysore played a significant role in Pune\u2019s history during the Anglo-Maratha conflicts. The rivalry between the Marathas and Tipu Sultan of Mysore influenced strategic decisions in Pune, the seat of the Peshwas. The Marathas played a key role in Tipu Sultan\u2019s defeat alongside the British in 1799. Source: Duff, James Grant. A History of the Mahrattas, 1826.   ",
    // 243
    "Peshwa Bajirao II": " Peshwa Bajirao Ii Peshwa Baji Rao II \u2014 Peshwa Baji Rao II was the last Peshwa of the Maratha Empire, ruling from 1796 to 1818. His reign saw the decline of Maratha power, culminating in the Third Anglo-Maratha War (1817\u20131818). Defeated by the British, he surrendered and was exiled to Bithoor. Source: Gordon, Stewart. The Marathas 1600-1818, Cambridge University Press, 1993.   ",
    // 244
    "Kolaba": " Kolaba Kolaba \u2014 Kolaba, now known as Alibaug, is a coastal region in Maharashtra with historical and strategic significance. The Kolaba Fort, built by Chhatrapati Shivaji Maharaj in the 17th century, served as a key naval base for the Marathas. The region played a crucial role in Maratha defense strategies against foreign invasions. Today, Kolaba is a popular tourist destination known for its beaches, forts, and cultural heritage. Source: Gazetter of the Bombay Presidency: Kolaba and Janjira, Government Central Press, 1883.  ",
    // 245
    "Sindhia of Gwalior": " Sindhia Of Gwalior Sindhia of Gwalior \u2013 The Sindhia (Scindia) dynasty of Gwalior was a prominent Maratha power in northern India. Established by Ranoji Scindia in the 18th century, they played a crucial role in the Maratha Empire. Mahadji Scindia strengthened the dynasty, while Daulat Rao Scindia faced British conflicts, leading to eventual submission under British rule. Source: Sarkar, Jadunath. Fall of the Mughal Empire, Orient Blackswan, 1992.   ",
    // 246
    "Gaikwad of Baroda": " Gaikwad Of Baroda Gaikwad of Baroda \u2013 The Gaikwads of Baroda were a prominent Maratha dynasty that ruled Gujarat. Established by Pilaji Gaikwad in the early 18th century, they became powerful under British suzerainty. Sayajirao Gaikwad III was a notable ruler known for social reforms and modernization of Baroda. Source: Gillion, Kenneth. The Western Indian States Agency, Cambridge University Press, 1968.   ",
    // 247
    "Samyukta Maratha Movement": " Samyukta Maratha Movement Samyukta Maratha Movement \u2014 The Samyukta Maharashtra Movement was a political campaign in the 1950s advocating for a separate Marathi-speaking state. Led by figures like S.M. Joshi, Prabodhankar Thackeray, and Senapati Bapat, the movement sought the inclusion of Mumbai in Maharashtra. After protests and sacrifices, including the deaths of 105 protestors on November 21, 1955, the movement succeeded, and Maharashtra was formed on May 1, 1960, with Mumbai as its capital. Source: Masselos, Jim. Bombay in Transition: The Growth and Social Setting of a Colonial City, 1880-1980, Oxford University Press, 1995.   ",
    // 248
    "Salt Satyagraha": " Salt Satyagraha Salt Satyagraha \u2013 The Salt Satyagraha, led by Mahatma Gandhi in 1930, was a nonviolent protest against the British salt tax. Beginning with the Dandi March, it inspired nationwide civil disobedience, including in Pune, where activists like Senapati Bapat played key roles. It marked a turning point in India\u2019s independence movement. Source: Brown, Judith M. Gandhi: Prisoner of Hope, Yale University Press, 1989.  ",
    // 249
    "Gandhi": " Gandhi Gandhi \u2013 Mahatma Gandhi had a deep connection with Pune, where he was imprisoned multiple times, including at Yerwada Jail. The historic Poona Pact of 1932, negotiated with Dr. B.R. Ambedkar, was signed here. Pune also witnessed his influence in social reform movements, promoting nonviolence and self-reliance. Source: Fischer, Louis. The Life of Mahatma Gandhi, Harper & Row, 1950.   ",
    // 250
    "Yesubai": " Yesubai Yesubai, the wife of Chhatrapati Sambhaji Maharaj, played a crucial role in Maratha history. After Sambhaji\u2019s execution by Aurangzeb in 1689, she was imprisoned along with her son, Shahu Maharaj, in Delhi for nearly 17 years. She displayed remarkable political acumen despite captivity, ensuring Shahu\u2019s survival and preparing him for leadership. Upon his release in 1707, Yesubai supported Shahu in his succession struggle against Tarabai, ultimately securing his throne and paving the way for Peshwa's rule. Her resilience and diplomacy were instrumental in preserving the Maratha legacy, making her a significant figure in the empire\u2019s history. (refer Ratnagiri for more)  ",
    // 251
    "Gudi Padwa": " Gudi Padwa Gudi Padwa is a significant spring festival that marks the New Year for Hindus. Celebrated on the first day of Chaitra (March-April), it is widely observed in Maharashtra and the Konkan region. The term Padwa originates from the Sanskrit word Pratipada, denoting the first day of a lunar fortnight. People believe that Gudi Padwa symbolizes the day when Bhagwan Brahma initiated the creation of the world after a great deluge that had destroyed all existence. It is said that time itself had come to a standstill, and every aspect of nature was annihilated. With Bhagwan Brahma's intervention, time resumed, heralding a new era of truth and justice\u2014Satyug. It is also believed to be the day when Bhagwan Ram returned to Ayodhya after defeating Ravan, completing 14 years of exile. On Gudi Padwa, the day begins with house cleaning, followed by rangoli designs around entrances. People consume a mixture of neem leaves and jaggery, which symbolizes the acceptance of both bitter and sweet experiences of life. Families prepare festive delicacies such as puran poli, shrikhand, and poori-bhaji. The day is considered auspicious for commencing new business ventures, making investments, purchasing new vehicles, and performing Vastu pooja. A defining feature of Gudi Padwa is the hoisting of the Gudi, a decorated flag positioned on the right side of homes. The Gudi is crafted using a bamboo stick adorned with mango and neem leaves, sugar crystals, a garland of flowers, and an inverted silver or copper vessel. Each element of the Gudi holds meaning. The yellow silk cloth represents Sato Guna (the seven noble attributes), eliminating negativity and impurities. Green and saffron colors signify life, vitality, and pure fire. Mango leaves reflect immortality and the perpetual cycle of life. Red flowers symbolize passion and triumph over negativity. Sugar crystals represent the sweetness of life and the rewards of perseverance.  ",
    // 252
    "Ram Navami": " Ram Navami Ram Navami, celebrates the birth of Bhagwan Ram, who is regarded as the seventh avatar of Vishnu. The festival occurs on the ninth day (Navami) of the Chaitra (March or April) month. The observance of Ram Navami includes ritualistic vrat, with many people beginning their vrats before sunrise and continuing until the next morning. One of the stories behind Ram Navami originates in the ancient kingdom of Ayodhya, where King Dasharatha and Queen Kausalya were blessed with the birth of Ram. Despite having three wives\u2014Kausalya, Kaikeyi, and Sumitra\u2014Dasharatha remained childless for many years. In his longing for an heir, he performed a sacrifice under the guidance of the Sadhu Rishyasringa. At the culmination of the ritual, a Devta emerged from the sacred fire, presenting an offering\u2014a pot filled with rice and milk. Following the Sadhu\u2019s instructions, the king divided the contents among his wives. As a result, Kausalya gave birth to Ram, Kaikeyi bore Bharat, and Sumitra gave birth to twins, Lakshman and Shatrughna. Thus, Dasharatha\u2019s wish for sons was fulfilled. The day is marked by the recitation of Ram Katha and readings from texts such as the Shrimad Bhagavatam and the Ramayana. In mandirs and households, bhajans and kirtans are performed. The day also includes charitable activities and Bhandaras (community meals), bringing people together in celebration.  ",
    // 253
    "Akshaya Tritiya": " Akshaya Tritiya Akshaya Tritiya, observed on the third lunar day of Vaishakh (April-May), is considered one of the most auspicious days in the Hindu calendar. The festival marks the birth anniversary of Parshuram, the sixth avatar of Vishnu. People feel on this day, Bhagwan Krishna once visited the Pandavas during their exile unannounced. Draupadi, the wife of the Pandavas, was unable to prepare a feast to welcome Bhagwaan Krishna. She fell at his feet and sought forgiveness. Bhagwaan Krishna took a single strand of a herb from the food bowl and forgave her. He then blessed the Pandavas with the Akshaya Patra, a bowl that would never run out of food and offerings. People visit mandirs of Bhagwaan Vishnu, Devi Lakshmi, Bhagwan Ganesh, and Bhagwaan Kuber and buy. Married women pray to Devi Gauri for the longevity and well-being of their husbands. Prasad and sweets are distributed among family and friends as a part of the celebrations.   ",
    // 254
    "Vat Purnima": " Vat Purnima Vat Purnima is a festival observed on the full moon day (Purnima) in the month of Jyeshtha (May-June). It is primarily celebrated by married women, who observe vrats and pray for the long life and well-being of their husbands. The central ritual of Vat Purnima involves tying a thread around a Vat Vriksha (banyan tree) while offering prayers to Savitri. One of the stories associated with the Vat Savitri festival revolves around the love and devotion of Savitri, the daughter of King Ashvapati, and her husband Satyavan, a prince living in exile. The Sadhu Narada foretold that Satyavan would not survive beyond a year after their marriage. Despite this ominous prediction, Savitri chose to marry him. As the foretold day of his death approached, she did everything in her power to protect him. She accompanied Satyavan to the forest, waiting anxiously for the inevitable moment. When Yama, the Devta of death, arrived to claim Satyavan\u2019s Atma, Savitri resolutely confronted him and pleaded for her husband\u2019s life. Yama, moved by her determination, granted her three wishes\u2014except the revival of Satyavan. Using her wisdom, Savitri requested to have children with Satyavan, compelling Yama to restore his life. She used her remaining two wishes to regain her father-in-law\u2019s lost kingdom and sight. Although the tree is not central to the story, it is worshipped as a symbol of the love and devotion depicted in this story.   ",
    // 255
    "Bail Pola": " Bail Pola Pola falls on the new moon day of Shravan (July-August). It is a festival dedicated to bulls, which play a crucial role in agriculture. On the day of Pola, farmers give their bulls a break from fieldwork. The male members of the family take the bulls to the fields, where they are given a special bath using turmeric, oil, and warm water. After the bath, the bulls are decorated with bright-colored paints on their horns, ornaments, and decorative clothing. Flowers, balloons, and ghungroos are also tied around their necks and feet. Once dressed, the bulls are taken through the streets in a grand miravnuk (procession). Farmers walk alongside their bulls, holding their ropes tightly. The miravnuk typically begins at a village mandir, where the bulls are taken around the temple sanctum (Parikrama) as a form of worship. At home, women welcome the bulls by decorating the entrance with colorful rangoli designs. They perform a puja using haldi, kumkum, rice grains, and sweets. The yoke, (a tool used for plowing fields), is also worshipped during the ceremony. The bulls are fed homemade dishes like poori, rice, and sweets as a token of appreciation for their hard work. After the puja, families gather to enjoy a festive meal. Traditional dishes such as Puran Poli are commonly prepared and shared among family members.   ",
    // 256
    "Nag Panchami": " Nag Panchami Nag Panchami is a festival dedicated to the puja of snakes, especially cobras. It is celebrated on the fifth day (Panchami) of Shravan (July-August). On this day, people worship Nag Devta made of silver, stone, or wood, as well as snake paintings. The murtis are bathed with milk and water and decorated with flowers, haldi, and sandalwood paste. Some people also worship real snakes, offering them milk and sweets. Many people observe vrats as part of the ritual. Digging the earth is avoided on this day to prevent harming snakes that may be living underground.   ",
    // 257
    "Gokul Ashtami": " Gokul Ashtami Gokulashtami, also known as Janmashtami, celebrates the birth of Bhagwaan Krishna, the eighth avatar of Vishnu. It is celebrated on the eight day (Ashtami) in the month of Shravan (July-August). It is observed with vrats and prayers. Many people observe a vrat throughout the day and break it at midnight, the time believed to be Bhagwaan Krishna\u2019s birth. A major part of the festival in Maharashtra is Dahi Handi, where groups of young people form human pyramids to break a clay pot filled with buttermilk that is hung at a height. The spilled buttermilk is considered prasad. This event is popular in cities like Mumbai, Pune, and Nashik, where large crowds gather to watch different groups compete.   ",
    // 258
    "Ganesh Chaturthi": " Ganesh Chaturthi Ganesh Chaturthi marks the birth of Bhagwaan Ganesh and begins on the fourth day (Chaturthi) of the Bhadrapada month, which falls between August and September. The festival is observed both in households and in public, with rituals and celebrations spanning several days. In many homes, families bring a Ganpati murti, often with its face covered, which is unveiled during Pran Pratishthapana to invoke the Devta\u2019s presence. The murti is placed on a raised platform and worshipped daily throughout the festival. People offer prasad, including coconut, jaggery, and 21 modaks, a sweet considered to be Ganesha\u2019s favorite. Aarti is performed twice a day, in the morning and evening. The duration of the festival varies among households, lasting 1.5, 5, 7, or 11 days. On the final day, a farewell ritual known as Uttarpooja is conducted before Ganeshji is immersed in a water body, symbolizing Ganesh\u2019s return to Mount Kailash. Ganesh Chaturthi gained prominence as a public festival in the 19th century when freedom fighter Bal Gangadhar Tilak introduced large-scale public celebrations. Since then, public pandals have become a key part of the festival, attracting large gatherings. Some pandals house two murtis\u2014a primary large murti and a smaller one. The festival begins with the installation of the murti, followed by rituals such as Prana Pratishthapana and Shodashopachara (16 forms of offering). Pandals organize various cultural and religious activities, including bhajans, discourses, dance competitions, and programs for children. Aarti is conducted daily, with great fanfare. The festival concludes with Ganpati Visarjan, a grand miravnuk in which the murti is carried to a nearby water body for immersion. People accompany the procession with kirtans and chants. The murti is usually transported on a trolley, followed by a vehicle carrying a generator for lighting and sound systems. Large crowds take part in this miravnuk, marking the culmination of the festival.   ",
    // 259
    "Navratri": " Navratri Navratri is a nine-day Hindu festival dedicated to Devi Durga, observed in the month of Ashvina (September-October). It is marked by various rituals, prayers, and vrat. Navratri commemorates Devi Durga\u2019s nine-day battle against a rakshas. Each day is associated with a specific color, symbolizing different qualities of the Devi. Many people wear traditional attire matching the color of the day. Throughout the festival, different forms of the Devi are honored through pooja. In urban areas, Garba, a traditional Gujarati dance (though performed with slight variations in some Maharashtrian regions), is an integral part of the celebrations. Many people observe vrats during Navratri. Some consume only milk, water, fruits, and nuts during the day, followed by a full meal after sunset. Others limit their intake to water and a simple meal at night.   ",
    // 260
    "Dasara": " Dasara Vijayadashami, also known as Dussehra, is celebrated on the tenth day of Navratri in Maharashtra. It marks the victory of Bhagwan Ram over Ravan and the triumph of Devi Durga over Mahishasura. The festival concludes with the visarjan of murtis for which pooja was performed during Navratri. People gather to celebrate the occasion by exchanging sweets and good wishes. A significant tradition in Maharashtra is the pooja of the Apta tree. Its leaves, known as Sona (gold leaves), are exchanged Vijayadashami holds special importance for artisans and skilled workers in Maharashtra. On this day, they perform puja for their tools and refrain from using them. Many people also extend this tradition by performing puja for items they value, such as cars, books, laptops, musical instruments, or any object they use regularly, whether for work, study, or personal passion. Marigold flowers, especially saffron-colored ones, play a significant role in the celebrations. They are widely used for rituals, home decorations, and adorning workplaces. Markets see a high demand for marigold flowers during this festival. In some places, Bhandaras are organized as part of the celebrations.   ",
    // 261
    "Kojagiri Purnima": " Kojagiri Purnima Kojagiri Purnima, also known as Sharad Purnima, is an important festival in Maharashtra, celebrated on the full moon night of the Ashwin month (September-October). It marks the end of the monsoon season and is considered a harvest festival, honoring Devi Lakshmi. In Maharashtra, people keep vrats during the day and perform puja under the moonlight at night. Homes are decorated with lights and rangoli to welcome Devi Lakshmi. Kojagiri Purnima is also a time for community bonding. People gather under the moonlight to share food, especially masala doodh (spiced milk), which is prepared using contributions from different households.   ",
    // 263
    "Tulsi Vivah": " Tulsi Vivah Tulsi Vivah is observed on Prabodhini Ekadashi, the eleventh day of the Shukla Paksha in the month of Kartik (October\u2013November). In Maharashtra, it marks the beginning of the traditional wedding season, and many families commence marriage ceremonies for their sons and daughters only after this auspicious occasion. One of the stories behind Tulsi Vivah is associated with Vrinda, a devoted follower of Bhagwaan Vishnu, who was married to the rakshas king Jalandhar. Due to her devotion towards Bhagwaan Vishnu, Jalandhar became powerful and invincible, even in battles against the Devtas. To restore balance and prevent his growing dominance, Bhagwaan Vishnu disguised himself as Jalandhar and deceived Vrinda, leading to Jalandhar\u2019s downfall and eventual death. Upon discovering the truth, Vrinda was heartbroken and cursed Bhagwan Vishnu, turning him into a black stone called Shaligram, which is still worshipped by Hindus today. After placing the curse, Vrinda immolated herself in a fire, and from her ashes, the Tulsi plant emerged. Moved by her devotion, Bhagwaan Vishnu declared Tulsi sacred and decreed that she would be worshipped as a Devi. To honor her, a symbolic marriage between Tulsi and Vishnu, known as Tulsi Vivah, is performed every year.   ",
    // 264
    "Makar Sankranti": " Makar Sankranti Makar Sankranti is a festival in Maharashtra that marks the Sun\u2019s transition into Makar Rashi (Capricorn) and the end of winter. Celebrated on 14 January (or sometimes 15th on leap years), it is an important harvest festival. On Sankranti Day, Haldi-Kumkum ceremonies take place, where married women exchange gifts. People also share Tilgul ladoos (sesame and jaggery sweets) while saying, \"Tilgul ghya, goad goad bola\" (Take this sweet and speak sweetly). Kite flying is a key tradition, with people gathering on rooftops and open spaces to fly kites. The sky is filled with kites, and many places hold competitions.  ",
    // 265
    "Mahashivratri": " Mahashivratri Mahashivratri is an important festival in Maharashtra, dedicated to Bhagwaan Shiv. It is celebrated on the fourteenth day of the Krishna Paksha in the month of Phalguna (February-March). The festival marks the union of Bhagwaan Shiv and Devi Parvati and is also associated with Bhagwaan Shiv\u2019s cosmic dance, Tandava, which represents creation, preservation, and destruction. On Mahashivratri, people keep vrats throughout the day and offer milk, honey, ghee, fruits, and bael leaves to the Shiva Linga. Many mandirs organize night-long vigils, where people chant \"Om Namah Shivaya\" and recite prayers. Mandir visits are an important part of the festival, with people gathering at major Shiv mandirs across Maharashtra. Some mandirs also host events which include bhajans and traditional performances. Within families, married women observe vrats for their husband\u2019s well-being, while unmarried women pray for a suitable match.   ",
    // 266
    "Shivaji Jayanti": " Shivaji Jayanti Shiv Jayanti, also known as Chhatrapati Shivaji Maharaj Jayanti, is a festival in Maharashtra that marks the birth anniversary of Chhatrapati Shivaji Maharaj, the founder of the Maratha Empire. It is celebrated on 19 February each year, though some people observe it according to the Hindu calendar. The day is a public holiday in Maharashtra and is observed with various events across the state. Public celebrations include setting up decorated pandals with images or statues of Chhatrapati Shivaji Maharaj. People gather to pay tribute, and sweets are distributed. Chants of \u201cChhatrapati Shivaji Maharaj Ki Jai\u201d and \u201cJai Bhavani, Jai Shivaji\u201d are heard during the celebrations. Processions and two-wheeler rallies take place in different cities across Maharashtra. Replicas of forts are created at various locations to highlight the military achievements of Chhatrapati Shivaji Maharaj.   ",
    // 267
    "Holi": " Holi Holi is celebrated on the full moon (Purnima) of the Phalguna month (February-March) and consists of two main rituals: Holika Dahan and Dhulivandan (Rang Panchami). About a week before the festival, children and young people collect firewood and small donations from the neighborhood. On the evening of Holika Dahan, a large bonfire is lit, symbolizing the victory of good over evil. A community member, often a pujari or someone knowledgeable in mantras, recites verses from the Rig Veda. As part of the ritual, a coconut or Puran Poli is offered to the fire. People make a distinctive sound by striking their mouths with the back of their hands while the fire burns. Each household brings food or sweets to offer to the fire. On the day of Rang Panchami, children and young adults come together with water balloons, colors, and pichkaris. People drench themselves in water and smear colors on each other\u2019s faces and clothes. A special treat prepared during the festival is Puran Poli, a sweet-stuffed flatbread. Children often chant, \"Holi re Holi, Puranachi Poli,\" meaning \"Holi o Holi, sweet-stuffed bread.\" Along with Puran Poli, people also enjoy sugarcane juice and watermelons. Often a traditional drink called Bhaang is also prepared and consumed during the festival. Made with milk and sometimes with cannabis leaves, it is flavored with ingredients like cardamom, cloves, nutmeg, and rosewater.   ",
    // 268
    "Alibag": " Alibag  Alibag, a coastal town in Maharashtra, was a strategic naval base of the Marathas under Kanhoji Angre, the legendary admiral of the Maratha Navy. It served as a defense hub against European colonial powers. The Kolaba Fort, built by Chhatrapati Shivaji Maharaj, stands as a testament to its military significance.  ",
    // 269
    "​Hiuen Tsang": " \u200bHiuen Tsang  \u200bHiuen Tsang (Xuanzang), the renowned Chinese Buddhist monk, visited India during the 7th century CE to study Buddhism. His detailed accounts provide valuable insights into India's historical and cultural landscape. Notably, he documented his visit to Ceul (Chaul), an ancient port town in the present-day Raigad district. This highlights the region's significance as a center of trade and culture during that period.  ",
    // 270
    "Murud Janjira": " Murud Janjira Murud-Janjira is a formidable sea fort located off the coastal town of Murud in Raigad district. Constructed in 1567 by Malik Ambar (military leader), the fort became the stronghold of the Siddi dynasty, which successfully repelled numerous invasion attempts by the Marathas, Mughals, and Portuguese. Notably, Chhatrapati Shivaji Maharaj attempted to capture the fort between 1675 and 1677 but was unsuccessful. The fort's strategic significance and robust architecture have made it an iconic maritime defence symbol in Indian history. \u200b  ",
    // 271
    "Siddi Kings": " Siddi Kings The Siddi rulers, of Abyssinian descent, established the Janjira State in the Raigad district of Maharashtra, with Murud-Janjira Fort as their capital. Renowned for their naval prowess, they successfully defended their territory against multiple invasion attempts by the Marathas, Mughals, and Portuguese. The Siddis' governance in Raigad spanned from the 15th century until India's independence in 1947, marking a significant chapter in the region's history.   ",
    // 272
    "Maratha Angarias": " Maratha Angarias The Angre family, notably Kanhoji Angre, played a pivotal role in the Maratha Navy's dominance along the western coast of India during the early 18th century. While their primary base was at Vijaydurg Fort, their influence extended across the Konkan region, including Raigad district.   ",
    // 273
    "Abyssinian": " Abyssinian Abyssinian descent, the Siddis of Janjira were of Abyssinian origin \u2014 that is, they came from the Horn of Africa, particularly Ethiopia (historically known as Abyssinia). \"Habshi\" (from \"al-Habash\", the Arabic name for Abyssinia) was another term often used to describe them. Siddis established the Janjira State in the late 15th century, with Murud-Janjira Fort as their capital in the present-day Raigad district.   ",
    // 274
    "Mauryas": " Mauryas The Maurya Empire (321\u2013185 BCE) was one of the oldest and ancient India\u2019s most powerful dynasties, founded by Chandragupta Maurya with guidance from Chanakya. At its height under Ashoka (268 BCE), the Great Empire stretched across most of the Indian subcontinent. Ashoka\u2019s adoption of Buddhism and promotion of Dhamma had a lasting impact on Indian culture and governance. The Mauryas maintained a well-organized administration, a strong military, and extensive trade networks, laying the foundation for a unified Indian polity.   ",
    // 275
    "Nalas": " Nalas The Nala dynasty ruled parts of present-day Raigad district, Maharashtra, during the 6th century CE. They coexisted with the Mauryas, as evidenced by inscriptions and historical records. The Nalas' influence in the Konkan region is noted in various historical accounts, indicating their role in the area's early political landscape.   ",
    // 276
    "King Kritivarman I": " King Kritivarman I  Kritivarman I (r. c. 566\u2013592 CE) was a prominent ruler of the Chalukya dynasty. He was known for expanding his kingdom by defeating several neighboring dynasties. He conquered the Nalas, Mauryas of Konkana, Kadambas, Alupas, and the Gangas of Talakad. His victory over the Mauryas of Konkana extended Chalukya influence into the Konkan region, encompassing the present-day Raigad district. These conquests significantly enhanced the Chalukya presence along India's western coast.   ",
    // 277
    "Chalukyas": " Chalukyas  The Chalukyas were a powerful Indian dynasty that ruled over large parts of southern and central India between the 6th and 12th centuries. They were known for their military conquests and mandir architecture. The Chalukyas extended their influence into the Konkan region, defeating local rulers like the Mauryas of Konkana and the Nalas. Their dominance in western India laid the foundation for later regional powers, including the Yadavas and the Marathas.   ",
    // 278
    "Pulikesin II": " Pulikesin Ii  Pulakeshin II (610\u2013640 CE), the greatest ruler of the Chalukya dynasty, expanded his empire through decisive military campaigns. He defeated Harsha of Kannauj, conquered Gujarat, and extended Chalukya control over Maharashtra and the Deccan. His successful southern campaigns established dominance over the Pallavas, marking a golden era for Chalukyan power.   ",
    // 279
    "Suketuvarman": " Suketuvarman Suketuvarman (400 CE) was a Maurya king who ruled the northern Konkan region, including parts of the present-day Raigad district, around the late 4th century CE. His reign is evidenced by the Wada inscription from Thane district, which records donations made by his officer, Simhadatta, to local mandirs.   ",
    // 280
    "Pliny": " Pliny Pliny the Elder (23\u201379 CE) was a Roman author, naturalist, and historian known for his encyclopedic work \"Naturalis Historia\". He documented trade routes between Rome and India, mentioning Indian ports, including those possibly linked to Raigad's coastal areas. His accounts provide insights into ancient Indo-Roman maritime commerce.   ",
    // 281
    "Western Kshatrapas": " Western Kshatrapas  The Western Kshatrapas (circa 35\u2013405 CE) were a dynasty of Indo-Scythian rulers who controlled parts of western India, including Maharashtra and Gujarat. They were the successors of the Indo-Scythians and contemporaries of the Satavahanas, with whom they frequently clashed. The Kshatrapas issued numerous inscriptions and coins, contributing to regional trade and administration. In Raigad, their rule influenced maritime commerce and fortified settlements, shaping the region's early political landscape before the rise of later Indian dynasties.  ",
    // 282
    "Rudradaman I": " Rudradaman I Rudradaman I: (r. 130\u2013150 CE) was a prominent ruler of the Western Kshatrapas, known for his military conquests and patronage of Sanskrit. He expanded his empire by defeating the Satavahanas and strengthened trade networks. His Junagadh inscription, one of the earliest Sanskrit inscriptions, highlights his administrative and infrastructural achievements.  ",
    // 283
    "Satavahana King": " Satavahana King The Satavahanas (circa 1st century BCE \u2013 3rd century CE) were one of the earliest Indian dynasties to rule over the Deccan. They played a crucial role in promoting trade, maritime links, and Buddhist culture. In the Raigad region, their influence is evident through ancient trade routes and Buddhist caves, such as those in Kanheri and Kondane. The Satavahanas maintained strong commercial ties with Rome and Southeast Asia, fostering economic prosperity and cultural exchanges.   ",
    // 284
    "Kushan": " Kushan The Kushan Empire (1st\u20133rd century CE) had indirect influence over Raigad through trade networks connecting the Deccan with Central Asia and Rome. Their rule facilitated the spread of Buddhism, impacting Buddhist sites in the region. Coastal trade routes in Raigad were linked to the Kushan-controlled Silk Road, enhancing commerce.  ",
    // 285
    "Indo-Scythian": " Indo-Scythian \u200bThe Indo-Scythians, also known as Sakas, were nomadic Iranian peoples who migrated into the Indian subcontinent between the 2nd century BCE and 4th century CE. They established several dynasties across northwestern and western India, including regions like Gujarat and Maharashtra. In Maharashtra, their influence extended to areas such as Raigad, where they controlled important trade routes and coastal settlements, integrating the region into broader Indo-Scythian political and economic networks. Their presence in Raigad contributed to the area's historical development during this period.\u200b   ",
    // 286
    "Shilahara Dynasty": " Shilahara Dynasty  The Shilahara dynasty ruled parts of Maharashtra, including Raigad, between the 8th and 13th centuries CE. They were initially feudatories of the Rashtrakutas but later became independent rulers. The Shilaharas significantly contributed to ancient mandir architecture, trade, and administration in the Konkan region. Raigad, an important territory under their rule, flourished as a center of cultural and economic activity. They built several forts and temples, strengthening regional governance. Their rule laid the foundation for later dynasties, including the Yadavas and the Marathas.   ",
    // 287
    "Kadambas": " Kadambas  The Kadamba dynasty (4th\u20136th century CE) was an influential ruling house in southern and western India, known for pioneering early Kannada and Sanskrit inscriptions. Though primarily based in Karnataka, their influence extended into parts of Maharashtra, including Raigad. They contributed to regional temple architecture and trade networks, shaping the early Deccan polity.  ",
    // 288
    "Jimutvahana": " Jimutvahana \u200bJimutavahana (c. 12th century) was a notable Indian Sanskrit scholar from Bengal, renowned for his contributions to Hindu legal literature. His seminal work, the D\u0101yabh\u0101ga, focuses on inheritance laws and significantly influenced legal practices in Bengal. Additionally, he authored Kalaviveka, analyzing auspicious timings for rituals, and Vyavah\u0101ra-m\u0101t\u1e5bk\u0101, addressing judicial procedures. His writings have had a lasting impact on the development of Hindu law. \u200b   ",
    // 289
    "Masudi": " Masudi Abu al-Hasan Ali al-Masudi (c. 896\u2013956 CE) was an Arab historian and geographer known for his extensive travels and detailed accounts of different regions, including India. In his work Muruj al-Dhahab (Meadows of Gold), he provides insights into Indian society, trade, and political structures. His descriptions of maritime routes and trade connections highlight India's significance in global commerce. His writings serve as valuable historical records of the medieval world.   ",
    // 290
    "Jhanjha": " Jhanjha  Jhanjha (910-930 CE) was a notable ruler of the North Konkan branch of the Shilahara dynasty, which governed between the 8th and 13th centuries. He ruled from Chaul (Saimur), a significant port town, highlighting its maritime importance. His reign is marked by the promotion of trade, mandir patronage, and administrative stability. Jhanjha played a key role in strengthening the Shilahara influence along the Konkan coast, ensuring economic prosperity through active engagement in regional and international trade networks.   ",
    // 291
    "Anantpai": " Anantpai \u200bAnantpal (1081-1096 CE ), also known as Anantdev, was the fourteenth ruler of the Shilahara dynasty in North Konkan, succeeding his father, Mummuni or Mamvani. His reign is documented in inscriptions dated 1081 and 1096 CE. Notably, a 1096 CE grant mentions Anantpal governing the entire Konkan region, spanning fourteen hundred villages.   ",
    // 292
    "Allauddin Khilji": " Allauddin Khilji Alauddin Khilji (r. 1296\u20131316 CE)was the second and arguably one of the most powerful ruler of the Khilji dynasty of the Delhi Sultanate. Known for his ambitious military campaigns, he expanded the empire deep into South India and successfully repelled multiple Mongol invasions. A shrewd administrator, he introduced strict market reforms, price control systems, and maintained a large standing army. His reign is also marked by authoritarian rule, centralized power, and controversial legends such as the siege of Chittor and the story of Rani Padmini.   ",
    // 293
    "Red Sea": " Red Sea The Raigad district, located along India's Konkan coast, has historically been a significant trading hub. According to the district gazetteer, it maintained extensive trade networks extending westward towards the Red Sea and Egypt, and possibly inland towards the Bay of Bengal and further east. The gazetteer details a diverse range of goods exported from and imported into the district, underscoring its importance in both regional and international trade. This strategic positioning facilitated economic prosperity and cultural exchanges, highlighting Raigad's role in ancient maritime commerce.   ",
    // 294
    "Bhor Ghats": " Bhor Ghats  The Bhor Ghat is a crucial mountain pass in the Western Ghats, connecting Mumbai and Pune. Historically, it served as a vital trade route for goods transported between the Konkan coast and the Deccan Plateau. The Marathas, British, and earlier dynasties extensively used this pass for commerce and military movements. Today, it remains significant for railway and road transportation, with the Mumbai-Pune Expressway and railway line passing through it. The district gazetteer highlights its importance in facilitating inland and coastal trade.   ",
    // 295
    "Persian Gulf": " Persian Gulf The Persian Gulf (it\u2019s a strategic body of water in the Middle East, located between Iran to the north and the Arabian Peninsula to the south) played a crucial role in India\u2019s ancient maritime trade, including routes connected to Raigad and the Konkan coast. Ports like Chaul (Saimur) facilitated trade with Persia, Mesopotamia, and the Arabian Peninsula. Goods such as spices, textiles, and precious stones were exported, while dates, horses, and pearls were imported.   ",
    // 296
    "Nagothana": " Nagothana  Nagothana, located in Raigad district, has been a historically significant trade and transport hub. Positioned on the banks of the Amba River, it played a crucial role in ancient maritime trade, facilitating connections between the Konkan coast, the Deccan, and the Arabian Sea. During the Silhara rule, it served as an important inland trading center, supporting commerce with Persian Gulf regions and Southeast Asia. Even during Maratha rule, Nagothana remained a key route for inland trade.   ",
    // 297
    "Savitri  River": " Savitri River \u200bThe Savitri River, originating from Mahabaleshwar, traverses the Raigad district and holds significant cultural and historical importance. According to local folklore, the river is linked to a tale involving Lord Brahma and Goddess Savitri. During a yagna (sacrificial ritual), Brahma's disregard for Savitri led her to transform him, along with Vishnu and Shiva, into rivers: Shiva became the Koyna River, Vishnu the Krishna River, and Savitri herself became the river bearing her name. \u200bThe river has been integral to the region's history, supporting agriculture and settlements along its banks for centuries. In 2016, the river gained tragic notoriety when a British-era bridge over it collapsed during heavy rains, resulting in several fatalities. \u200b   ",
    // 298
    "Erthraean Sea": " Erthraean Sea The Erythraean Sea, known today as the Arabian Sea,(The Arabian Sea, historically known as the Erythraean Sea, is a large body of water in the northwestern Indian Ocean, situated west of India and bounded by Pakistan, Iran, Oman, Yemen, and the Arabian Peninsula.) was central to ancient maritime trade routes connecting the Konkan coast, including the Raigad region, with regions like the Roman Empire. The Periplus of the Erythraean Sea, a 1st-century CE mariner's guide, mentions ports such as Symulla (identified with Chaul in Raigad), highlighting its role in international commerce. \u200b   ",
    // 299
    "Kanheri Cave": " Kanheri Cave Kanheri Caves are a cave complex, consisting of over 100 rock-cut caves. These caves served as a significant Buddhist monastic center and were used for meditation, study, and worship. The complex includes viharas (monasteries), chaityas (prayer halls), stupas, and intricate sculptures, reflecting the evolution of Buddhist architecture in western India. These rock-cut caves, carved from basalt, feature viharas (monasteries), chaityas (prayer halls), and inscriptions in Brahmi and Devanagari scripts. The site was a thriving trade and religious hub, with monks overseeing routes connecting the Konkan coast, including Raigad, to inland Maharashtra.   ",
    // 300
    "Idrisi": " Idrisi Idrisi: Al-Idrisi (1100\u20131165 CE) was a renowned Arab geographer and cartographer. He,documented Indian coastal trade routes in his work Tabula Rogeriana (1154 CE). He described Konkan and Raigad's maritime connections, highlighting Chaul (in Raigad) (Saimur) as a major port engaged in commerce with the Persian Gulf, Red Sea, and Indian Ocean regions. His accounts provide valuable insights into Raigad\u2019s role in medieval trade networks.   ",
    // 301
    "Sopara": " Sopara  An ancient port town in the present-day Palghar district, Sopara (Shurparaka) was a major trade hub and centre of buddhist learning in antiquity. It played a key role in Buddhist and maritime history, with links to Persian Gulf, Red Sea, and Southeast Asia. Buddhist relics, including an Ashokan edict, were found here.  ",
    // 302
    "Athanasius Nikitin": " Athanasius Nikitin :Athanasius Nikitin (1446-1472 CE) was a Russian traveler and merchant who visited India between 1468 and 1474. His travelogue, Voyage Beyond Three Seas, provides one of the earliest foreign accounts of India. In Raigad, Nikitin\u2019s journey through the Deccan region gives insights into the trade and cultural landscape of Western India, including ports along the Konkan coast. His accounts highlight Indo-Russian trade relations and the prosperity of maritime commerce in regions like Chaul and other trading centers near Raigad.   ",
    // 303
    "John Mandeville": " John Mandeville John Mandeville (1357-1371 CE)was a medieval traveler and writer credited with The Travels of Sir John Mandeville, a widely read travelogue from the 14th century. Mandeville\u2019s accounts indirectly reflect the medieval European perception of India\u2019s wealth and trade. While he did not explicitly mention Raigad, his descriptions of Indian maritime trade, ports, and exotic goods align with the thriving Konkan coast\u2019s commercial activities, which included ports like Chaul and Nagothana, historically linked to Raigad.   ",
    // 304
    "Bijapur Sultanate": " Bijapur Sultanate  The Bijapur Sultanate (The Bijapur Sultanate (1490\u20131686) was a Deccan sultanate in present-day Karnataka, India. It was founded by Yusuf Adil Shah after breaking away from the Bahmani Sultanate and became a major power in the region before being annexed by the Mughal Empire under Aurangzeb in 1686). Played a crucial role in the history of Raigad. The Adil Shahi rulers controlled port towns like Chaul and engaged in conflicts with the Portuguese and Marathas for dominance over coastal trade routes. The Sultanate's weakening in the 17th century enabled Chhatrapati Shivaji Maharaj to expand Maratha control, including capturing Raigad Fort in 1656 from a local More chief under Bijapur\u2019s influence. The fort later became the capital of the Maratha Empire in 1674.   ",
    // 305
    "Varthema": " Varthema  Ludovico di Varthema (1470-1517) was an Italian traveler and merchant who explored India in the early 16th century, documenting trade routes, maritime commerce, and socio-political conditions. His accounts provide valuable insights into pre-Portuguese coastal trade in western India, including regions near Raigad. Source: Varthema, Ludovico di. The Travels of Ludovico di Varthema. Hakluyt Society, 1863.   ",
    // 306
    "Antora Port": " Antora Port  According to the Kolaba Gazetteer (1964), Antora Port was historically known as Chaul. Chaul, an ancient port town in Maharashtra, was a significant maritime trade center with connections to various regions, including the Red Sea, the Persian Gulf, and Southeast Asia. It was known by different names in historical records, including Chainpavati and Revatikshetra in Hindu traditions. Over time, its strategic importance attracted various ruling dynasties, including the Satavahanas, Shilaharas, and the Portuguese, who established a stronghold in the region.   ",
    // 307
    "Shaista Khan": " Shaista Khan Shaista Khan: Shaista Khan, a Mughal general and governor of the Deccan under Emperor Aurangzeb, played a crucial role in Mughal-Maratha conflicts. In 1660, he launched an extensive campaign against Chhatrapati Shivaji Maharaj, capturing Pune and attempting to suppress Maratha resistance. However, his failure to capture Raigad, the Maratha capital, demonstrated Shivaji\u2019s strategic superiority. The Marathas\u2019 surprise attack on Shaista Khan\u2019s residence in Pune (1663) forced his retreat, marking a turning point in Mughal-Maratha warfare.   ",
    // 308
    "Sadashivrav Bhau": " Sadashivrav Bhau Sadashivrao Bhau (1730-1761) was the commander-in-chief of the Maratha forces during the Third Battle of Panipat (1761). He played a crucial role in the Maratha Empire\u2019s military expansion. Before the battle, he was instrumental in managing the Deccan administration from Raigad and Pune, reinforcing Maratha authority. He focused on strengthening the empire\u2019s finances and military logistics. His defeat at Panipat was a major setback, yet his efforts solidified Maratha governance in Raigad and the Deccan. Source: Maharashtra State Gazetteers, Government of Maharashtra   ",
    // 309
    "Benel Israel Jews": " Benel Israel Jews  The Bene Israel Jews are one of the oldest Jewish communities in India, with their origins traced back to the west coast of Maharashtra, including Raigad. According to the local Marathi-speaking Bene Israel population, they are believed to be descendants of Jewish traders or refugees who were shipwrecked off the Konkan coast centuries ago. Over time, they adopted local customs while maintaining their distinct religious practices. Raigad, particularly Alibag and its surrounding villages, served as an early settlement for the Bene Israel community, influencing their cultural and social development.  ",
    // 310
    "The Sabbath": " The Sabbath The Sabbath (Shabbat) is the Jewish day of rest, observed from Friday evening to Saturday evening. It holds deep religious significance, symbolizing God's day of rest after creation. The Bene Israel Jews of Raigad, particularly in Alibag and surrounding areas, traditionally observed Sabbath rituals, including lighting oil lamps (ner tamid) and refraining from work. Their practice of Sabbath distinguished them within the local community while integrating elements of the Konkan region\u2019s culture.   ",
    // 311
    "Alauddin Khilji": " Alauddin Khilji Alauddin Khilji (1296\u20131316)was the second ruler of the Khilji dynasty. He expanded the Delhi Sultanate through aggressive military campaigns up to the Deccan, including Raigad and surrounding regions. He took control of the trade routes and argued that he had weakened regional powers. He is known for his economic reforms and market regulations during his rule.   ",
    // 312
    "Vijayanagara": " Vijayanagara Vijayanagara Empire (1336\u20131646) was a powerful South Indian kingdom founded by Harihara I and Bukka I. Though primarily centered in Karnataka, its influence extended into Raigad through maritime trade and diplomatic ties with local rulers. The empire's naval strength contributed to commerce along the Konkan coast, linking Raigad to broader Indian Ocean trade networks. It played a crucial role in resisting Islamic invasions and fostering trade, culture, and architecture.   ",
    // 313
    "Anegundi Kings": " Anegundi Kings Anegundi Kings \u2013 Anegundi, considered to be the precursor to the Vijayanagara Empire. It was ruled by the Kampili dynasty before Harihara I and Bukka I established Vijayanagara in 1336. The Anegundi region, located in present-day Karnataka, was historically significant for its strategic location and connections to Hindu myth. Though primarily associated with the early Vijayanagara rulers, Anegundi maintained its cultural and political influence in the Deccan, including maritime trade with coastal regions like Raigad.   ",
    // 314
    "Kanara Kings": " Kanara Kings The Kanara region, encompassing parts of present-day Karnataka and Goa, was historically ruled by various dynasties, including the Kadambas, Vijayanagara rulers, and later the Nayakas of Keladi. These rulers played a crucial role in coastal trade, connecting the Western Ghats to Arabian Sea commerce. The Kanara kings maintained maritime trade relations with ports like Chaul in Raigad, making the region significant in the Deccan\u2019s economic network.   ",
    // 315
    "Basavanna": " Basavanna  According to the Lingayat community (Basvanna): founded in the 12th century by Basava in Karnataka, follows the philosophy of Shaivism with a strong emphasis on social equality and devotion to Lord Shiva. Lingayats played a key role in regional politics and trade, including in Raigad, where their influence extended through the Deccan\u2019s economic and spiritual networks. Their contributions in administration, especially under the Vijayanagara and later Maratha rule, highlight their historical significance.   ",
    // 316
    "Redi": " Redi  Redi is a coastal town in Sindhudurg district, known for its iron ore mines and the historic Yashwantgad Fort. The port of Redi played a role in regional trade, linking the Konkan coast to wider maritime routes, including those towards the Persian Gulf and the Red Sea. The area is also famous for the Redi Ganpati mandir, a significant religious site.   ",
    // 317
    "Muhammad Gawan": " Muhammad Gawan Muhammad Gawan (1411\u20131481) was a prominent statesman, scholar, and prime minister of the Bahmani Sultanate during the reign of Sultan Muhammad Shah III. He played a key role in expanding and consolidating Bahmani rule, implementing administrative reforms, and fostering Persian culture in the Deccan. His policies strengthened the sultanate\u2019s control over trade and maritime routes, including coastal regions like Raigad. However, court rivalries led to his execution in 1481.  ",
    // 318
    "Muhammad Shah": " Muhammad Shah Muhammad Shah (r. 1358\u20131375) \u2013 Muhammad Shah I was the second ruler of the Bahmani Sultanate, succeeding his father, Alauddin Bahman Shah. He consolidated the Bahmani kingdom, expanded its territories, and strengthened its administrative structure. His reign saw conflicts with the Vijayanagara Empire and local chieftains, including those controlling coastal and trade hubs like Raigad. His efforts laid the foundation for later rulers to establish the Deccan as a dominant power.   ",
    // 319
    "Burhan Nizam Shah": " Burhan Nizam Shah Burhan Nizam Shah (1509\u20131553) \u2013 Burhan Nizam Shah was the ruler of the Ahmadnagar Sultanate, one of the breakaway Deccan Sultanates that emerged after the fall of the Bahmani Sultanate. He played a crucial role in Deccan politics, forging alliances and rivalries with Bijapur, Golconda, and the Mughals. His rule saw efforts to strengthen Ahmadnagar\u2019s economy and military. Raigad\u2019s coastal trade routes were indirectly influenced by his expansionist policies and conflicts in the region.   ",
    // 320
    "Siddi Dynasty": " Siddi Dynasty The Siddi Dynasty, of African Abyssinian origin, ruled Janjira on the Raigad coast from the late 16th century. Known for their naval strength, they resisted Maratha and Portuguese attempts to capture their stronghold. The Siddis of Janjira played a crucial role in Deccan politics, often aligning with the Mughals against the Marathas. Their naval power influenced maritime trade and defense along the Konkan coast, impacting Raigad's strategic importance.   ",
    // 321
    "Ramrao Patil": " Ramrao Patil  \u200bRaja Ram Rao Patil, also known as Itbarrao Koli, was a prominent figure in the history of Janjira Island, located in the present-day Raigad district, Maharashtra. As an admiral of the Ahmadnagar Navy and a leader of the Koli community, he played a pivotal role in the establishment and fortification of the Janjira Fort. \u200b   ",
    // 322
    "Piram Khan": " Piram Khan  Piram Khan was a general and naval admiral of the Ahmadnagar Sultanate who captured Janjira Fort in the late 16th century.   ",
    // 323
    "Richard Eaton": " Richard Eaton \u200bRichard M. Eaton, a historian at the University of Arizona, has extensively studied the Deccan region's social and cultural history. His work, A Social History of the Deccan, 1300\u20131761: Eight Indian Lives, provides insights into the area's historical dynamics. While this work offers a comprehensive understanding of the Deccan's history, specific references to Raigad are not prominently featured in the available sources.\u200b  ",
    // 324
    "Danda Rajpuri": " Danda Rajpuri  \u200bDanda-Rajpuri, also known as Samrajgad, is a fort located near Murud in the Raigad district. Constructed by Chhatrapati Shivaji Maharaj, it was strategically positioned to monitor and challenge the Siddi-controlled Janjira Fort. In 1671, the Siddis, led by Siddi Khairiyat Khan, launched a surprise attack during the Holi festival, capturing Danda-Rajpuri and thwarting Shivaji's plans against Janjira. \u200b   ",
    // 325
    "Rairy Fort": " Rairy Fort Rairy Fort, historically known as Rairi, is a hill fort located near Mahad in Maharashtra's Raigad district. In 1674, Chhatrapati Shivaji Maharaj chose it as the capital of the Maratha Empire, renaming it Raigad Fort. The fort stands approximately 820 meters above its base and 1,356 meters above sea level, offering strategic defense and panoramic views of the Sahyadri mountains. Today, visitors can access the fort via a pathway of about 1,737 steps or by using the Raigad Ropeway.   ",
    // 326
    "Hiroji Indulkar": " Hiroji Indulkar \u200bHiroji Indulkar was a 17th-century architect renowned for constructing Raigad Fort, which became the capital of the Maratha Empire under Chhatrapati Shivaji Maharaj. He also built Sindhudurg and Pratapgad forts. His dedication is commemorated at the Jagdishwar Temple in Raigad, where a tile inscribed with \"Seveche thayi tatpar, Hiroji Indulkar\" (\"always ready for service, Hiroji Indulkar\") is placed at the entrance. \u200b  ",
    // 327
    "Raigad Fort": " Raigad Fort Raigad Fort, located in Raigad district, was historically referred to as the \"Gibraltar of the East\" by early Europeans due to its strategic hilltop position and formidable defenses. This designation underscores the fort's significance as a nearly impregnable stronghold during its time.\u200b  ",
    // 328
    "Nagarkhana Darwaja": " Nagarkhana Darwaja Nagarkhana Darwaja: \u200bNagarkhana Darwaja, a prominent gateway at Raigad Fort, is a three-story structure that historically faced the royal throne in the king's court. This architectural feature was acoustically designed to facilitate clear hearing from the doorway to the throne. Today, the platform houses an octagonal ornate canopy with a seated image of Chhatrapati Shivaji Maharaj placed above the original location of the throne. \u200b   ",
    // 329
    "Gaga Bhatt​": " Gaga Bhatt: \u200b  \u200bGaga Bhatt, a 17th-century Brahmin scholar from Varanasi, presided over the coronation of Chhatrapati Shivaji Maharaj at Raigad Fort on June 6, 1674. Renowned as \"Vedonarayana,\" he was esteemed for his expertise in Vedic discourse. \u200b  ",
    // 330
    "Zulfikar Khan": " Zulfikar Khan  \u200bZulfiqar Khan, born Muhammad Ismail (1649/1657\u20131713), was a prominent Mughal noble and military leader. In 1689, he led the siege of Raigad Fort, resulting in its capture and the escape of Maratha king Rajaram. This victory earned him the title \"Nusrat Jung.\" Later, as Viceroy of the Deccan, he pursued conciliatory policies toward the Marathas. \u200b   ",
    // 331
    "Bhavani": " Bhavani Tulja Bhavani, a revered form of devi Durga, holds profound significance in the life of Chhatrapati Shivaji Maharaj, the founder of the Maratha Empire. The Tulja Bhavani mandir, located in Tuljapur, is one of the state's four major Shakti Peethas. Shivaji Maharaj frequently visited this temple to seek the goddess's blessings for his military campaigns. According to legend, during one such visit, the devi appeared to him in a dream, presenting a divine sword known as the Bhavani Talwar. This sword became a symbol of his valor and divine support in his quest to establish the Maratha Empire. \u200b   ",
    // 332
    "Raghuji Bhosle": " Raghuji Bhosle \u200bRaghuji Bhonsle (1695\u20131755) was a distinguished Maratha general who established the Bhonsle dynasty's rule in Nagpur. Serving under Chhatrapati Shahu I, he rose to prominence by defeating local Gond rulers and expanding Maratha influence across central India. His reign marked significant military campaigns, notably in Bengal and Odisha, enhancing the Maratha Empire's territorial reach. Raghuji's leadership laid the foundation for Nagpur's prominence within the empire. \u200b   ",
    // 333
    "Peshwa Bajirao Pingale": " Peshwa Bajirao Pingale Bajirao I (1700\u20131740) was the seventh Peshwa (Prime Minister) of the Maratha Empire. Appointed at age 19 by Chhatrapati Shahu I, he expanded Maratha influence across India. Renowned for his military prowess, Bajirao never lost a battle. His leadership significantly shaped Maratha history. \u200b   ",
    // 334
    "Underi Fort": " Underi Fort  \u200bUnderi Fort, also known as Jaidurg, is a historic sea fort located near the mouth of Mumbai Harbour, south of Prong's Lighthouse in Maharashtra, India. Constructed in 1680 by Kahim of the Siddis, it served as a strategic counterpart to the nearby Khanderi Fort, together forming significant fortifications along the Maharashtra coast. The fort is situated approximately 2 km offshore and is characterized by two prominent hills. Its robust ramparts and bastions are notable features, and the site offers panoramic views of the surrounding sea and the nearby Alibaug beach. Access to the fort is primarily by boat during low tide, with departures from Thal village near Alibaug. Visitors can explore the fort's remnants, including several bastions equipped with cannons, water cisterns, and a cave with carvings. Despite its current dilapidated state, Underi Fort remains a testament to the region's rich history and military architecture.   ",
    // 335
    "Padmadurg": " Padmadurg  \u200bPadmadurg Fort, also known as Kasa Fort, is a historic sea fort constructed by Chhatrapati Shivaji Maharaj in 1676 to monitor the activities of the nearby Janjira Fort. Situated about 4 km northwest of Janjira, it played a strategic role in safeguarding the Konkan coast. The fort features six bastions and was recaptured by the Marathas from the Siddis in 1759. Today, Padmadurg remains a significant testament to Maratha naval architecture and history. \u200b   ",
    // 336
    "James Forbes": " James Forbes James Forbes (1749\u20131819) was a British artist and writer who served as a writer for the British East India Company in India from 1765 to 1784. During his time in India, Forbes produced numerous sketches and paintings, documenting various aspects of Indian life, flora, fauna, and architecture. His works provide valuable insights into India's cultural and natural history during the 18th century.   ",
    // 337
    "Wind Speed": " Wind Speed Wind speed refers to the rate of air movement measured over a distance per unit of time, typically in kilometers per hour (km/h) or meters per second (m/s).  ",
    // 338
    "Night Light": " Night Light Night light data measures artificial illumination visible from space; it's often used to estimate urbanization, economic activity, and infrastructure development.  ",
    // 339
    "Groundwater": " Groundwater Groundwater is water found underground in aquifers, used for drinking, irrigation, and industrial purposes. It is a critical resource in water-scarce regions.  ",
    // 340
    "Micro, Small, and Medium Enterprises": " Micro, Small, And Medium Enterprises MSMEs are businesses categorized by their investment and turnover limits; they play a vital role in employment and GDP, especially in developing economies like India.  ",
    // 341
    "Fatalities": " Fatalities Number of persons who died due to road traffic accidents, either on the spot or within 30 days of the crash.  ",
    // 342
    "Grievous Injuries": " Grievous Injuries Serious injuries resulting from road accidents that involve prolonged hospitalization, permanent disability, or loss of limb/sight.  ",
    // 343
    "Minor Injuries": " Minor Injuries Non-life-threatening injuries from road accidents that require short-term medical treatment and cause no permanent disability.  ",
    // 344
    "Non-injury Crashes": " Non-Injury Crashes Road accidents where no person is injured, though there may be vehicle or property damage.  ",
    // 345
    "National Highways": " National Highways Major roads connecting multiple states, constructed and maintained by the central government for long-distance and high-volume traffic.  ",
    // 346
    "Expressways": " Expressways Access-controlled, high-speed corridors designed for uninterrupted traffic flow, typically connecting major urban centers.  ",
    // 347
    "Major State Highways": " Major State Highways Important state-maintained roads that link district headquarters and key cities to national highways or expressways.  ",
    // 348
    "State Highways": " State Highways Roads managed by state governments that connect towns, tehsils, and rural areas within the state.  ",
    // 349
    "Category of Tourist Places": " Category Of Tourist Places Classification of tourism destinations based on themes such as cultural heritage, nature, adventure, wellness, and religious significance.  ",
    // 350
    "Air Quality Index": " Air Quality Index A numerical scale (typically 0\u2013500) used to communicate how polluted the air is; it reflects the concentration of pollutants like PM2.5, PM10, NO\u2082, etc.  ",
    // 351
    "Outward Migration": " Outward Migration The movement of people leaving a specific district, state, or country to reside or work in another region.  ",
    // 352
    "Inward Migration": " Inward Migration The movement of people into a specific district, state, or country from other regions, typically for employment, education, or resettlement.  ",
    // 353
    "Liquefied Petroleum Gas": " Liquefied Petroleum Gas A mixture of propane and butane gases, stored under pressure as a liquid, used as fuel for cooking, heating, and in some vehicles.  ",
    // 354
    "Kerosene": " Kerosene A flammable hydrocarbon liquid used as fuel for cooking and lighting, particularly in rural and low-income households.  ",
    // 355
    "Piped Natural Gas": " Piped Natural Gas Methane-rich natural gas delivered to homes and industries through a pipeline network, mainly used for cooking, heating, and fuel.  ",
    // 356
    "Main Workers": " Main Workers Persons who worked for 183 days or more in the reference year in any economic activity.  ",
    // 357
    "Marginal Workers": " Marginal Workers Persons who worked for less than 183 days in the reference year in any economic activity.  ",
    // 358
    "Pensioners": " Pensioners Individuals who receive a regular income after retirement from government or organized sector employment.  ",
    // 359
    "Dependents": " Dependents Individuals who do not work and rely on others (e.g., family members) for economic support, such as children, elderly, or disabled persons.  ",
    // 360
    "Public Sector Undertaking": " Public Sector Undertaking A government-owned corporation or enterprise engaged in commercial activities, owned fully or partly by the central or state government.  ",
    // 361
    "Private Proprietorship": " Private Proprietorship A business owned and managed by a single individual with no legal distinction between the owner and the business.  ",
    // 362
    "Private Partnership": " Private Partnership A business entity in which two or more individuals manage and operate a business in accordance with terms and responsibilities laid out in a partnership agreement.  ",
    // 363
    "Private Company": " Private Company A company incorporated under the Companies Act, with limited liability, not publicly traded, and with restrictions on share transfers.  ",
    // 364
    "Self-help Groups": " Self-Help Groups Informal associations of people, usually women, formed to facilitate mutual financial support, savings, and access to credit or government schemes.  ",
    // 365
    "Non-profit Institutions": " Non-Profit Institutions Organizations that operate for social, educational, charitable, or community objectives, not for profit generation.  ",
    // 366
    "Co-operatives": " Co-Operatives Member-owned institutions that operate for mutual benefit, often in areas like agriculture, credit, housing, and consumer services.  ",
    // 367
    "Pay Grade": " Pay Grade A salary classification that determines an employee's compensation based on their role, experience, and qualifications within an organization.  ",
    // 368
    "Non-workers": " Non-Workers Individuals not engaged in any economically productive activity during the reference period, including students, homemakers, and dependents.  ",
    // 369
    "Particulate Matter 10": " Particulate Matter 10 Airborne particles with a diameter of 10 micrometers or less that can penetrate the respiratory tract and cause health issues.  ",
    // 370
    "Particulate Matter 2.5": " Particulate Matter 2.5 Fine inhalable particles with a diameter of 2.5 micrometers or less, posing serious health risks as they can reach deep into the lungs and bloodstream.  ",
    // 371
    "Biomedical Waste": " Biomedical Waste Waste generated from medical and healthcare activities, such as used syringes, bandages, and human tissues, requiring special treatment and disposal.  ",
    // 372
    "Sporadic Forest": " Sporadic Forest Areas with scattered tree cover that do not meet the minimum threshold to be classified as open forest, often less than 10% canopy density.  ",
    // 373
    "Thick Forest": " Thick Forest An informal term often used for forests with higher canopy cover, generally corresponding to dense forest classifications.  ",
    // 374
    "Dense Forest": " Dense Forest Forests with canopy cover between 40% and 70%, as classified in national forest reports.  ",
    // 375
    "Open Forest": " Open Forest Forest areas with canopy density between 10% and 40%, often showing signs of degradation or limited regeneration.  ",
    // 376
    "Actual Rainfall": " Actual Rainfall The recorded amount of precipitation in a specific area over a certain time period, usually measured in millimetres (mm).  ",
    // 377
    "Dry Waste": " Dry Waste Non-biodegradable waste such as plastic, metal, glass, and paper that can be segregated and recycled.  ",
    // 378
    "Wet Waste": " Wet Waste Biodegradable organic waste such as food scraps, vegetable peels, and garden waste that can be composted.  ",
    // 379
    "Wildlife Sanctuary": " Wildlife Sanctuary A protected area designated for the conservation of wild animals and their habitats, where limited human activity is permitted under regulation.  ",
    // 380
    "Tiger Project": " Tiger Project A centrally sponsored scheme (Project Tiger) launched in 1973 for the conservation of tigers in specially created reserves across India.  ",
    // 381
    "Botanical Gardens": " Botanical Gardens Areas dedicated to the collection, cultivation, and display of a wide range of plants for research, education, and conservation.  ",
    // 382
    "Cognizable Crimes": " Cognizable Crimes Crimes for which a police officer can register a case and make an arrest without prior approval from a magistrate (e.g., murder, rape, kidnapping).  ",
    // 383
    "Dowry Deaths": " Dowry Deaths Deaths of women due to harassment over dowry demands, typically occurring within seven years of marriage and considered a punishable offence.  ",
    // 384
    "Insult to the Modesty of Women": " Insult To The Modesty Of Women Offences under IPC Section 509 involving verbal or physical acts intended to outrage or insult a woman's dignity.  ",
    // 385
    "Immoral Traffic Prevention Act": " Immoral Traffic Prevention Act A law aimed at preventing and combating human trafficking and sexual exploitation for commercial purposes.  ",
    // 386
    "Human Trafficking": " Human Trafficking Illegal trade of humans for exploitation, often for forced labor or sexual slavery; addressed under multiple legal provisions including IPC and ITPA.  ",
    // 387
    "Cyber Crimes": " Cyber Crimes Criminal activities carried out using digital technologies, including hacking, identity theft, and online harassment.  ",
    // 388
    "Crime Against Women": " Crime Against Women Any act of violence or discrimination specifically targeting women, including sexual assault, domestic violence, and harassment.  ",
    // 389
    "Indian Penal Code": " Indian Penal Code The comprehensive criminal code of India that defines various offences and prescribes punishments.  ",
    // 390
    "Social Legislation Law": " Social Legislation Law Special and local laws addressing social issues like child marriage, domestic violence, and dowry prohibition, separate from the IPC.  ",
    // 391
    "Police Outposts": " Police Outposts Smaller police units established to extend the reach of law enforcement in remote or high-crime areas, often under the control of a main police station.  ",
    // 392
    "Police Stations": " Police Stations Official local units of law enforcement responsible for maintaining law and order, registering FIRs, and conducting investigations.  ",
    // 393
    "Police Chowkis": " Police Chowkis Sub-units of a police station providing local presence, often staffed with minimal personnel to address community-level law enforcement.  ",
    // 394
    "National Crime Records Bureau": " National Crime Records Bureau A government agency under the Ministry of Home Affairs responsible for collecting and analyzing crime data across India.  ",
    // 395
    "Forestry and Logging": " Forestry And Logging Economic activities involving the management, harvesting, and sale of forest products like timber, fuelwood, and non-timber forest products (NTFPs).  ",
    // 396
    "Aquaculture": " Aquaculture The farming of aquatic organisms such as fish, shrimp, and shellfish under controlled conditions for commercial or subsistence purposes.  ",
    // 397
    "Gross District Value Added": " Gross District Value Added The value of goods and services produced in a district after subtracting the cost of inputs, used to estimate the district\u2019s economic output.  ",
    // 398
    "Gross District Domestic Product": " Gross District Domestic Product The total value of all goods and services produced in a district in a given year, including taxes but excluding subsidies.  ",
    // 399
    "Gross Domestic Product": " Gross Domestic Product The total market value of all final goods and services produced within a country in a specific period, often annually.  ",
    // 400
    "Current Price": " Current Price Economic data expressed in terms of the prices during the year being measured, not adjusted for inflation.  ",
    // 401
    "Gram Panchayat": " Gram Panchayat The basic village-level administrative unit in India\u2019s Panchayati Raj system responsible for local governance and development activities.  ",
    // 402
    "Zilla Parishad": " Zilla Parishad The apex district-level body in the Panchayati Raj system that coordinates development across all blocks and villages within the district.  ",
    // 403
    "Jilla Parishad": " Jilla Parishad Alternate spelling of Zilla Parishad; functionally the same.  ",
    // 404
    "Classified Banks": " Classified Banks Banks classified under scheduled commercial banks by the Reserve Bank of India, including public sector, private sector, and foreign banks.  ",
    // 405
    "Value Added Tax": " Value Added Tax A tax on the value added to goods and services at each stage of production or distribution, now largely subsumed under GST.  ",
    // 406
    "Central Sales Tax": " Central Sales Tax A tax on sales of goods between states in India, levied by the central government but collected by state governments.  ",
    // 407
    "Goods and Services Tax": " Goods And Services Tax A comprehensive indirect tax on manufacture, sale, and consumption of goods and services, replacing many indirect taxes in India.  ",
    // 408
    "Central Goods and Services Tax": " Central Goods And Services Tax The portion of GST collected by the central government on intra-state sales of goods and services.  ",
    // 409
    "Entry Tax": " Entry Tax A tax levied by state governments on goods entering a local area for use, sale, or consumption, now largely replaced by GST.  ",
    // 410
    "Business Tax": " Business Tax General term for taxes levied on business income, profits, or turnover by various levels of government.  ",
    // 411
    "Luxury Tax": " Luxury Tax A tax levied on goods and services considered non-essential or high-end, such as hotels and luxury vehicles, mostly subsumed under GST.  ",
    // 412
    "Entertainment Tax": " Entertainment Tax Tax on entertainment-related activities like cinema, cable, and amusement parks; now mostly replaced by GST.  ",
    // 413
    "National Development and Planning": " National Development And Planning A framework for long-term socio-economic planning and infrastructure development at the national and subnational levels.  ",
    // 414
    "Cooperative Marketing Societies": " Cooperative Marketing Societies Cooperatives formed to help farmers and producers collectively market their goods to get fair prices and avoid exploitation by middlemen.  ",
    // 415
    "Udyam Registrations": " Udyam Registrations Online registration under the Ministry of MSME for classifying enterprises as micro, small, or medium for availing government benefits.  ",
    // 416
    "Registered Factories": " Registered Factories Industrial establishments registered under the Factories Act, 1948, authorized to engage in manufacturing using power and employing workers.  ",
    // 417
    "Working Factories": " Working Factories Factories that were operational and reported production during the reference period, among those registered under the Factories Act.  ",
    // 418
    "Non-institutional Borrowing": " Non-Institutional Borrowing Loans taken from informal sources such as moneylenders, relatives, friends, or local landlords, typically without formal contracts or regulation.  ",
    // 419
    "Self-finance": " Self-Finance The use of an individual\u2019s or household\u2019s own savings or income for funding consumption, business, or development needs, without external borrowing.  ",
    // 420
    "Life Expectancy": " Life Expectancy The average number of years a person is expected to live from birth, based on current mortality patterns.  ",
    // 421
    "Consumer Price Index": " Consumer Price Index An index measuring the average change over time in the prices paid by consumers for a basket of goods and services.  ",
    // 422
    "Foreign Direct Investment": " Foreign Direct Investment Investment made by a company or individual in one country into business interests located in another country, typically in the form of ownership.  ",
    // 423
    "Infant Mortality Rate": " Infant Mortality Rate Number of infant deaths (under 1 year) per 1,000 live births in a given year.  ",
    // 424
    "Maternal Mortality Rate": " Maternal Mortality Rate Number of maternal deaths per 100,000 live births due to complications from pregnancy or childbirth.  ",
    // 425
    "Live Births": " Live Births Births in which the baby shows signs of life after delivery.  ",
    // 426
    "Still Births": " Still Births Births of babies showing no signs of life at or after 28 weeks of gestation.  ",
    // 427
    "Health Management Information System": " Health Management Information System A national digital platform collecting routine service delivery data from health facilities across India.  ",
    // 428
    "National Family Health Survey": " National Family Health Survey A large-scale, multi-round household survey providing data on population, health, and nutrition indicators.  ",
    // 429
    "Female Sterilization": " Female Sterilization A permanent contraceptive method involving surgical blockage of the fallopian tubes (tubectomy).  ",
    // 430
    "Male Sterilization": " Male Sterilization A permanent contraceptive method involving surgical blockage of the vas deferens (vasectomy).  ",
    // 431
    "Winter Fever": " Winter Fever General term for viral fevers prevalent during winter, often caused by respiratory infections.  ",
    // 432
    "Typhoid Fever": " Typhoid Fever A bacterial infection caused by Salmonella typhi, transmitted through contaminated food and water.  ",
    // 433
    "Tuberculosis": " Tuberculosis A contagious bacterial infection primarily affecting the lungs, caused by Mycobacterium tuberculosis.  ",
    // 434
    "Pneumonia": " Pneumonia Lung infection causing inflammation of air sacs, which may fill with fluid or pus, caused by viruses, bacteria, or fungi.  ",
    // 435
    "Dengue": " Dengue A mosquito-borne viral infection causing high fever, rash, and muscle pain, transmitted by Aedes mosquitoes.  ",
    // 436
    "Swine Flu": " Swine Flu A respiratory disease caused by the H1N1 influenza virus, initially found in pigs.  ",
    // 437
    "Paralysis": " Paralysis Loss of muscle function in part of the body, potentially caused by stroke, injury, or neurological conditions.  ",
    // 438
    "Special Hospitals": " Special Hospitals Hospitals that provide specialized medical services like cardiology, oncology, or neurology.  ",
    // 439
    "Clinics": " Clinics Health facilities offering outpatient care, usually for minor illnesses and routine check-ups.  ",
    // 440
    "Maternity Wards": " Maternity Wards Hospital sections dedicated to labor, delivery, and postnatal care of mothers and newborns.  ",
    // 441
    "High Blood Pressure": " High Blood Pressure A chronic condition where the force of the blood against artery walls is consistently too high (hypertension).  ",
    // 442
    "Hip to Waist Ratio": " Hip To Waist Ratio A measure of fat distribution, calculated by dividing waist circumference by hip circumference.  ",
    // 443
    "Body Mass Index": " Body Mass Index A measure of body fat based on height and weight, calculated as weight (kg) / height\u00b2 (m\u00b2).  ",
    // 444
    "Overweight": " Overweight A BMI between 25.0 and 29.9, indicating excess body weight relative to height.  ",
    // 445
    "Obesity": " Obesity A BMI of 30.0 or above, indicating excessive body fat with health risks.  ",
    // 446
    "Oral Cancer": " Oral Cancer Cancer that develops in the tissues of the mouth or throat, often linked to tobacco or alcohol use.  ",
    // 447
    "Cervical Cancer": " Cervical Cancer Cancer arising from the cervix, usually caused by the Human Papillomavirus (HPV).  ",
    // 448
    "Breast Cancer": " Breast Cancer Malignant tumor developed from breast cells, the most common cancer among women in India.  ",
    // 449
    "Tubectomy": " Tubectomy A surgical procedure for female sterilization that involves blocking or removing parts of the fallopian tubes.  ",
    // 450
    "Vasectomy": " Vasectomy A male sterilization procedure that involves cutting or sealing the vas deferens.  ",
    // 451
    "Intrauterine Device": " Intrauterine Device A small T-shaped contraceptive device inserted into the uterus to prevent pregnancy.  ",
    // 452
    "Family Planning": " Family Planning Strategies and services that allow individuals to anticipate and attain their desired number of children and spacing of pregnancies.  ",
    // 453
    "Severely Wasted": " Severely Wasted Children with extremely low weight-for-height, indicating acute malnutrition.  ",
    // 454
    "Stunted Growth": " Stunted Growth Low height-for-age in children, indicating chronic undernutrition.  ",
    // 455
    "Malnutrition": " Malnutrition A condition resulting from an imbalanced intake of nutrients\u2014includes undernutrition and overnutrition.  ",
    // 456
    "Malnourished": " Malnourished Individuals who suffer from malnutrition, whether from lack of nutrients or poor absorption.  ",
    // 457
    "Anemic": " Anemic A condition where there is a deficiency of red blood cells or hemoglobin in the blood, leading to fatigue and weakness.  ",
    // 458
    "Bajri": " Bajri Pearl Millet  ",
    // 459
    "Tur": " Tur Pigeon Pea  ",
    // 460
    "Jowar": " Jowar Sorghum  ",
    // 461
    "Urad": " Urad Black Gram  ",
    // 462
    "Tifan": " Tifan An implement used by farmers to sow seeds  ",
    // 463
    "Moong": " Moong Green Gram  ",
    // 464
    "Udid": " Udid Black Gram  ",
    // 465
    "Haihya Kingdom": " Haihya Kingdom  The Haihaya kingdom, ruled by the Yadava dynasty, was a prominent power in ancient central India, with its capital at Mahishmati associated with Maheshwar in present-day Madhya Pradesh. They are prominently mentioned in the Puranas and the Mahabharata. It is believed that the zamindars of the Chandrapur region were at one time subject to the Haihaya rulers of Chhattisgarh. The Haihayas were known for their military prowess and known for playing a significant role in shaping the political landscape of central India.  ",
    // 466
    "Gonda": " Gonda  The Gonds are a major community in Chandrapur district, known for their distinct culture, language, and history. Chandrapur was once part of the Gond dynasty's dominion, particularly under rulers like Khandkya Ballal Sah, who founded Chandrapur city in the 13th century.   ",
    // 467
    "Vakataka Dynasty": " Vakataka Dynasty  The Vakataka dynasty was a significant Indian ruling house originating in the central Deccan in the mid-3rd century CE. Their empire is believed to have extended from Malwa and Gujarat in the north to the Tungabhadra River in the south, and from the Arabian Sea in the west to the Bay of Bengal in the east. The Vakatakas were contemporaries of the Guptas and succeeded the Satavahanas in the Deccan region. They are noted for their contributions to art and architecture, particularly the patronage of the Ajanta Caves.  ",
    // 468
    "International Buddha Dhamma": " International Buddha Dhamma  International Buddha Dhamma movement is a social and cultural movement with an emphasis on social justice and equality informed by bhagwan Buddha\u2019s teachings. Chandrapur holds significant importance in this regard as the ancient Vijasan Buddhist Caves in Bhadravati have hosted international Buddha Dhamma conventions, attracting monks and leaders worldwide. \u200bAdditionally, the Yenbodi Vipassana Center in Ballarpur offers structured meditation courses, contributing to the district's spiritual landscape. \u200bFurthermore, the Dhammakirti Buddha Vihar in Chandrapur has been a site for significant events, such as the Buddha Datu installation ceremony conducted by monks from Thailand and India.   ",
    // 469
    "King Jajalladeva": " King Jajalladeva King Jajalladeva I (r. 1090\u20131120 CE) of the Kalachuri dynasty of Ratnapura played a significant role in the history of the Chandrapur region. By the late 12th century, the Nagas of Manikgarh became his feudatories, indicating the extent of his influence into present-day Chandrapur district. Jajalladeva I is also credited with reconstructing temples at Pali, as evidenced by inscriptions bearing his name. His reign marked the expansion of Kalachuri authority into eastern Maharashtra, leaving a lasting impact on the region's cultural and political landscape.\u200b  ",
    // 470
    "Nagavanshi Kings of Bastar": " Nagavanshi Kings Of Bastar  The Nagavanshi kings of Bastar, notably the Chhindaka Nagas, ruled the Chakrakota mandala\u2014encompassing present-day Bastar, Koraput, and Kalahandi\u2014between the 9th and 12th centuries CE. Their influence extended into regions like Chandrapur, as evidenced by cultural and architectural similarities. A notable legacy is the Dholkal Ganesh murti in Dantewada, a six-foot granite sculpture weighing over 500 kg, attributed to their reign. Local lore speaks of a Nagavanshi princess, Chameli Devi, whose valor inspired Annamdev of Warangal to unify Bastar under his rule. \u200b  ",
    // 471
    "Wairagha": " Wairagha  Wairagarh, located in present-day Chandrapur district, was the capital of the Mana dynasty, which ruled the region from approximately 650 to 850 CE. The Manas established several forts, including Wairagarh, Garbori, Rajoli, Surjagarh, and Manikgarh\u2014named after Manikyadevi. Their rule ended when Kol Bhill, a Gond leader, overthrew them, leading to the rise of Gond dominance in the area. This transition marked a significant shift in the region's political landscape. \u200b  ",
    // 472
    "Garha Kingdom": " Garha Kingdom The Garha Kingdom, also known as Garha-Mandla, was a prominent Gond dynasty in central India. While its core territory lay in present-day Madhya Pradesh, its influence extended into regions like Chandrapur. Chandrapur, historically referred to as the Chanda Kingdom, was one of the three major Gond principalities alongside Garha-Mandla and Deogarh. These kingdoms, though nominally under Mughal suzerainty, maintained significant autonomy and shared cultural and political ties. The interconnectedness of these Gond states highlights the Garha Kingdom's influence in shaping the historical landscape of Chandrapur.  ",
    // 473
    "Kherla Kingdom": " Kherla Kingdom : The Kherla Kingdom, centered in present-day Betul, Madhya Pradesh, was among the earliest Gond kingdoms in central India. Founded by Narsingh Rai in the 14th century, it played a pivotal role in the Gondwana region's history. While its core was in Madhya Pradesh, Kherla's influence extended into neighboring areas, including parts of present-day Chandrapur district in Maharashtra. This expansion facilitated cultural and political exchanges between the regions, contributing to Chandrapur's historical development. Kherla's interactions with neighboring powers, such as the Bahmani and Malwa Sultanates, further underscore its regional significance.  ",
    // 474
    "Deogarth King": " Deogarth King The Deogarh Kingdom, under the Gond dynasty, significantly influenced central India, including regions like Chandrapur. Founded by Ajanbahu Jatbasha (Jatba) in the late 16th century, the kingdom expanded its reach into parts of present-day Maharashtra. Jatba established Deogarh as a prominent Gond power, and his successors, notably Bakht Buland Shah, further extended the kingdom's influence. Bakht Buland Shah founded the city of Nagpur and integrated territories such as Chanda (now Chandrapur), Mandla, and Seoni into his realm. This expansion brought Chandrapur under the cultural and political umbrella of the Deogarh Kingdom, leaving a lasting impact on the region's history.\u200b  ",
    // 475
    "Lucie Smith": " Lucie Smith Charles Bean Lucie Smith was a British colonial official. In 1869, he authored the Report on the Land Revenue Settlement of the Chanda District, Central Provinces, attempting to provide a comprehensive analysis of the region's agrarian economy and administrative practices. This report offers valuable insights into the colonial governance and land revenue systems of the time.  ",
    // 476
    "R.V. Russel": " R.V. Russel \u200bRobert Vane Russell (1873\u20131915) was a British civil servant and ethnographer who served as Superintendent of Ethnography for the Central Provinces of British India. He co-authored The Tribes and Castes of the Central Provinces of India (1916) with Rai Bahadur Hira Lal. It was a four-volume work detailing the region's diverse communities. It is argued that Russell's research emphasized cultural narratives over anthropometric methods, offering valuable insights into the social fabric of areas like Chandrapur. \u200b  ",
    // 477
    "Bhim Balla Singh": " Bhim Balla Singh  Bhim Ballal Singh, a member of the Atram clan, is recognized as the founder of the Gond Kingdom of Chanda (present-day Chandrapur) around 870 CE. He consolidated various Gond communities , establishing his capital at Sirpur near the Wardha River and fortifying Manikgarh. His leadership laid the foundation for a dynasty that ruled the region for centuries.   ",
    // 478
    "Nilkanth Shah": " Nilkanth Shah \u200bNilkanth Shah (r. 1735\u20131751) was the last Gond ruler of the Chandrapur (Chanda) kingdom. His reign marked the end of Gond rule in the region due to conflicts with the Maratha Empire.\u200b In 1748, Nilkanth Shah allied with Raghunath Singh, the Diwan of Deogarh, to challenge Maratha dominance under Raghuji Bhosale. However, Raghuji swiftly suppressed the rebellion, defeating Nilkanth Shah and compelling him to sign a treaty in 1749 that ceded two-thirds of his kingdom's revenue to the Marathas. \u200bDespite this setback, Nilkanth Shah attempted another rebellion in 1751. Raghuji Bhonsle responded decisively, defeating Nilkanth Shah and imprisoning him in Ballarpur Fort, where he remained until his death. This event marked the dissolution of the Gond dynasty in Chandrapur, integrating the region into the Maratha-controlled Berar province.\u200bNilkanth Shah's tomb is located in Ballarpur, serving as a historical reminder of the Gond dynasty's legacy in the region.  ",
    // 479
    "Dinkar Singh": " Dinkar Singh Dinkar Singh was a Gond ruler of the Chanda (present-day Chandrapur) kingdom, succeeding his father, Khandkia Ballal Singh. His reign is noted for promoting peace and cultural development. Dinkar Singh encouraged Gond bards and supported Marathi literature, fostering a rich cultural environment in the region. His leadership contributed to the stability and prosperity of the Chanda kingdom during his tenure.\u200b   ",
    // 480
    "Suraj Ballal Singh": " Suraj Ballal Singh  Surja Ballal Singh, also known as Sher Shah, was a prominent Gond ruler of the Chanda (now Chandrapur) kingdom during the early 13th century (circa 1207\u20131242 CE). His reign is noted for military prowess, including a significant battle where he defeated Rajput chief Mohan Singh, earning him the title \"Sher Shah\" (Lion King). \u200bSurja Ballal Singh's legacy includes his son, Khandkya Ballal, who is credited with founding the city of Chandrapur. According to local lore, Khandkya Ballal was guided by a divine vision to establish the city at the confluence of the Erai and Zarpat rivers. This vision led to the construction of the Mahakali mandir, a significant cultural and religious site in Chandrapur. \u200bSurja Ballal Singh's leadership laid the foundation for the Gond dynasty's enduring influence in the region, shaping the historical and cultural landscape of Chandrapur.\u200b  ",
    // 481
    "Tel Thakurs": " Tel Thakurs The Tel Thakurs were Rajput officers who played a pivotal role in the establishment and fortification of Chandrapur (formerly known as Chanda) in the 13th century. Under the reign of King Khandkya Ballal, guided by his queen's counsel, the decision was made to construct a fortified city. The Tel Thakurs were entrusted with overseeing this significant endeavor, which included the meticulous planning and construction of the city's walls, gates, and bastions. Their contributions were instrumental in shaping Chandrapur's architectural and cultural heritage. \u200b   ",
    // 482
    "Erai River": " Erai River  \u200bThe Erai River is a vital waterway in Chandrapur district, originating near Kasarbodi village in Chimur taluka and flowing entirely within the district before merging with the Wardha River near Hadasti village. Spanning approximately 78 kilometers, it serves as a crucial water source for Chandrapur city and the Chandrapur Super Thermal Power Station (CSTPS) .\u200b Culturally, the Erai River holds local significance. It is associated with the founding legend of Chandrapur, where King Khandkya Ballal Sah, after being healed by the waters of a spring (believed to be part of the river system), established the city highlighting the river's importance in the region's historical narrative.\u200b  ",
    // 483
    "Raghoji II": " Raghoji Ii  Parsoji Bhonsle II, son of Raghoji II, briefly ruled the Nagpur kingdom in 1816. His rule was abruptly ended when his cousin, Appa Sahib (Mudhoji II), murdered him in 1817 to usurp the throne. Parsoji's death triggered political instability, drawing British intervention into Nagpur\u2019s succession and governance.  ",
    // 484
    "Treaty of 1818": " Treaty Of 1818 The Doctrine of Lapse was a policy introduced by Lord Dalhousie in the mid-19th century under British colonial rule. It stated that any princely state without a direct male heir would be annexed by the British East India Company. Applied notably to Jhansi and Nagpur, it caused widespread resentment and was a key factor leading to the 1857 revolt.  ",
    // 485
    "Captain W.H. Crichton": " Captain W.H. Crichton Captain W.H. Crichton (1819\u20131885) served as Deputy Commissioner of Chandrapur (then Chanda) during the Indian Revolt of 1857. In 1858, he led British forces to suppress the uprising led by the Gond leader Baburao Shedmake. It is argued that Crichton eventually captured Shedmake with assistance from local allies. Shedmake was tried and executed on 21 October 1858. Crichton's efforts were pivotal in reestablishing British colonial control in the region. \u200b   ",
    // 486
    "Pampa Revolt pf 1879-80": " Pampa Revolt Pf 1879-80  \u200bThe Rampa revolt of 1879\u201380 was a significant social l uprising in the Rampa region of the Vizagapatam Hill Tracts Agency (present-day Andhra Pradesh). Led by Chandrayya, the revolt was fueled by oppressive British policies, including the introduction of a toddy tax and the leasing of toddy tapping rights to contractors, which threatened the communities' traditional livelihoods. The revolt began in March 1879 with attacks on police stations in Chodavaram taluk and quickly spread across the district. The British responded by deploying a substantial military force, including infantry and cavalry regiments, to suppress the revolt. Despite fierce resistance, the revolt was eventually quelled, and many participants were imprisoned or deported. Chandrayya was killed in December 1880. The Rampa revolt remains a symbol of local resistance against colonial exploitation.   ",
    // 487
    "Sant Tukdoji Maharaj": " Sant Tukdoji Maharaj  Sant Tukdoji Maharaj was a well-known figure, social reformer, and freedom fighter who significantly influenced Chandrapur through his rural upliftment initiatives. He inspired self-reliance, cleanliness, and community service, especially in villages. His discourses and Gramgeeta teachings continue to impact Chandrapur's cultural and social life.   ",
    // 488
    "K.M. Subramaniam": " K.M. Subramaniam  \u200bK.M. Subramaniam, an Indian Forest Service (IFS) officer, served as the Additional Principal Chief Conservator of Forests in Maharashtra. He played a pivotal role in the preparation and revision of the Working Plan for the Chandrapur Forest Division, emphasizing sustainable forest management, conservation, and eco-tourism development. His contributions significantly influenced the strategic planning and ecological stewardship of Chandrapur's forest resources.\u200b  ",
    // 489
    "Netaji Subhas Chandra Bose": " Netaji Subhas Chandra Bose \u200bNetaji Subhas Chandra Bose (1897\u20131945) was a prominent leader in India's struggle for independence. Born in Cuttack, Odisha, he was influenced by Swami Vivekananda's teachings and later became a key figure in the Indian National Congress. Disillusioned with the Congress's moderate stance, he advocated for armed resistance against British rule. During World War II, Bose sought assistance from Axis powers, leading to the formation of the Indian National Army (INA) to fight against the British. His efforts significantly contributed to India's independence movement. \u200b   ",
    // 490
    "Patru Bhusari": " Patru Bhusari Patru Bhusari, born in 1917 was a freedom fighter from Chimur village in Chandrapur district. Born to Shri Varalu Bhusari, he worked as a labourer and actively participated in India's independence movement. His contributions are recognized among the unsung heroes of India's freedom struggle.   ",
    // 491
    "Rajura Tehsil": " Rajura Tehsil Rajura Tehsil, located in Chandrapur district, spans approximately 895 km\u00b2, comprising both rural and urban areas. As per the 2011 census, it has a population of around 138,408, with a literacy rate of 70.63%. Rajura town, the tehsil's administrative center, lies on the banks of the Wardha River and is a hub for coal and cement industries. The region is also known for mandirs like the Shri Saibaba mandir (Chota Shirdi) and Somnath Mandir. \u200b   ",
    // 492
    "Mr. R.S. Ellis": " Mr. R.S. Ellis Mr. R. S. Ellis of the Madras Civil Service was appointed as the first British administrator of Chandrapur (then Chanda) following its annexation under the Doctrine of Lapse in 1854. He assumed charge on 18 December 1854, marking the beginning of direct British governance in the region. Ellis's administration laid the foundation for subsequent colonial policies and consolidation of British rule in Chandrapur.   ",
    // 493
    "Megalithic stone": " Megalithic Stone The megalithic stones near Nagpur, particularly found in Junapani, are ancient burial markers dating back to 1000 BCE. These stone circles reflect early human settlement, social rituals, and astronomical knowledge. Their alignment suggests celestial observation. They are crucial to understanding the prehistoric culture of Vidarbha and indicate Nagpur's archaeological significance in India's early Iron Age civilisation.   ",
    // 494
    "Menhir stone": " Menhir Stone Menhir stones near Nagpur, especially in Junapani and surrounding regions, are upright monolithic stones believed to be part of megalithic burial practices. Dating back to the Iron Age, they possibly served ritualistic or commemorative purposes. Their presence highlights early human societal structures and ceremonial customs, underscoring Nagpur\u2019s role in the broader prehistoric and megalithic landscape of India.  ",
    // 495
    "Ahirs or Abhiras": " Ahirs Or Abhiras The Ahirs, also known as Abhiras, were an ancient pastoral community with significant influence in the Deccan region, including present-day Nagpur. They established the Abhira dynasty, which ruled parts of western Maharashtra, encompassing areas like Nashik, Khandesh, and Vidarbha, from approximately 203 to 370 CE. Their presence in the Vidarbha region underscores their role in shaping the early socio-political landscape of Nagpur and its surroundings. The modern Ahir community is considered to be descendants of the Abhiras.   ",
    // 496
    "Gaoli": " Gaoli The Gaoli, also known as Gavli or Gawli, are a pastoral community in Nagpur and the broader Vidarbha region. Traditionally engaged in cattle rearing and dairy farming, they are recognized as part of the Yadav community. Historical accounts suggest that the Gaoli established a kingdom in the area before the rise of the Gond dynasty, indicating their early influence in the region's socio-political landscape . Their expertise in animal husbandry contributed significantly to the local economy, particularly through the production of dairy products. In modern times, the Gaoli community continues to be an integral part of Nagpur's cultural and economic fabric.  ",
    // 497
    "Dantidurga": " Dantidurga Dantidurga, also known as Dantivarman II, was the founder of the Rashtrakuta Empire, reigning from 753 to 756 CE. His military campaigns extended into present-day Maharashtra, including the Vidarbha region encompassing Nagpur. By defeating the Chalukyas of Badami, he established Rashtrakuta dominance in the Deccan. His conquests in central India, including areas around Nagpur, marked the beginning of Rashtrakuta influence in the region. Dantidurga's reign laid the foundation for subsequent rulers to further expand the empire's territory and cultural impact.  ",
    // 498
    "King Krishna III": " King Krishna Iii  King Krishna III (r. 939\u2013967 CE), the last prominent ruler of the Rashtrakuta dynasty, played a significant role in shaping the history of the Deccan region, including areas encompassing present-day Nagpur. His military campaigns extended the empire's influence into northern territories, and his patronage of arts and literature left a lasting cultural legacy. The Rashtrakuta dynasty's control over the Vidarbha region, where Nagpur is located, during Krishna III's reign underscores the city's historical importance within the broader context of the empire's expansion and administration.   ",
    // 499
    "Kanarese Brahman": " Kanarese Brahman In the 10th century CE, during the reign of Rashtrakuta king Krishna III, a copper-plate inscription from Deoli in present-day Wardha district records the grant of a village named Talapurumshaka in the Nagapura-Nandivardhan region (modern Nagpur area) to a Kanarese Brahman. This indicates the presence and integration of Kannada-speaking Brahmins in the Nagpur region during that period, highlighting the cultural and administrative exchanges between Karnataka and Vidarbha.   ",
    // 500
    "Chalukya King Taila II": " Chalukya King Taila Ii Chalukya King Taila II (r. c. 973\u2013997 CE), also known as Tailapa II, was instrumental in reshaping the political landscape of the Deccan region, which includes present-day Nagpur. A former Rashtrakuta feudatory, he overthrew the last Rashtrakuta ruler, Karka II, in 973 CE, establishing the Western Chalukya dynasty with its capital at Manyakheta (modern Malkhed, Karnataka). His reign marked the resurgence of Chalukya power, influencing regions like Vidarbha and Nagpur through administrative reforms and cultural patronage. Taila II's consolidation of power laid the foundation for subsequent Chalukya rulers to expand their influence further into central India.   ",
    // 501
    "Munja's Seventh Attack": " Munja'S Seventh Attack The term \"Munja's seventh attack\" refers to the final military campaign of King Munja (Vakpati II), a prominent ruler of the Paramara dynasty in the late 10th century. Munja was known for his aggressive military expeditions, having launched multiple campaigns to expand his territory. His seventh and final campaign targeted the Western Chalukya kingdom, ruled by Tailapa II. Initially, Munja achieved some successes; however, he was ultimately defeated, captured, and executed by Tailapa II. This defeat marked a significant shift in the power dynamics of the Deccan region. While direct records of Munja's campaigns in Nagpur are scarce, the region's strategic location in the Vidarbha area suggests it may have been influenced by these broader geopolitical movements. The conflict between the Paramaras and the Chalukyas underscores the turbulent nature of the period and the constant struggle for dominance in central India.  ",
};

  // Function to find and highlight all words in the content
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


