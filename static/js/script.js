document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector(".prediction-form");
    const bhkInput = document.getElementById("bhk"); // Changed order
    const bathInput = document.getElementById("bath"); // Changed order
    const sqftInput = document.getElementById("sqft"); // Changed order

    // Helper function to display an error message
    function showError(inputElement, message) {
        const formGroup = inputElement.closest(".form-group");
        let errorDiv = formGroup.querySelector(".error-message");

        if (!errorDiv) {
            errorDiv = document.createElement("div");
            errorDiv.classList.add("error-message");
            formGroup.appendChild(errorDiv);
        }
        errorDiv.textContent = message;
        inputElement.classList.add("input-error");
    }

    // Helper function to clear an error message
    function clearError(inputElement) {
        const formGroup = inputElement.closest(".form-group");
        const errorDiv = formGroup.querySelector(".error-message");
        if (errorDiv) {
            errorDiv.remove();
        }
        inputElement.classList.remove("input-error");
    }

    form.addEventListener("submit", function (e) {
        // Clear all previous errors at the start of a new submission attempt
        clearError(bhkInput);
        clearError(bathInput);
        clearError(sqftInput);

        let isValid = true; // Flag to track overall form validity

        const bhk = parseInt(bhkInput.value);
        const bath = parseInt(bathInput.value);
        const sqft = parseFloat(sqftInput.value);


        // Validation for BHK
        if (isNaN(bhk) || bhk < 1 || bhk > 10) {
            showError(bhkInput, "BHK must be between 1 and 10.");
            isValid = false;
        }

        // Validation for Bathrooms
        if (isNaN(bath) || bath < 1 || bath > 5) {
            showError(bathInput, "Bathrooms must be between 1 and 5.");
            isValid = false;
        }

        // Validation for Total Sqft
        if (isNaN(sqft) || sqft < 200 || sqft > 10000) {
            showError(sqftInput, "Total Sqft must be between 200 and 10,000.");
            isValid = false;
        }


        // Logical check: Bathrooms cannot exceed BHK (only if basic validity holds)
        if (isValid && bath > bhk) {
            showError(bathInput, "Bathrooms cannot be more than BHK.");
            isValid = false;
        }

        if (!isValid) {
            e.preventDefault(); // Prevent form submission if any validation fails
        }
    });

    // Add event listeners to clear errors as user types for immediate feedback
    bhkInput.addEventListener("input", () => clearError(bhkInput));
    bathInput.addEventListener("input", () => clearError(bathInput));
    sqftInput.addEventListener("input", () => clearError(sqftInput));
});