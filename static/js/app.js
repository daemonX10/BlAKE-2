// CYBERPUNK BLAKE2 HASH GENERATOR - Enhanced UI/UX System
document.addEventListener('DOMContentLoaded', function() {
    console.log('[SYSTEM] Initializing cyberpunk interface...');
    
    // Auto-focus on terminal input
    const terminalInput = document.querySelector('textarea[name="text"]');
    if (terminalInput && !terminalInput.value) {
        terminalInput.focus();
        addTerminalEffect(terminalInput);
    }

    // Enhanced cyberpunk input animations
    const inputs = document.querySelectorAll('.form-control, .form-select');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
            // Cyberpunk focus animation
            this.style.transform = 'translateY(-2px) scale(1.02)';
            this.style.boxShadow = '0 0 25px rgba(0, 255, 255, 0.6)';
            addGlitchEffect(this);
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
            this.style.transform = '';
            this.style.boxShadow = '';
            removeGlitchEffect(this);
        });

        // Real-time validation with cyberpunk feedback
        input.addEventListener('input', function() {
            validateFieldCyberpunk(this);
        });
    });

    // Initialize cyberpunk effects
    initializeMatrixRain();
    setupTerminalEffects();
    setupKeyPreviews();
    setupCyberpunkTooltips();
    setupFormSubmission();
});

// Cyberpunk form submission with enhanced visuals
function setupFormSubmission() {
    const form = document.getElementById('blake2Form');
    const submitBtn = document.getElementById('submitBtn');
    const spinner = document.getElementById('loadingSpinner');
    
    if (form) {
        form.addEventListener('submit', function(e) {
            // Show cyberpunk loading state
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-sync fa-spin"></i> PROCESSING HASH...';
            if (spinner) {
                spinner.style.display = 'inline-block';
            }
            
            // Validate all fields before submission
            const isValid = validateForm();
            if (!isValid) {
                e.preventDefault();
                // Reset button state
                resetSubmitButton();
                return false;
            }
        });
    }
}

// Enhanced form validation
function validateForm() {
    const form = document.getElementById('blake2Form');
    let isValid = true;
    
    // Check all required fields
    const requiredFields = form.querySelectorAll('[required], .form-control, .form-select');
    requiredFields.forEach(field => {
        if (!validateField(field)) {
            isValid = false;
        }
    });
    
    // BLAKE2 specific validation
    const blake2Key = document.querySelector('input[name="blake2_key"]');
    const blake2Salt = document.querySelector('input[name="blake2_salt"]');
    const blake2DigestSize = document.querySelector('select[name="blake2_digest_size"]');
    
    if (blake2Key && blake2Key.value) {
        // BLAKE2 key validation (0-64 bytes)
        const keyBytes = new TextEncoder().encode(blake2Key.value).length;
        if (keyBytes > 64) {
            showFieldError(blake2Key, 'Key must be 64 bytes or less');
            isValid = false;
        }
    }
    
    if (blake2Salt && blake2Salt.value) {
        // BLAKE2 salt validation (0-16 bytes)
        const saltBytes = new TextEncoder().encode(blake2Salt.value).length;
        if (saltBytes > 16) {
            showFieldError(blake2Salt, 'Salt must be 16 bytes or less');
            isValid = false;
        }
    }
    
    return isValid;
}

// Individual field validation
function validateField(field) {
    const value = field.value.trim();
    const fieldName = field.name;
    let isValid = true;
    
    // Clear previous errors
    clearFieldError(field);
    
    // Required field check
    if (field.hasAttribute('required') || field.classList.contains('form-control') || field.classList.contains('form-select')) {
        if (!value) {
            showFieldError(field, 'This field is required');
            isValid = false;
        }
    }
    
    // Field-specific validation
    switch (fieldName) {
        case 'blake2_key':
            if (value) {
                const keyBytes = new TextEncoder().encode(value).length;
                if (keyBytes > 64) {
                    showFieldError(field, 'Key must be 64 bytes or less');
                    isValid = false;
                }
            }
            break;
        case 'blake2_salt':
            if (value) {
                const saltBytes = new TextEncoder().encode(value).length;
                if (saltBytes > 16) {
                    showFieldError(field, 'Salt must be 16 bytes or less');
                    isValid = false;
                }
            }
            break;
        case 'blake2_digest_size':
            const digestSize = parseInt(value);
            if (value && (digestSize < 1 || digestSize > 64)) {
                showFieldError(field, 'Digest size must be between 1 and 64 bytes');
                isValid = false;
            }
            break;
    }
    
    if (isValid) {
        field.classList.remove('is-invalid');
        field.classList.add('is-valid');
    }
    
    return isValid;
}

// Show field error
function showFieldError(field, message) {
    field.classList.add('is-invalid');
    field.classList.remove('is-valid');
    
    // Find or create error message element
    let errorElement = field.parentElement.querySelector('.invalid-feedback');
    if (!errorElement) {
        errorElement = document.createElement('div');
        errorElement.className = 'invalid-feedback';
        field.parentElement.appendChild(errorElement);
    }
    errorElement.textContent = message;
}

// Clear field error
function clearFieldError(field) {
    field.classList.remove('is-invalid');
    const errorElement = field.parentElement.querySelector('.invalid-feedback');
    if (errorElement) {
        errorElement.textContent = '';
    }
}

// Reset submit button to original state
function resetSubmitButton() {
    const submitBtn = document.getElementById('submitBtn');
    const spinner = document.getElementById('loadingSpinner');
    
    if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.innerHTML = 'Generate Hash';
    }
    if (spinner) {
        spinner.style.display = 'none';
    }
}

// Copy to clipboard functionality with enhanced feedback
function copyToClipboard(elementId) {
    const element = document.getElementById(elementId);
    const text = element.textContent;
    
    navigator.clipboard.writeText(text).then(() => {
        // Show success feedback
        const btn = event.target.closest('.copy-btn');
        const originalContent = btn.innerHTML;
        btn.innerHTML = '<i class="fas fa-check"></i> Copied!';
        btn.style.background = '#10b981';
        
        // Add ripple effect
        addRippleEffect(btn);
        
        setTimeout(() => {
            btn.innerHTML = originalContent;
            btn.style.background = '';
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy text: ', err);
        showNotification('Failed to copy text to clipboard', 'error');
    });
}

// Add ripple effect to buttons
function addRippleEffect(button) {
    const ripple = document.createElement('span');
    ripple.classList.add('ripple');
    button.appendChild(ripple);
    
    setTimeout(() => {
        ripple.remove();
    }, 600);
}

// Key preview functionality
function setupKeyPreviews() {
    const blake2Key = document.querySelector('input[name="blake2_key"]');
    const blake2Salt = document.querySelector('input[name="blake2_salt"]');
    const blake2DigestSize = document.querySelector('select[name="blake2_digest_size"]');
    
    // Add real-time previews for BLAKE2 parameters
    if (blake2Key) {
        blake2Key.addEventListener('input', updateBlake2Preview);
    }
    if (blake2Salt) {
        blake2Salt.addEventListener('input', updateBlake2Preview);
    }
    if (blake2DigestSize) {
        blake2DigestSize.addEventListener('change', updateBlake2Preview);
    }
}

// Update BLAKE2 configuration preview
function updateBlake2Preview() {
    const keyValue = document.querySelector('input[name="blake2_key"]')?.value || '';
    const saltValue = document.querySelector('input[name="blake2_salt"]')?.value || '';
    const digestSize = document.querySelector('select[name="blake2_digest_size"]')?.value || '32';
    
    // Calculate byte lengths
    const keyBytes = new TextEncoder().encode(keyValue).length;
    const saltBytes = new TextEncoder().encode(saltValue).length;
    
    console.log(`BLAKE2 Configuration:
        - Digest Size: ${digestSize} bytes (${digestSize * 8} bits)
        - Key: ${keyBytes} bytes
        - Salt: ${saltBytes} bytes`);
}

// Setup tooltips for additional information
function setupTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', showTooltip);
        element.addEventListener('mouseleave', hideTooltip);
    });
}

// Show notification system
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} notification fade-in`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-triangle'}"></i>
        ${message}
    `;
    
    // Add to top of container
    const container = document.querySelector('.container');
    container.insertBefore(notification, container.firstChild);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        notification.remove();
    }, 5000);
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + Enter to submit form
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        const form = document.getElementById('blake2Form');
        if (form) {
            form.dispatchEvent(new Event('submit'));
        }
    }
    
    // Escape to clear form
    if (e.key === 'Escape') {
        const inputs = document.querySelectorAll('.form-control, .form-select');
        inputs.forEach(input => {
            if (input.type !== 'submit') {
                input.value = '';
                clearFieldError(input);
            }
        });
    }
});

// Cyberpunk matrix rain effect
function initializeMatrixRain() {
    const matrixContainer = document.querySelector('.matrix-rain');
    if (!matrixContainer) return;
    
    const binaryChars = '01';
    const density = 50;
    
    for (let i = 0; i < density; i++) {
        const drop = document.createElement('div');
        drop.style.position = 'absolute';
        drop.style.left = Math.random() * 100 + '%';
        drop.style.fontSize = '12px';
        drop.style.color = 'rgba(0, 255, 255, 0.1)';
        drop.style.fontFamily = '"Courier Prime", monospace';
        drop.style.animationDelay = Math.random() * 20 + 's';
        drop.style.animationDuration = (15 + Math.random() * 10) + 's';
        drop.style.animation = 'matrix-fall linear infinite';
        
        // Generate random binary string
        let binaryString = '';
        for (let j = 0; j < 20; j++) {
            binaryString += binaryChars[Math.floor(Math.random() * binaryChars.length)];
        }
        drop.textContent = binaryString;
        
        matrixContainer.appendChild(drop);
    }
}

// Terminal typing effect
function addTerminalEffect(element) {
    element.addEventListener('input', function() {
        if (this.value.length > 0 && !this.value.startsWith('> ')) {
            this.value = '> ' + this.value;
        }
    });
}

// Glitch effect for focused elements
function addGlitchEffect(element) {
    element.classList.add('glitch');
    element.setAttribute('data-text', element.value || element.textContent);
}

function removeGlitchEffect(element) {
    element.classList.remove('glitch');
}

// Cyberpunk field validation
function validateFieldCyberpunk(field) {
    const value = field.value.trim();
    
    // Remove existing validation classes
    field.classList.remove('is-valid', 'is-invalid');
    
    // Add cyberpunk validation styling
    if (value) {
        field.classList.add('is-valid');
        field.style.borderColor = 'var(--accent-color)';
        field.style.boxShadow = '0 0 15px rgba(0, 255, 0, 0.3)';
    } else if (field.hasAttribute('required')) {
        field.classList.add('is-invalid');
        field.style.borderColor = 'var(--danger-color)';
        field.style.boxShadow = '0 0 15px rgba(255, 82, 82, 0.3)';
    }
}

// Enhanced terminal effects
function setupTerminalEffects() {
    // Add scanning line effect to main container
    const mainCard = document.querySelector('.main-card');
    if (mainCard) {
        mainCard.classList.add('scan-lines');
    }
    
    // Add cursor effect to result text
    const resultTexts = document.querySelectorAll('.result-text');
    resultTexts.forEach(text => {
        text.classList.add('terminal-cursor');
    });
}

// Cyberpunk tooltips
function setupCyberpunkTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            showCyberpunkTooltip(this);
        });
        element.addEventListener('mouseleave', function() {
            hideCyberpunkTooltip();
        });
    });
}

function showCyberpunkTooltip(element) {
    const tooltip = document.createElement('div');
    tooltip.className = 'cyberpunk-tooltip';
    tooltip.textContent = element.getAttribute('data-tooltip');
    tooltip.style.cssText = `
        position: absolute;
        background: rgba(0, 0, 0, 0.9);
        color: var(--primary-color);
        padding: 8px 12px;
        border-radius: 4px;
        font-family: 'Courier Prime', monospace;
        font-size: 12px;
        border: 1px solid var(--primary-color);
        box-shadow: 0 0 15px rgba(0, 255, 255, 0.5);
        z-index: 1000;
        pointer-events: none;
    `;
    
    document.body.appendChild(tooltip);
    
    const rect = element.getBoundingClientRect();
    tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
    tooltip.style.top = rect.top - tooltip.offsetHeight - 8 + 'px';
}

function hideCyberpunkTooltip() {
    const tooltip = document.querySelector('.cyberpunk-tooltip');
    if (tooltip) {
        tooltip.remove();
    }
}

// Enhanced Bootstrap validation with cyberpunk style
(function() {
    'use strict';
    window.addEventListener('load', function() {
        const forms = document.getElementsByClassName('needs-validation');
        Array.prototype.filter.call(forms, function(form) {
            form.addEventListener('submit', function(event) {
                if (form.checkValidity() === false) {
                    event.preventDefault();
                    event.stopPropagation();
                    
                    // Add cyberpunk error effects
                    const invalidFields = form.querySelectorAll(':invalid');
                    invalidFields.forEach(field => {
                        field.style.animation = 'glitch 0.5s ease-in-out';
                        setTimeout(() => {
                            field.style.animation = '';
                        }, 500);
                    });
                }
                form.classList.add('was-validated');
            }, false);
        });
    }, false);
})();
