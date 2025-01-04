document.addEventListener('DOMContentLoaded', function() {
    // Formateo de número de teléfono
    const phoneInput = document.querySelector('input[name="phone"]');
    if (phoneInput) {
        phoneInput.addEventListener('input', function(e) {
            // Elimina todo excepto números
            let x = e.target.value.replace(/\D/g, '');
            
            // Aplica el formato (XXX) XXX-XXXX
            if (x.length > 0) {
                if (x.length <= 3) {
                    x = x;
                } else if (x.length <= 6) {
                    x = x.slice(0,3) + '-' + x.slice(3);
                } else if (x.length <= 10) {
                    x = x.slice(0,3) + '-' + x.slice(3,6) + '-' + x.slice(6);
                } else {
                    x = x.slice(0,3) + '-' + x.slice(3,6) + '-' + x.slice(6,10);
                }
            }
            
            e.target.value = x;
        });
    }

    // Copiar token al portapapeles
    const tokenElement = document.querySelector('.token-container');
    if (tokenElement) {
        const tokenText = tokenElement.textContent;
        const copyButton = document.createElement('button');
        copyButton.className = 'mt-2 px-3 py-1 text-sm text-indigo-600 border border-indigo-600 rounded hover:bg-indigo-50';
        copyButton.textContent = 'Copy Token';
        
        copyButton.addEventListener('click', async function() {
            try {
                await navigator.clipboard.writeText(tokenText);
                const originalText = copyButton.textContent;
                copyButton.textContent = 'Copied!';
                copyButton.classList.add('bg-green-50', 'text-green-600', 'border-green-600');
                
                setTimeout(() => {
                    copyButton.textContent = originalText;
                    copyButton.classList.remove('bg-green-50', 'text-green-600', 'border-green-600');
                }, 2000);
            } catch (err) {
                console.error('Failed to copy text: ', err);
            }
        });
        
        tokenElement.parentNode.insertBefore(copyButton, tokenElement.nextSibling);
    }

    // Validación del formulario
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function(e) {
            const emailInput = form.querySelector('input[name="email"]');
            const phoneInput = form.querySelector('input[name="phone"]');
            
            // Validación básica de email
            if (emailInput && !isValidEmail(emailInput.value)) {
                e.preventDefault();
                showError(emailInput, 'Please enter a valid email address');
            }
            
            // Validación de teléfono
            if (phoneInput && !isValidPhone(phoneInput.value)) {
                e.preventDefault();
                showError(phoneInput, 'Please enter a valid phone number');
            }
        });
    }
});

// Funciones de utilidad
function isValidEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function isValidPhone(phone) {
    // Acepta formatos: XXX-XXX-XXXX
    const re = /^\d{3}-\d{3}-\d{4}$/;
    return re.test(phone);
}

function showError(inputElement, message) {
    // Elimina mensajes de error previos
    const existingError = inputElement.parentNode.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }
    
    // Crea y muestra el nuevo mensaje de error
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message text-red-500 text-xs mt-1';
    errorDiv.textContent = message;
    inputElement.parentNode.appendChild(errorDiv);
    
    // Resalta el input
    inputElement.classList.add('border-red-500', 'focus:border-red-500', 'focus:ring-red-500');
    
    // Quita el resaltado después de 5 segundos
    setTimeout(() => {
        inputElement.classList.remove('border-red-500', 'focus:border-red-500', 'focus:ring-red-500');
        errorDiv.remove();
    }, 5000);
}