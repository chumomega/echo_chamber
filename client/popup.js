// Use "http://127.0.0.1:8000" in dev and https://echochamber-mtxmtj5oba-ue.a.run.app/ in prod
//const SERVER_URL = "https://echochamber-mtxmtj5oba-ue.a.run.app/"
const SERVER_URL = "http://127.0.0.1:8000"
const DESKTOP_YOUTUBE_VIDEO_REGEX = /^(https\:\/\/www\.youtube\.com\/watch\?v=){1}.+/;

const isDesktopYoutubeUrl = (searchQuery) => {
    return DESKTOP_YOUTUBE_VIDEO_REGEX.test(searchQuery);
}

const getPodcastIdFromDesktopYoutubeVideoUrl = (desktopYoutubeUrl) => {
    let urlSearchParamsStart = desktopYoutubeUrl.indexOf('?')
    let urlSearchParams = desktopYoutubeUrl.substring(urlSearchParamsStart)
    return (new URLSearchParams(urlSearchParams)).get('v');
}

document.addEventListener('DOMContentLoaded', function() {
    const chamberStatusElement = document.getElementById('chamberStatus');
    const chamberReasoningButtonElement = document.getElementById('chamberReasoningButton');
    const chamberStatusGroupElement = document.getElementById('chamberStatusGroup');

    getIdentifierAndType().then(
        ({ identifier, type }) => {
            fetchChamberStatus(identifier, type).then(
                (data) => {
                    var chamberStatusContent = null
                    var buttonContent = null
                    if (data.isBiasedChamber) {
                        chamberStatusContent = `
                            This is most likely a ${data.biasedChamber} 
                            echo chamber by ${getChamberPercentage(data.biasedChamber, 
                                data.chamberLabelMagnitudes)}%`;
                        buttonContent = "Why is this an echo chamber?"
                    } else {
                        chamberStatusContent = "This is not a biased echo chamber";
                        buttonContent = "Why is this not echo chamber?"
                    }
                    
                    chamberStatusElement.textContent = chamberStatusContent
                    chamberReasoningButtonElement.textContent = buttonContent
                    chamberStatusGroupElement.style.display = '';
                }
            )

            const chamberReasoningElement = document.getElementById('chamberReasoning');
            const chamberReasoningGroupElement = document.getElementById('chamberReasoningGroup');
            chamberReasoningButtonElement.addEventListener('click', function () {
                fetchChamberReasoning(identifier, type).then(
                    (data) => {
                        chamberReasoningElement.textContent = data.chamberReasoning;
                        chamberReasoningGroupElement.style.display = '';
                    }
                )
            });
        }
    ).catch(error => {
        console.error("Error: ", error);
    });
});

async function getIdentifierAndType() {
    const [tab] = await chrome.tabs.query({active: true, lastFocusedWindow: true});
    let identifier = null
    let type = null
    if (isDesktopYoutubeUrl(tab.url)) {
        identifier = getPodcastIdFromDesktopYoutubeVideoUrl(tab.url)
        type = "youtube"
    } else {
        throw("Supported Platform content not found")
    }
    return {identifier, type}
}

async function fetchChamberStatus(identifier, type) {
    console.log("fetchChamberStatus called")
    const url = `${SERVER_URL}/getEchoChamberStatus?identifier=${identifier}&chamber_type=${type}`;
  
    try {
      const response = await fetch(url);
      const data = await response.json(); // Parse the JSON response
      return data
    } catch (error) {
      console.error("Error fetching data:", error);
    }
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
  