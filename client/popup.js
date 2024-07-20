console.log("This is the javascript")

document.addEventListener('DOMContentLoaded', function() {
    const chamberStatusElement = document.getElementById('chamberStatus');
    const chamberReasoningButtonElement = document.getElementById('chamberReasoningButton');
    const chamberStatusGroupElement = document.getElementById('chamberStatusGroup');
    fetchChamberStatus(chamberStatusElement, chamberReasoningButtonElement, chamberStatusGroupElement).then(
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
        fetchChamberReasoning(chamberReasoningElement, chamberReasoningGroupElement).then(
            (data) => {
                chamberReasoningElement.textContent = data.chamberReasoning;
                chamberReasoningGroupElement.style.display = '';
            }
        )
    });
});

async function fetchChamberStatus() {
    const url = "http://127.0.0.1:8000/getEchoChamberStatus?identifier=OPK7wbZkx8w&chamber_type=youtube";
  
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

async function fetchChamberReasoning() {
    console.log("fetchChamberReasoning called")
    const url = "http://127.0.0.1:8000/getEchoChamberReasoning?identifier=OPK7wbZkx8w&chamber_type=youtube";
  
    try {
      const response = await fetch(url);
      const data = await response.json(); // Parse the JSON response
      return data
    } catch (error) {
      console.error("Error fetching data:", error);
    }
}
  