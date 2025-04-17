function validateForm() {
    let isValid = true;

    let tumorSize = document.getElementById("tumor_size").value;
    let smokingHistory = document.getElementById("smoking_history").value;
    let stage = document.getElementById("stage").value;
    let bpSystolic = document.getElementById("bp_systolic").value;
    let wbcCount = document.getElementById("wbc_count").value;
    let ldhLevel = document.getElementById("ldh_level").value;

    document.querySelectorAll('.error').forEach(el => el.textContent = '');

    if (tumorSize <= 0) {
        document.getElementById("tumor_size_error").textContent = "Tumor size must be greater than 0.";
        isValid = false;
    }
    
    if (!smokingHistory) {
        document.getElementById("smoking_history_error").textContent = "Please select a smoking history.";
        isValid = false;
    }

    if (!stage) {
        document.getElementById("stage_error").textContent = "Please select a cancer stage.";
        isValid = false;
    }

    if (bpSystolic < 50 || bpSystolic > 200) {
        document.getElementById("bp_systolic_error").textContent = "Systolic blood pressure must be between 50 and 200.";
        isValid = false;
    }

    if (wbcCount < 0 || wbcCount > 50000) {
        document.getElementById("wbc_count_error").textContent = "WBC count must be between 1000 and 50000.";
        isValid = false;
    }

    if (ldhLevel < 100 || ldhLevel > 10000) {
        document.getElementById("ldh_level_error").textContent = "LDH level must be between 100 and 1000.";
        isValid = false;
    }

    if (isValid) {
        let formData = new FormData(document.getElementById("predictionForm"));
        fetch("/predict", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById("result").innerText = "Predicted Treatment: " + data.prediction;
        })
        .catch(error => console.error("Error:", error));
    }

    return false;
}
