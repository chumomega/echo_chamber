// Use "http://127.0.0.1:8000" in dev and https://echochamber-mtxmtj5oba-ue.a.run.app/ in prod
const SERVER_URL = "https://echochamber-mtxmtj5oba-ue.a.run.app/"
// const SERVER_URL = "http://127.0.0.1:8000"
const DESKTOP_YOUTUBE_VIDEO_REGEX = /^(https\:\/\/www\.youtube\.com\/watch\?v=){1}.+/;
const REDDIT_REGEX = /^(https?:\/\/)?(?:www\.)?reddit\.com\/r\/[\w\d\-_]+\/comments\/[\w\d]+/;
const REDDIT_ID_REGEX = /\/r\/[\w\d]+\/comments\/([\w\d]+)\//;
const TWITTER_REGEX = /^https:\/\/(www\.)?x\.com\/(?:[A-Za-z0-9]+)\/status\/([0-9]+)$/;
const TWITTER_ID_REGEX = /\/status\/(\d+)/;

const isDesktopYoutubeUrl = (searchQuery) => {
    return DESKTOP_YOUTUBE_VIDEO_REGEX.test(searchQuery);
}

const getVideoIdFromDesktopYoutubeVideoUrl = (desktopYoutubeUrl) => {
    let urlSearchParamsStart = desktopYoutubeUrl.indexOf('?')
    let urlSearchParams = desktopYoutubeUrl.substring(urlSearchParamsStart)
    return (new URLSearchParams(urlSearchParams)).get('v');
}

const isRedditUrl = (searchQuery) => {
    isReddit = REDDIT_REGEX.test(searchQuery)
    return isReddit;
}

const getThreadIdFromRedditUrl = (redditUrl) => {
    const match = REDDIT_ID_REGEX.exec(redditUrl);
    return match ? match[1] : null;
}

const isTwitterUrl = (searchQuery) => {
    isTwitter = TWITTER_REGEX.test(searchQuery)
    return isTwitter;
}

const getStatusIdFromTwitterUrl = (twitterUrl) => {
    const match = TWITTER_ID_REGEX.exec(twitterUrl);
    return match ? match[1] : null;
}

document.addEventListener('DOMContentLoaded', function() {
    const chamberStatusElement = document.getElementById('chamberStatus');
    const chamberReasoningButtonElement = document.getElementById('chamberReasoningButton');
    const chamberStatusGroupElement = document.getElementById('chamberStatusGroup');
    const chamberAlternativesButtonElement = document.getElementById('chamberAlternativesButton');
    const loadingSpinnerElement = document.getElementById('loading-spinner-1');

    getIdentifierAndType().then(
        ({ identifier, type }) => {
            fetchChamberStatus(identifier, type).then(
                (data) => {
                    var chamberStatusContent = null
                    var chamberReasoningButtonContent = null
                    if (data.isBiasedChamber) {
                        chamberStatusContent = `
                            This is most likely a ${data.biasedChamber} 
                            echo chamber by ${getChamberPercentage(data.biasedChamber, 
                                data.chamberLabelMagnitudes)}%`;
                        chamberReasoningButtonContent = "Why is this an echo chamber?"
                    } else {
                        chamberStatusContent = "This is not a biased echo chamber";
                        chamberReasoningButtonContent = "Why is this not echo chamber?";
                    }
                    loadingSpinnerElement.style.display = 'none';
                    chamberStatusElement.textContent = chamberStatusContent
                    chamberReasoningButtonElement.textContent = chamberReasoningButtonContent
                    chamberStatusGroupElement.style.display = '';
                }
            ).catch(
                error => {
                    console.error("Error fetching ChamberStatus:", error);
                    const contentDiv = document.getElementById('mainContent');
                    const paragraph = document.createElement('p');
                    paragraph.textContent = "We don't support this website yet, but please try again later.";
                    contentDiv.appendChild(paragraph);
                    contentDiv.classList.add("lead")
                    loadingSpinnerElement.style.display = 'none';
                }
            )

            const chamberReasoningElement = document.getElementById('chamberReasoning');
            const chamberReasoningGroupElement = document.getElementById('chamberReasoningGroup');
            const chamberAlternativesElement = document.getElementById('chamberAlternatives');
            const chamberAlternativesGroupElement = document.getElementById('chamberAlternativesGroup');
            chamberReasoningButtonElement.addEventListener('click', function () {
                chamberReasoningButtonElement.disabled = true;
                loadingSpinnerElement.style.display = '';
                fetchChamberReasoning(identifier, type).then(
                    (data) => {
                        loadingSpinnerElement.style.display = 'none';
                        chamberReasoningElement.textContent = data.chamberReasoning;
                        chamberReasoningGroupElement.style.display = '';
                        // chamberAlternativesGroupElement.style.display = ''
                    }
                ).catch(
                    error => {
                        console.error("Error fetching ChamberReasoning:", error);
                        const contentDiv = document.getElementById('mainContent');
                        const paragraph = document.createElement('p');
                        paragraph.textContent = "We don't support this website yet, but please try again later.";
                        contentDiv.appendChild(paragraph);
                        contentDiv.classList.add("lead")
                        loadingSpinnerElement.style.display = 'none';
                    }
                )
            });
            chamberAlternativesButtonElement.addEventListener('click', function () {
                chamberAlternativesButtonElement.disabled = true;
                loadingSpinnerElement.style.display = '';
                fetchChamberAlternatives(identifier, type).then(
                    (data) => {
                        data.diverseChamberObjects.forEach(chamberObj => {
                            const listItem = document.createElement('li');
                            listItem.appendChild(
                                createCardComponent(
                                    chamberObj.title, 
                                    chamberObj.author, 
                                    chamberObj.chamber_status,
                                    chamberObj.url
                                )
                            );
                            chamberAlternativesElement.appendChild(listItem);
                        })
                        loadingSpinnerElement.style.display = 'none';
                        chamberAlternativesGroupElement.style.display = '';
                    }
                ).catch(
                    error => {
                        console.error("Error fetching ChamberAlternatives:", error);
                        const contentDiv = document.getElementById('mainContent');
                        const paragraph = document.createElement('p');
                        paragraph.textContent = "We don't support this website yet, but please try again later.";
                        contentDiv.appendChild(paragraph);
                        contentDiv.classList.add("lead")
                        loadingSpinnerElement.style.display = 'none';
                    }
                )
            });
        }
    ).catch(error => {
        console.log(error);
        const contentDiv = document.getElementById('mainContent');
        const paragraph = document.createElement('p');
        paragraph.textContent = "We don't support this website yet, but please try again later.";
        contentDiv.appendChild(paragraph);
        contentDiv.classList.add("lead")
        loadingSpinnerElement.style.display = 'none';
    });
});

async function getIdentifierAndType() {
    const [tab] = await chrome.tabs.query({active: true, lastFocusedWindow: true});
    let identifier = null
    let type = null
    if (isDesktopYoutubeUrl(tab.url)) {
        identifier = getVideoIdFromDesktopYoutubeVideoUrl(tab.url)
        type = "youtube"
    } else if (isRedditUrl(tab.url)) {
        identifier = getThreadIdFromRedditUrl(tab.url)
        type = "reddit"
    } else if (isTwitterUrl(tab.url)) {
        identifier = getStatusIdFromTwitterUrl(tab.url)
        type = "twitter"
    } else {
        throw(`Supported Platform content not found for url: ${tab.url}`)
    }
    return {identifier, type}
}

async function fetchChamberStatus(identifier, type) {
    console.log("fetchChamberStatus called")
    const url = `${SERVER_URL}/getEchoChamberStatus?identifier=${identifier}&chamber_type=${type}`;

    const response = await fetch(url);
    const data = await response.json(); // Parse the JSON response
    return data
}

function getChamberPercentage(chamber, chamberLabelMagnitudes) {
    var sum = 0;
    Object.keys(chamberLabelMagnitudes).forEach(function(key) {
        sum += chamberLabelMagnitudes[key]
    })
    return ((chamberLabelMagnitudes[chamber]/sum) * 100).toFixed(2)
}

async function fetchChamberReasoning(identifier, type) {
    console.log("fetchChamberReasoning called")
    const url = `${SERVER_URL}/getEchoChamberReasoning?identifier=${identifier}&chamber_type=${type}`;
  
    try {
      const response = await fetch(url);
      const data = await response.json(); // Parse the JSON response
      return data
    } catch (error) {
      console.error("Error fetching data:", error);
    }
}

async function fetchChamberAlternatives(identifier, type) {
    console.log("fetchChamberReasoning called")
    const url = `${SERVER_URL}/getDiverseEchoChambers?identifier=${identifier}&chamber_type=${type}`;

    try {
      const response = await fetch(url);
      const data = await response.json(); // Parse the JSON response
      return data
    } catch (error) {
      console.error("Error fetching data:", error);
    }
}
  
function createCardComponent(title, subtitle, text, link1) {
    const card = document.createElement('div');
    card.classList.add('card', 'mb-3'); // Add Bootstrap classes for styling
  
    const cardBody = document.createElement('div');
    cardBody.classList.add('card-body');
  
    const cardLink1 = document.createElement('a');
    cardLink1.classList.add('card-link');
    cardLink1.href = link1;
    cardLink1.textContent = title;
    cardLink1.target = "_blank";
    
    const cardTitle = document.createElement('h5');
    cardTitle.classList.add('card-title');
    cardTitle.appendChild(cardLink1)
  
  
    const cardSubtitle = document.createElement('h6');
    cardSubtitle.classList.add('card-subtitle', 'mb-2', 'text-body-secondary');
    cardSubtitle.textContent  = subtitle;
  
    const cardText = document.createElement('span');
    cardText.classList.add('badge', 'rounded-pill',  'text-bg-info');
    cardText.textContent = text;

    cardBody.appendChild(cardTitle);
    cardBody.appendChild(cardSubtitle);
    cardBody.appendChild(cardText);
    card.appendChild(cardBody);
  
    return card;
  }