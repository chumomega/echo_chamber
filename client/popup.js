console.log("This is the javascript")

document.addEventListener('DOMContentLoaded', function() {
    const button = document.getElementById('chamberReasoningButton');
    const chamberReasoningElement = document.getElementById('chamberReasoning');
    button.addEventListener('click', function () {
        fetchChamberReasoning(chamberReasoningElement)
    });
});

async function fetchChamberReasoning(textElement) {
    const url = "http://127.0.0.1:8000/getEchoChamberReasoning?identifier=OPK7wbZkx8w&chamber_type=youtube";
  
    try {
      const response = await fetch(url);
      const data = await response.json(); // Parse the JSON response
      textElement.textContent = data.chamberReasoning;
    } catch (error) {
      console.error("Error fetching data:", error);
    }
}
  